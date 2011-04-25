#!usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Karol Będkowski"
__copyright__ = "Copyright (c) Karol Będkowski, 2011"
__version__ = "2011-04-24"


class BaseFilter(object):
	STEPS = 99
	NAME = ""
	CATEGORY = None

	def __init__(self):
		pass

	def process(self, image):
		return image
