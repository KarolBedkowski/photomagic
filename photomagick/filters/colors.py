#!usr/bin/python
# -*- coding: utf-8 -*-

__plugins__ = ('ColorBlue', 'ColorPurple', 'ColorRed',
		'ColorCyano', 'ColorPalladium', 'ColorSelenium', 'ColorSilver',
		'Desaturated', 'SunnyDay', 'BwAndRed')
__version__ = '2011-03-20'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2011"

import Image
import ImageEnhance
import ImageChops

from photomagick.common import colors
from photomagick.common import curves
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_BASE


class _ColorsHue(BaseFilter):
	STEPS = 3
	NAME = _('Colors')
	CATEGORY = CATEGORY_BASE
	_HUE = 0

	def process(self, image):
		yield 'Start...', image
		image = colors.convert_to_luminosity(image)
		yield 'Convert...', image
		image = colors.colorize_hls(image, (self._HUE, 0, 0.25))
		yield 'Done', image


class ColorBlue(_ColorsHue):
	NAME = _('Colors Blue')
	_HUE = 0.55


class ColorPurple(_ColorsHue):
	NAME = _('Colors Purple')
	_HUE = 0.7


class ColorRed(_ColorsHue):
	NAME = _('Colors Red')
	_HUE = 1


class _ColorsRGB(BaseFilter):
	STEPS = 3
	NAME = _('Colors')
	CATEGORY = CATEGORY_BASE
	_RGB = 0

	def process(self, image):
		yield 'Start...', image
		image = colors.convert_to_luminosity(image)
		yield 'Convert...', image
		image = colors.colorize(image, self._RGB)
		yield 'Done', image


class ColorCyano(_ColorsRGB):
	NAME = _('Colors Cyano')
	_RGB = (68, 174, 246)


class ColorPalladium(_ColorsRGB):
	NAME = _('Colors Palladium')
	_RGB = (143, 153, 69)


class ColorSelenium(_ColorsRGB):
	NAME = _('Colors Selenium')
	_RGB = (158, 79, 104)


class ColorSilver(_ColorsRGB):
	NAME = _('Colors Silver')
	_RGB = (92, 154, 154)


class Desaturated(BaseFilter):
	NAME = _('Desaturated')
	STEPS = 2
	CATEGORY = CATEGORY_BASE

	def process(self, image):
		yield 'Color...', image
		image = ImageEnhance.Color(image).enhance(0.7)
		yield 'Done', image


class SunnyDay(BaseFilter):
	NAME = _('Sunny Day')
	STEPS = 2
	CATEGORY = CATEGORY_BASE

	def process(self, image):
		yield 'Color...', image
#		image = colors.apply_color(image, (255, 255, 0), 0.2)
		bredgreen = list(curves.create_curve([(0, 0), (192, 200), (255, 255)]))
		bblue = list(curves.create_curve([(0, 0), (96, 64), (255, 255)]))
		image = curves.apply_curves(image, None, bredgreen, bredgreen, bblue)
		yield 'Done', image


class BwAndRed(BaseFilter):
	NAME = _('BW and Red')
	STEPS = 4
	CATEGORY = CATEGORY_BASE

	def process(self, image):
		yield 'Mask', image
		mask = image.convert("L", [2, -1, -1, 0]).convert("RGB")
		source = list(mask.split())
		maxv = int(source[0].getextrema()[1] * 0.99)
		source[0] = source[0].point(lambda i: i > maxv and 255 or 0)
		mask = Image.merge("RGB", tuple(source)).convert("L")
		yield 'Desaturate', mask
		bw_lay = colors.convert_to_luminosity(image)
		yield 'Merge', bw_lay
		image = ImageChops.composite(image, bw_lay, mask)
		yield 'Done', image
