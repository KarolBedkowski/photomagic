#!usr/bin/python
# -*- coding: utf-8 -*-

__plugins__ = ('Video', )
__version__ = '2011-03-20'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2011"

import Image
import ImageFilter
import ImageEnhance
import ImageDraw
import ImageChops

from photomagick.common import curves
from photomagick.common import vignette
from photomagick.common import colors
from photomagick.common import gradients
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_BASE


class Video(BaseFilter):
	NAME = _('Video')
	STEPS = 8
	CATEGORY = CATEGORY_BASE

	def process(self, image):
		yield 'Color...', image
		image = ImageEnhance.Color(image).enhance(0.5)
		yield 'Curves...', image
		bcurv = list(curves.create_curve([(0, 0), (90, 20), (140, 80), (200, 206),
				(255, 255)]))
		image = curves.apply_curves(image, bcurv)
		yield 'Smoth...', image
		blur = image.filter(ImageFilter.BLUR)
		yield 'Merge smoth...', blur
		gradient = gradients.create_gradient(image, 1.2, 1.4)
		mask = gradient.convert("L")
		mask = ImageEnhance.Brightness(mask).enhance(2.0)
		image = Image.composite(image, blur, mask)
		yield 'vignette...', image
		image = vignette.vignette(image)
		yield 'Color...', image
		cyanlayer = image.copy()
		colors.fill_with_color(cyanlayer, (230, 255, 255))
		image = ImageChops.multiply(image, cyanlayer)
		yield 'Aspect...', image
		width, height = image.size
		if width > height:
			dheight = int(width / 16. * 9)
			margin = (height - dheight) / 2
			if margin > 0:
				draw = ImageDraw.Draw(image)
				draw.rectangle((0, 0, width, margin), fill=0)
				draw.rectangle((0, height, width, height - margin), fill=0)
			del draw
		#image = ImageEnhance.Sharpness(image).enhance(1.1)
		#image = ImageEnhance.Brightness(image).enhance(1.2)
		yield 'Done', image
