#!usr/bin/python
# -*- coding: utf-8 -*-

__plugins__ = ('TiltShift', )
__version__ = '2011-03-20'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2011"

import Image
import ImageFilter
import ImageEnhance

from photomagick.common import gradients
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_SIMPLE


class TiltShift(BaseFilter):
	NAME = _('Tilt-Shift')
	STEPS = 7
	CATEGORY = CATEGORY_SIMPLE

	def process(self, image):
		yield 'Sharpness...', image
		image = ImageEnhance.Sharpness(image).enhance(1.5)
		yield 'Contrast...', image
		image = ImageEnhance.Contrast(image).enhance(1.5)
		yield 'Color...', image
		image = ImageEnhance.Color(image).enhance(1.5)
		yield 'Gradient...', image
		gradient = gradients.create_gradient(image, 1.1, 1.0)
		yield 'Smoth...', gradient
		blur = image.filter(ImageFilter.GaussianBlur(10.))
		blur = blur.filter(ImageFilter.GaussianBlur(5.))
		yield 'Apply Smoth...', blur
		gradient = gradient.convert("L")
		image = Image.composite(image, blur, gradient)
		yield 'Done', image
