#!usr/bin/python
# -*- coding: utf-8 -*-

__plugins__ = ('Techicolor3', )
__version__ = '2011-03-20'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2011"

import ImageEnhance
import ImageChops

from photomagick.common import colors
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_SIMPLE


class Techicolor3(BaseFilter):
	NAME = _('Techicolor 3')
	STEPS = 9
	CATEGORY = CATEGORY_SIMPLE

	def process(self, image):
		red = 1.2
		green = 1.2
		blue = 1.2
		red_r = red
		red_g = (1. - red) / 2.
		red_b = (1. - red) / 2.
		green_r = (1. - green) / 2.
		green_g = green
		green_b = 1. - green
		blue_r = (1. - blue) / 2.
		blue_g = (1. - blue) / 2.
		blue_b = blue
		yield 'Red layer', image
		redlayer = image.copy()
		redlayer = colors.color_mixer_monochrome(redlayer, red_r, red_g, red_b)
		redlayer = ImageChops.invert(redlayer)
		redlayer = colors.apply_color(redlayer, (255, 0, 0))
		redlayer = ImageChops.invert(redlayer)
		yield 'Green layer', redlayer
		greenlayer = image.copy()
		greenlayer = colors.color_mixer_monochrome(greenlayer, green_r, green_g,
				green_b)
		greenlayer = ImageChops.invert(greenlayer)
		greenlayer = colors.apply_color(greenlayer, (0, 255, 0))
		greenlayer = ImageChops.invert(greenlayer)
		yield 'Blue layer', redlayer
		bluelayer = image.copy()
		bluelayer = colors.color_mixer_monochrome(bluelayer, blue_r, blue_g, blue_b)
		bluelayer = ImageChops.invert(bluelayer)
		bluelayer = colors.apply_color(bluelayer, (0, 0, 255))
		bluelayer = ImageChops.invert(bluelayer)
		yield 'Red + green...', bluelayer
		image = ImageChops.multiply(greenlayer, redlayer)
		yield '+ blue...', image
		image = ImageChops.multiply(image, bluelayer)
		yield 'Contrast...', image
		image = ImageEnhance.Contrast(image).enhance(1.1)
		yield 'Sharpness...', image
		image = ImageEnhance.Sharpness(image).enhance(1.1)
		yield 'Color...', image
		image = ImageEnhance.Color(image).enhance(1.2)
		yield 'Done', image
