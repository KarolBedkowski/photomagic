#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Karol Będkowski"
__copyright__ = "Copyright (c) Karol Będkowski, 2011"
__version__ = "2011-04-24"


from contextlib import contextmanager
from functools import wraps

import wx


@contextmanager
def with_wait_cursor():
	wx.SetCursor(wx.HOURGLASS_CURSOR)
	try:
		yield
	finally:
		wx.SetCursor(wx.STANDARD_CURSOR)


def call_after(func):

	@wraps(func)
	def wrapper(*args, **kwds):
		if wx.Thread_IsMain():
			return func(*args, **kwds)
		wx.CallAfter(func, *args, **kwds)
	return wrapper


@contextmanager
def with_freeze(*windows):
	""" Wyłaczenie odświerzania okna """
	for win in windows:
		win.Freeze()
	try:
		yield
	finally:
		for win in windows:
			win.Thaw()
