#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Karol Będkowski"
__copyright__ = "Copyright (c) Karol Będkowski, 2011"
__version__ = "2011-04-24"


import wx
import Image


def pilimage2wximage(img, set_alpha=True):
	wximg = wx.EmptyImage(*img.size)
	wximg.SetData(img.convert('RGB').tostring())
	if set_alpha and img.mode.endswith('A'):
		wximg.SetAlphaData(img.tostring()[3::4])
	return wximg


def wximage2pilimage(wximg):
	pimg = Image.new('RGB', (wximg.GetWidth(), wximg.GetHeight()))
	pimg.fromstring(wximg.GetData())
	return pimg
