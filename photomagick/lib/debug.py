# -*- coding: UTF-8 -*-

__author__ = "Karol Będkowski"
__copyright__ = "Copyright (c) Karol Będkowski, 2009-2011"
__version__ = "2011-04-24"

from contextlib import contextmanager
import time
import logging
from functools import wraps

_LOG = logging.getLogger(__name__)


if __debug__:

	@contextmanager
	def time_it(name):
		_ts = time.time()
		yield
		_LOG.debug('%s: %0.4f', name, time.time() - _ts)
else:

	@contextmanager
	def time_it(name):
		yield


if __debug__:

	def time_method(func):
		@wraps(func)
		def wrapper(*args, **kwds):
			_ts = time.time()
			res = func(*args, **kwds)
			_LOG.debug('%s.%s: %0.4f', func.__module__, func.__name__,
					time.time() - _ts)
			return res
		return wrapper
else:

	def time_method(func):
		return func


if __debug__:

	def log(func):
		@wraps(func)
		def wrapper(*args, **kwds):
			_LOG.debug('%s.%s: (%r) {%r}', func.__module__, func.__name__,
					repr(args), repr(kwds))
			return func(*args, **kwds)
		return wrapper

else:

	def log(func):
		return func
