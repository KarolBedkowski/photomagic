#!usr/bin/python
# -*- coding: utf-8 -*-

__plugins__ = ('YellowGreen', )
__version__ = '2011-03-20'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2011"

import Image
import ImageEnhance
import ImageChops

from photomagick.common import colors
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_SIMPLE


class YellowGreen(BaseFilter):
	NAME = _('Yellow-Green')
	STEPS = 5
	CATEGORY = CATEGORY_SIMPLE

	def process(self, image):
		yield 'Cyan Layer...', image
		cyanlayer = image.copy()
		cyanlayer_bw = colors.convert_to_luminosity(cyanlayer)
		cyanlayer = colors.colorize(cyanlayer_bw, (0, 255, 0))
		cyanlayer = ImageEnhance.Brightness(cyanlayer).enhance(1.1)
		yield 'Orange Layer...', cyanlayer
		orangelayer = image.copy()
		orangelayer_bw = colors.convert_to_luminosity(orangelayer)
		orangelayer = colors.colorize(orangelayer_bw, (255, 255, 0))
		orangelayer = ImageEnhance.Brightness(orangelayer).enhance(1.2)
		yield 'Merge cyan...', orangelayer
		cyanlayer_bw = cyanlayer_bw.convert("L")
		cyanlayer_bw = ImageEnhance.Brightness(cyanlayer_bw).enhance(2.0)
		image = Image.composite(image, cyanlayer, cyanlayer_bw)
		yield 'Merge orange...', image
		orangelayer_bw = ImageChops.invert(orangelayer_bw)
		orangelayer_bw = orangelayer_bw.convert("L")
		orangelayer_bw = ImageEnhance.Brightness(orangelayer_bw).enhance(0.6)
		image = Image.composite(image, orangelayer, orangelayer_bw)
		yield 'Done', image
