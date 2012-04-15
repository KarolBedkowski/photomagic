#!usr/bin/python
# -*- coding: utf-8 -*-

__plugins__ = ('Lomo', 'Lomo2', 'Lomo3')
__version__ = '2012-04-15'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2011-2012"

import Image
import ImageFilter
import ImageEnhance
import ImageChops

from photomagick.common import colors
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


class Lomo2(BaseFilter):
	NAME = _('Lomo 2')
	STEPS = 4
	CATEGORY = CATEGORY_SIMPLE

	def process(self, image):
		yield 'Color...', image
		image = ImageEnhance.Color(image).enhance(1.3)
		yield 'Color balance...', image
		color = colors.fill_with_color(image.copy(), (50, 50, 0))
		yield 'Merge', color
		image = ImageChops.add(image, color, 1.3)
		yield 'Curves...', image
		rgcurv = list(curves.create_curve(
				[(0, 0), (32, 0), (64, 11), (128, 111), (192, 241), (224, 255),
				(240, 255), (255, 255)]
		))
		bcurv = curves.create_line([(0, 62), (36, 62), (218, 191), (255, 191)])
		image = curves.apply_curves(image, None, rgcurv, rgcurv, bcurv)
#		curves.draw_curve(image, rgcurv, 10, 10, (255, 255, 255))
#		curves.draw_curve(image, bcurv, 10, 300, (0, 0, 255))
		yield 'Done', image


class Lomo3(BaseFilter):
	NAME = _('Lomo 3')
	STEPS = 3
	CATEGORY = CATEGORY_SIMPLE

	def process(self, image):
		yield 'Curves...', image
		rcurv = list(curves.create_curve(
			[(0, 0), (32, 17), (64, 53), (128, 174), (192, 233), (224, 247),
				(255, 255)]
		))
		gcurv = list(curves.create_curve(
			[(0, 0), (32, 21), (64, 48), (128, 143), (192, 218), (224, 239),
				(255, 255)]
		))
		bcurv = list(curves.create_curve(
			[(0, 0), (32, 34), (64, 66), (128, 118), (192, 181), (224, 218),
				(255, 255)]
		))
		image = curves.apply_curves(image, None, rcurv, gcurv, bcurv)
		yield 'Contrast...', image
		image = ImageEnhance.Contrast(image).enhance(1.2)
#		curves.draw_curve(image, rcurv, 10, 10, (255, 0, 0))
#		curves.draw_curve(image, bcurv, 10, 300, (0, 0, 255))
#		curves.draw_curve(image, gcurv, 300, 10, (0, 255, 0))
		yield 'Done', image
