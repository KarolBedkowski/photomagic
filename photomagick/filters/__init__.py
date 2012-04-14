#!usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Karol Będkowski"
__copyright__ = "Copyright (c) Karol Będkowski, 2011"
__version__ = "2011-04-24"

import sys
import os
import pkgutil
import logging

_LOG = logging.getLogger(__name__)
MODULES = {}

from photomagick.common import const
from photomagick.common.base_filter import BaseFilter


def load_filters():
	if MODULES:
		return
	_LOG.info('Loading modules...')
	from photomagick.lib import appconfig
	if appconfig.is_frozen():
		try:
			import _plugin_list
		except ImportError:
			pass
	aconf = appconfig.AppConfig()
	_LOG.info('Loading filters...')
	_LOG.debug('Searching for filters - photomagick...')
	for modname, _ispkg in pkgutil.ImpImporter(__path__[0]).iter_modules():
		if modname.startswith('_') or modname.endswith('_support'):
			continue
		if (modname.startswith('test_') or modname.endswith('_test')) and \
			not aconf.debug:
				continue
		_LOG.debug('Loading module %s', modname)
		try:
			__import__('photomagick.filters.' + modname, fromlist=[modname])
		except ImportError:
			_LOG.exception("Load module %s error", modname)

	user_filters_path = os.path.join(aconf.user_share_dir, 'filters')
	_LOG.debug('Searching for filters - user dir: %s', user_filters_path)
	if os.path.isdir(user_filters_path):
		init_file = os.path.join(user_filters_path, '__init__.py')
		if not os.path.exists(init_file):
			try:
				file(init_file, 'wt').close()
			except IOError:
				_LOG.exception("Creating missing __init__.py file failed")
		sys.path.append(aconf.user_share_dir)
		for modname, _ispkg in pkgutil.ImpImporter(user_filters_path).iter_modules():
			if modname.startswith('_') or modname.endswith('_support'):
				continue
			if (modname.startswith('test_') or modname.endswith('_test')) and \
				not aconf.debug:
					continue
			_LOG.debug('Loading module %s', modname)
			try:
				__import__('filters.' + modname, fromlist=[modname])
			except ImportError:
				_LOG.exception("Load module %s error", modname)
	_LOG.debug('Loading filters...')
	base = BaseFilter()
	_load_filters_from_subclass(base, aconf)
	_LOG.info('Modules (%d): %s', len(MODULES), ', '.join(sorted(MODULES.keys())))


def _load_filters_from_subclass(base, aconf):
	_LOG.debug('_load_filters_from_subclass(%s.%s)', base.__class__.__module__,
			base.__class__.__name__)
	for filter_class in base.__class__.__subclasses__():
		if hasattr(filter_class, 'DISABLED'):
			continue
		name = filter_class.__name__
		module = filter_class.__module__
		if not aconf.debug and (name.startswith('Test') or \
				module.endswith('_test') or module.endswith('_support')):
			continue
		_LOG.debug(' loading %s from %s', name, module)
		try:
			filter_obj = filter_class()
			if name and not name.startswith('_'):
				name = name.lower()
				if name in MODULES:
					name = module + '.' + name
				MODULES[name] = filter_obj
		except:
			_LOG.exception('Loading %s from %s error', name, module)
		else:
			_load_filters_from_subclass(filter_obj, aconf)


def get_filter_name(module):
	if hasattr(module, '__plugin_name__'):
		return getattr(module, '__plugin_name__')
	elif hasattr(module, 'NAME'):
		return getattr(module, 'NAME')
	return module.__name__


def get_filter_category(module):
	if hasattr(module, 'CATEGORY'):
		return getattr(module, 'CATEGORY')
	return const.CATEGORY_SIMPLE
