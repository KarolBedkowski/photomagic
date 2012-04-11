#!usr/bin/python
# -*- coding: utf-8 -*-

__plugins__ = ('SepiaBrown', 'SepiaGrey', 'SepiaRed', 'SepiaYellow')
__version__ = '2011-03-20'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2011"

from photomagick.common import colors
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_SIMPLE


class _ColorsRGB(BaseFilter):
	STEPS = 3
	NAME = 'Colors'
	CATEGORY = CATEGORY_SIMPLE
	_RGB = 0

	def process(self, image):
		yield 'Start...', image
		image = colors.convert_to_luminosity(image)
		yield 'Convert...', image
		image = colors.colorize(image, self._RGB)
		yield 'Done', image


class SepiaBrown(_ColorsRGB):
	NAME = _('Sepia Brown')
	_RGB = (162, 127, 92)


class SepiaGrey(_ColorsRGB):
	NAME = _('Sepia Grey')
	_RGB = (162, 138, 101)


class SepiaRed(_ColorsRGB):
	NAME = _('Sepia Red')
	_RGB = (184, 110, 55)


class SepiaYellow(_ColorsRGB):
	NAME = _('Sepia Yellow')
	_RGB = (181, 127, 52)
