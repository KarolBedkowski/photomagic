#!usr/bin/python
# -*- coding: utf-8 -*-

__plugins__ = ('Lomo', )
__version__ = '2011-03-20'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2011"

import Image
import ImageFilter
import ImageEnhance

from photomagick.common import curves
from photomagick.common import vignette
from photomagick.common import gradients
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_SIMPLE


class Lomo(BaseFilter):
	NAME = _('Lomo')
	STEPS = 9
	CATEGORY = CATEGORY_SIMPLE

	def process(self, image):
#		yield 'Contrast...', image
#		image = ImageEnhance.Contrast(image).enhance(1.1)
		yield 'Color...', image
		image = ImageEnhance.Color(image).enhance(1.2)
		yield 'Sharpness...', image
		image = ImageEnhance.Sharpness(image).enhance(1.1)
		yield 'Brightness...', image
		image = ImageEnhance.Brightness(image).enhance(1.2)
		yield 'Curves...', image
		bcurv = list(curves.create_curve([(0, 0), (64, 50), (128, 128), (192, 206),
				(255, 255)]))
		bblue = list(curves.create_curve([(0, 0), (64, 90), (128, 128), (192, 164),
				(255, 255)]))
		image = curves.apply_curves(image, bcurv, bcurv, bcurv, bblue)
		yield 'vignette...', image
		image = vignette.vignette(image)
		yield 'Gradient...', image
		gradient = gradients.create_circular_gradient(image.size, 1.0, circle=False,
				offset=1.2)
		yield 'Smoth...', gradient
		blur = image.filter(ImageFilter.SMOOTH)
		yield 'Apply Smoth...', blur
		gradient = gradient.convert("L")
		image = Image.composite(image, blur, gradient)

		#curves.draw_curve(image, bcurv, 100, 100, (255, 255, 255))
		#curves.draw_curve(image, bblue, 100, 700, (0, 0, 255))

		yield 'Done', image
