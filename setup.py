#!/usr/bin/python
# -*- coding: utf8 -*-

import os
import os.path
import time
import sys
import glob

from distutils.core import setup, Extension
from distutils.cmd import Command
import distutils.command.clean
distutilsextra = False
try:
	from DistUtilsExtra.command import *
	distutilsextra = True
except ImportError:
	pass

import wx

if sys.platform == 'win32':
	try:
		import py2exe
	except:
		pass

from photomagick import version, configuration

build = time.asctime()


def packages_for(filename, basePackage=""):
	"""Find all packages in filename"""
	packages = {}
	for item in os.listdir(filename):
		dirname = os.path.join(filename, item)
		if os.path.isdir(dirname) and os.path.isfile(os.path.join(\
				dirname, '__init__.py')):
			if basePackage:
				moduleName = basePackage + '.' + item
			else:
				moduleName = item
			packages[moduleName] = dirname
			packages.update(packages_for(dirname, moduleName))
	return packages


def find_files(directory, base):
	for name, subdirs, files in os.walk(directory):
		if files:
			yield (os.path.join(base[:-len(directory)], name), \
					[os.path.join(name, fname) for fname in files])


packages = packages_for(".")


def get_data_files():
	if sys.platform == 'win32':
		doc_dir = '.'
		locales_dir = configuration.LOCALES_DIR
		data_dir = configuration.DATA_DIR
	else:
		doc_dir = configuration.LINUX_DOC_DIR
		locales_dir = configuration.LINUX_LOCALES_DIR
		data_dir = configuration.LINUX_DATA_DIR
	yield (doc_dir, ['AUTHORS', 'README', "TODO", "COPYING", 'ChangeLog'])
	# data
	yield (data_dir, glob.glob('data/*.png'))
	yield (data_dir, glob.glob('data/*.xrc'))
	yield (data_dir, glob.glob('data/*.ico'))
	if 'py2exe' not in sys.argv:
		yield (data_dir, glob.glob('data/*.svg'))
		yield (data_dir, glob.glob('data/*.wxg'))
		yield (data_dir, glob.glob('data/*.xcf'))
	yield (os.path.join(data_dir, 'coffee'), glob.glob('data/coffee/*.*'))
	# locales
	for x in find_files('locale', locales_dir):
		yield x
	if 'py2exe' in sys.argv:
		for loc in glob.iglob('locale/*'):
			yield (os.path.join(locales_dir, loc, 'LC_MESSAGES'),
					[os.path.join(os.path.dirname(wx.__file__), loc,
					'LC_MESSAGES', 'wxstd.mo')])


#print list(get_data_files())


def _delete_dir(path):
	if os.path.exists(path):
		for root, dirs, files in os.walk(path, topdown=False):
			for name in files:
				filename = os.path.join(root, name)
				print 'Delete ', filename
				try:
					os.remove(filename)
				except Exception, err:
					print err
			for name in dirs:
				filename = os.path.join(root, name)
				print 'Delete dir ', filename
				try:
					os.rmdir(filename)
				except Exception, err:
					print err
		os.removedirs(path)


class CleanupCmd(distutils.command.clean.clean):
	description = "cleanup all files"

	def run(self):
		for root, dirs, files in os.walk('.', topdown=False):
			for name in files:
				nameext = os.path.splitext(name)[-1]
				if (name.endswith('~') or name.startswith('profile_result_')
						or name.endswith('-stamp')
						or nameext in ('.pyd', '.pyc', '.pyo', '.log', '.tmp',
							'.swp', '.db', '.cfg', '.debhelper', '.substvars',
							'.orig', '.so', '.pyd')):
					if name == 'defaults.cfg':
						continue
					if name == 'setup.cfg':
						continue
					filename = os.path.join(root, name)
					print 'Delete ', filename
					try:
						os.remove(filename)
					except Exception, err:
						print err
		_delete_dir('build')
		_delete_dir('locales')
		_delete_dir('debian/photomagick')
		if os.path.exists('hotshot_edi_stats'):
			os.remove('hotshot_edi_stats')
		if os.path.exists('photomagick/filters/_plugin_list.py'):
			os.remove('photomagick/filters/_plugin_list.py')
		distutils.command.clean.clean.run(self)


class UpdatePotfilesCommand(Command):
	"""docstring for cleanup"""

	description = "update POTFILEs.in"
	user_options = []

	def initialize_options(self):
		pass

	def finalize_options(self):
		pass

	def run(self):
		potfiles = open('po/POTFILES.in', 'wt')
		for line in self._find_files():
			potfiles.write(line + '\n')
		potfiles.close()

	def _find_files(self):
		for root, dirs, files in os.walk('.'):
			if root == '.':
				for name in files:
					if name.endswith('.desktop.in'):
						filename = os.path.join(root, name)[2:]
						yield filename
			if not (root.startswith('./photomagick') or \
					root.startswith('./data')):
				continue
			for name in files:
				nameext = os.path.splitext(name)[-1]
				filename = os.path.join(root, name)[2:]
				if nameext == '.xrc':
					yield '[type: gettext/glade] ' + filename
				elif nameext == '.py':
					yield filename


class MakeMoCommand(Command):
	"""docstring for cleanup"""

	description = "create mo files"
	user_options = []

	def initialize_options(self):
		pass

	def finalize_options(self):
		pass

	def run(self):
		for filename in os.listdir('po'):
			if not filename.endswith('.po'):
				continue
			lang = filename[:-3]
			print 'creating mo for', lang
			path = os.path.join('locale', lang, 'LC_MESSAGES')
			if not os.path.exists(path):
				os.makedirs(path)
			os.execlp('msgfmt', 'msgfmt', 'po/%s.po' % lang,
					'-o', os.path.join(path, '%s.mo' % version.SHORTNAME))


class MakeManCommand(Command):
	"""docstring for cleanup"""

	description = "create manpages"
	user_options = []

	def initialize_options(self):
		pass

	def finalize_options(self):
		pass

	def run(self):
		for rst in (filename[:-4] for filename in os.listdir('man')
				if filename.endswith('.rst')):
			print 'creating manpage', rst
			os.execlp('rst2man', 'rst2man', 'man/%s.rst' % rst, 'man/%s.1' % rst)


def _create_plugin_list():
	# wymagane przez py2exe
	plistf = open('photomagick/filters/_plugin_list.py', 'wt')
	plistf.write('PLUGINS = []\n\n')
	for name in os.listdir('photomagick/filters'):
		if name.startswith('_') or not name.endswith('.py'):
			continue
		mod = os.path.splitext(name)[0]
		print mod
		plistf.write('import %s\n' % mod)
		plistf.write('PLUGINS.append(%s)\n' % mod)
	plistf.close()


class MakePluginListCommand(Command):
	description = "create plugin list for py2exe"
	user_options = []

	def initialize_options(self):
		pass

	def finalize_options(self):
		pass

	def run(self):
		_create_plugin_list()


cmdclass = {'clean': CleanupCmd,
		'make_mo': MakeMoCommand,
		'make_man': MakeManCommand,
		'update_potfiles': UpdatePotfilesCommand,
		'create_plugin_list': MakePluginListCommand,
}
if 'py2exe' not in sys.argv and distutilsextra:
	cmdclass.update({
			"build": build_extra.build_extra,
			"build_i18n": build_i18n.build_i18n,
			"build_help": build_help.build_help,
			"build_icons": build_icons.build_icons,
	})


target = {
	'script': "photomagick_dbg.py",
	'name': "photomagick_dbg",
	'version': version.VERSION,
	'description': "%s - %s (%s, build: %s)" \
			% (version.NAME, version.DESCRIPTION, version.RELEASE, build),
	'company_name': "Karol Będkowski",
	'copyright': version.COPYRIGHT,
	'icon_resources': [(0, "data/photomagick.ico")],
	'other_resources': [("VERSIONTAG", 1, build)],
}


target_win = target.copy()
target_win.update({'script': "photomagick.pyw", 'name': "photomagick"})


if 'py2exe' in sys.argv:
	_create_plugin_list()


modules_support = [
		Extension('photomagick.support._layers',
			sources=['support/layers.c', 'support/common.c']),
		Extension('photomagick.support._colors',
			sources=['support/colors.c', 'support/common.c']),
		Extension('photomagick.support._gradients',
				sources=['support/gradients.c', 'support/common.c']),
]


options = {}
if not 'py2exe' in sys.argv and distutilsextra:
	options['build'] = {
			'i18n': True,
			'icons': True,
	}


setup(
	name='photomagick',
	version=version.VERSION,
	author=target['company_name'],
	author_email='karol.bedkowski@gmail.com',
	description=target['description'],
	long_description='-',
	license='GPL v2',
	url='-',
	download_url='-',
	classifiers=[
		'Development Status :: 4 - Beta',
		'Environment :: Win32 (MS Windows)',
		'Environment :: X11 Applications',
		'License :: OSI Approved :: GNU General Public License (GPL)',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: Database :: Desktop',
	],
	packages=packages.keys(),
	package_dir=packages,
	data_files=list(get_data_files()),
	scripts=['photomagick.pyw', 'photomagick_dbg.py'],
	options=options,
	zipfile=r"modules.dat",
	windows=[target_win],
	console=[target],
	cmdclass=cmdclass,
	ext_modules=modules_support,
)
