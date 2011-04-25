#!usr/bin/python
# -*- coding: utf-8 -*-

__plugins__ = ('ModBlurred', )
__version__ = '2011-03-20'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2011"

import Image
import ImageFilter
import ImageChops
import ImageEnhance

from photomagick.lib import appconfig
from photomagick.common import gradients
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_MODIFICATOR


class ModBlurred(BaseFilter):
	STEPS = 4
	NAME = _('Blurred')
	CATEGORY = CATEGORY_MODIFICATOR

	def process(self, image):
		yield 'Gradient...', image
		gradient = gradients.create_gradient(image, 2.0, 1.0)
		yield 'Smoth...', gradient
		blur = image.filter(ImageFilter.BLUR)
		yield 'Apply Smoth...', blur
		gradient = gradient.convert("L")
		image = Image.composite(image, blur, gradient)
		yield 'Done', image


class ModFog(BaseFilter):
	STEPS = 4
	NAME = _('Fog')
	CATEGORY = CATEGORY_MODIFICATOR
	_IMAGE = 'fog.png'

	def process(self, image):
		yield 'Loading...', image
		imgp = appconfig.AppConfig().get_data_file(self._IMAGE)
		img = Image.open(imgp)
		img = ImageEnhance.Contrast(img).enhance(0.7)
		img = ImageEnhance.Brightness(img).enhance(0.5)
		yield 'Curves...', image
		width, height = image.size
		yield 'Create fog layer...', img
		canvas = Image.new('RGB', image.size)
		for x in xrange(0, width, img.size[0]):
			for y in xrange(0, height, img.size[1]):
				canvas.paste(img, (x, y))
		yield 'Merge...', canvas
		image = ImageChops.add(image, canvas)
		yield 'Done', image
