#!/usr/bin/python2.4
# -*- coding: utf-8 -*-
"""
Logging setup.

2008-04-17 [k]: umieszczanie loga w tempie jeżeli jest frozen lub wybrany
katalog jest ro.
"""
__author__ = "Karol Będkowski"
__copyright__ = "Copyright (c) Karol Będkowski, 2006-2010"
__version__ = "2011-04-24"

__all__ = ['logging_setup']


import os.path
import logging
import tempfile
import time

from . import appconfig


def logging_setup(filename, debug=False):

	log_fullpath = os.path.abspath(filename)
	log_dir = os.path.dirname(log_fullpath)
	log_dir_access = os.access(log_dir, os.W_OK)

	create_temp = False
	if os.path.isabs(filename):
		if not log_dir_access:
			create_temp = True
	else:
		if appconfig.is_frozen() or not log_dir_access:
			create_temp = True

	if create_temp:
		basename = os.path.basename(filename)
		spfname = os.path.splitext(basename)
		filename = spfname[0] + "_" + str(int(time.time())) + spfname[1]
		log_fullpath = os.path.join(tempfile.gettempdir(), filename)

	print 'Logging to %s' % log_fullpath

	if debug:
		level_console = logging.DEBUG
		level_file = logging.DEBUG
	else:
		level_console = logging.INFO
		level_file = logging.ERROR

	logging.basicConfig(level=level_file,
			format='%(asctime)s %(levelname)-8s %(name)s - %(message)s',
			filename=log_fullpath, filemode='w')
	console = logging.StreamHandler()
	console.setLevel(level_console)

	console.setFormatter(logging.Formatter(
			'%(levelname)-8s %(name)s - %(message)s'))
	logging.getLogger('').addHandler(console)

	logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
	logging.getLogger('sqlalchemy.orm.unitofwork').setLevel(logging.WARN)

	log = logging.getLogger(__name__)
	log.debug('logging_setup() finished')


# vim: ff=unix: encoding=utf8:
