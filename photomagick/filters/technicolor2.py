#!usr/bin/python
# -*- coding: utf-8 -*-

__plugins__ = ('Techicolor2', )
__version__ = '2011-03-20'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2011"

import ImageEnhance
import ImageChops

from photomagick.common import colors
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_BASE


class Techicolor2(BaseFilter):
	NAME = _('Techicolor 2')
	STEPS = 7
	CATEGORY = CATEGORY_BASE

	def process(self, image):
		red = 1.0  # (0.1 - 1.0)
		green = 0.5  # (0.1 - 0.5)
		red_r = red
		red_g = (1. - red) / 2.
		red_b = (1. - red) / 2.
		cyan_r = 0
		cyan_g = green
		cyan_b = 1. - green
		yield 'Red layer', image
		redlayer = image.copy()
		redlayer = colors.color_mixer_monochrome(redlayer, red_r, red_g, red_b)
		redlayer = ImageChops.invert(redlayer)
		redlayer = colors.apply_color(redlayer, (255, 0, 0))
		redlayer = ImageChops.invert(redlayer)
		yield 'Cyan layer', redlayer
		cyanlayer = image.copy()
		cyanlayer = colors.color_mixer_monochrome(cyanlayer, cyan_r, cyan_g, cyan_b)
		cyanlayer = ImageChops.invert(cyanlayer)
		cyanlayer = colors.apply_color(cyanlayer, (0, 255, 255))
		cyanlayer = ImageChops.invert(cyanlayer)
		yield 'Cyan + Red...', cyanlayer
		image = ImageChops.multiply(cyanlayer, redlayer)
		yield 'Yellow layer', image
		yellowlayer = image.copy()
		colors.fill_with_color(yellowlayer, (255, 255, 240))
		image = ImageChops.multiply(image, yellowlayer)
		yield 'Contrast...', image
		image = ImageEnhance.Contrast(image).enhance(1.1)
		yield 'Sharpness...', image
		image = ImageEnhance.Sharpness(image).enhance(1.1)
		yield 'Done', image
