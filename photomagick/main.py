# -*- coding: utf-8 -*-

__author__ = "Karol Będkowski"
__copyright__ = "Copyright (c) Karol Będkowski, 2011"
__version__ = "2011-04-24"


import sys
reload(sys)
try:
	sys.setappdefaultencoding("utf-8")
except AttributeError:
	sys.setdefaultencoding("utf-8")

import logging
from optparse import OptionParser
import locale
import gettext
import os


def show_version(*_args, **_kwargs):
	from photomagick import version
	print version.INFO
	exit(0)


def _parse_opt():
	optp = OptionParser()
	optp.add_option('--debug', '-d', action="store_true", default=False,
			help='enable debug messages')
	optp.add_option('--version', action="callback", callback=show_version,
		help='show information about application version')
	optp.add_option("-D", "--debug_scripts",
			action="store_true", dest="debug_scripts", default=False,
			help="draw additional debug information on imges")
	optp.add_option("-F", "--filter",
			dest="filter",
			help="filter names (separate by ,) for batch processing")
	optp.add_option('--list-filters', action='store_true',
			dest="list_filters",
			help='show available filters')
	optp.add_option('--list-filter-names', action='store_true',
			dest="list_filter_names",
			help='show available filters (only names)')
	optp.add_option("-b", "--batch",
			dest="batch", action="store_true",
			help="run batch processing")
	optp.add_option("-v", "--verbose",
			dest="verbose", action="store_true",
			help="print more messages")
	optp.add_option("-o", "--output",
			dest="output",
			help="output directory for batch processed images")
	optp.add_option("-p", "--postfix",
			dest="postfix",
			help="output file name postfix for batch processed images")
	options, args = optp.parse_args()
	if options.batch:
		if not options.filter:
			optp.error("missing filter name for batch processing")
		if not args:
			optp.error("missing input files")
	return options, args

_OPTIONS, _ARGS = _parse_opt()


from photomagick.lib.logging_setup import logging_setup
logging_setup('photomagick.log', _OPTIONS.debug or _OPTIONS.verbose)
_LOG = logging.getLogger(__name__)


from photomagick.lib import appconfig


def _setup_locale():
	''' setup locales and gettext '''
	app_config = appconfig.AppConfig('photomagick.cfg', 'photomagick')
	locales_dir = app_config.locales_dir
	package_name = 'photomagick'
	_LOG.info('run: locale dir: %s' % locales_dir)
	try:
			locale.bindtextdomain(package_name, locales_dir)
			locale.bind_textdomain_codeset(package_name, "UTF-8")
	except AttributeError:
			pass
	default_locale = locale.getdefaultlocale()
	locale.setlocale(locale.LC_ALL, '')
	os.environ['LC_ALL'] = os.environ.get('LC_ALL') or default_locale[0]
	gettext.install(package_name, localedir=locales_dir, unicode=True,
					names=("ngettext",))
	gettext.bindtextdomain(package_name, locales_dir)
	gettext.bindtextdomain('wxstd', locales_dir)
	gettext.bind_textdomain_codeset(package_name, "UTF-8")

	_LOG.info('locale: %s' % str(locale.getlocale()))


_setup_locale()

import random
import glob
import itertools

import Image as PILImage

from photomagick import filters


def get_filter(filename):
	return filters.MODULES[filename]


def run_gui(filename):
	if not appconfig.is_frozen():
		try:
			import wxversion
			try:
				wxversion.select('2.8')
			except wxversion.AlreadyImportedError:
				pass
		except ImportError, err:
			print 'No wxversion.... (%s)' % str(err)

	import wx

	from photomagick.gui.frame_main import FrameMain
	from photomagick.lib import iconprovider

	config = appconfig.AppConfig()
	app = wx.PySimpleApp(0)
	wx.InitAllImageHandlers()
	if sys.platform == 'win32':
		wx.Locale.AddCatalogLookupPathPrefix(config.locales_dir)
		wxloc = wx.Locale(wx.LANGUAGE_DEFAULT)
		wxloc.AddCatalog('wxstd')
	iconprovider.init_icon_cache(None, config.data_dir)
	main_frame = FrameMain(filename)
	app.SetTopWindow(main_frame.wnd)
	main_frame.wnd.Show()
	app.MainLoop()
	config.save()


def run(filename, filters):
	_LOG.info('Run %s --- %s ---->', filename, filters)
	try:
		image = PILImage.open(filename)
		image.load()
	except Exception, err:
		_LOG.warn('Error loading file %s: %s', filename, str(err))
		print >> sys.stderr, 'Error loading file %s: %s' % (filename, str(err))
		return
	widx = 1
	fname, fext = os.path.splitext(filename)
	fname = os.path.basename(fname)
	for filter_name in filters.split(','):
		filterm = get_filter(filter_name)
		for idx, (msg, image) in enumerate(filterm.process(image)):
			idx += 1
			_LOG.debug('  %d: %s', idx, msg)
			if _OPTIONS.debug_scripts:
				odeb = '%s_%02d_%s_%02d' % (fname, widx, filter_name, idx)
				if _OPTIONS.output:
					odeb = os.path.join(_OPTIONS.output, odeb)
				if _OPTIONS.postfix:
					odeb += _OPTIONS.postfix
				image.save(odeb + fext, "JPEG", quality=100)
			widx += 1
	if _OPTIONS.postfix:
		fname += _OPTIONS.postfix
	elif not _OPTIONS.output:
		fname += "_pm"
	out_name = fname + fext
	if _OPTIONS.output:
		out_name = os.path.join(_OPTIONS.output, out_name)
	_LOG.info('    -----> %s', out_name)
	try:
		image.save(out_name, "JPEG", quality=100)
	except Exception, err:
		_LOG.warn('Error saving file %s: %s', out_name, str(err))
		print >> sys.stderr, 'Error saving file %s: %s' % (out_name, str(err))
		return


def main():
	config = appconfig.AppConfig()
	config.load_defaults(config.get_data_file('defaults.cfg'))
	config.load()
	config.debug = _OPTIONS.debug
	config['debug_scripts'] = _OPTIONS.debug_scripts
	filters.load_filters()

	if _OPTIONS.list_filter_names:
		for filter_name, _fmodule in sorted(filters.MODULES.iteritems()):
			print filter_name
		exit(0)

	if _OPTIONS.list_filters:
		print 'Filters:'
		for filter_name, fmodule in sorted(filters.MODULES.iteritems()):
			print ' - %s: %s' % (filter_name, filters.get_filter_name(fmodule))
		exit(0)

	random.seed()
	filenames = list(itertools.chain(*(glob.glob(fname) for fname in _ARGS)))
	if _OPTIONS.batch:
		for filename in filenames:
			run(filename, _OPTIONS.filter)
	else:
		if filenames:
			run_gui(filenames)
		else:
			run_gui(None)
