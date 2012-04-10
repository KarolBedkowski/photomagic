#!usr/bin/python
# -*- coding: utf-8 -*-

__plugins__ = ('IF1', 'IF2', 'IF3', 'IF4', 'IF5' 'IF6', 'IF7', 'IF8', 'IF9')
__version__ = '2012-04-10'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2012"

"""
Filters based on Filtrr:
https://github.com/alexmic/filtrr
"""


import Image
import ImageEnhance
import ImageChops
import ImageFilter

from photomagick.common import colors
from photomagick.common import layers
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_BASE


class IF1(BaseFilter):
	NAME = _('I-F 1')
	STEPS = 4
	CATEGORY = CATEGORY_BASE

	def process(self, image):
		yield 'Tint...', image
		image = colors.tint(image, 60, 35, 10, 170, 140, 160)
		yield 'Contrast...', image
		image = ImageEnhance.Contrast(image).enhance(0.75)
		yield 'Brightness...', image
		image = ImageEnhance.Brightness(image).enhance(1.1)
		yield 'Done', image


class IF2(BaseFilter):
	NAME = _('I-F 2')
	STEPS = 4
	CATEGORY = CATEGORY_BASE

	def process(self, image):
		yield 'Start...', image
		image = ImageEnhance.Color(image).enhance(0.3)
		yield 'Posterize...', image
		image = colors.posterize(image, 70)
		yield 'Tint...', image
		image = colors.tint(image, 50, 35, 10, 190, 190, 230)
		yield 'Done', image


class IF3(BaseFilter):
	NAME = _('I-F 3')
	STEPS = 3
	CATEGORY = CATEGORY_BASE

	def process(self, image):
		yield 'Start...', image
		image = colors.tint(image, 60, 35, 10, 170, 170, 230)
		yield 'Contrast...', image
		image = ImageEnhance.Contrast(image).enhance(0.8)
		yield 'Done', image


class IF4(BaseFilter):
	NAME = _('I-F 4')
	STEPS = 3
	CATEGORY = CATEGORY_BASE

	def process(self, image):
		yield 'Start...', image
		image = colors.convert_to_luminosity(image)
		yield 'Tint...', image
		image = colors.tint(image, 60, 60, 30, 210, 210, 210)
		yield 'Done', image


class IF5(BaseFilter):
	NAME = _('I-F 5')
	STEPS = 6
	CATEGORY = CATEGORY_BASE

	def process(self, image):
		yield 'Start...', image
		image = colors.tint(image, 30, 40, 30, 120, 170, 210)
		yield 'Contrast...', image
		image = ImageEnhance.Contrast(image).enhance(0.7)
		yield 'Bias...', image
		image = colors.bias(image, 1)
		yield 'Saturation...', image
		image = ImageEnhance.Color(image).enhance(0.7)
		yield 'Brightness...', image
		image = ImageEnhance.Brightness(image).enhance(1.1)
		yield 'Done', image


class IF6(BaseFilter):
	NAME = _('I-F 6')
	STEPS = 4
	CATEGORY = CATEGORY_BASE

	def process(self, image):
		yield 'Saturation...', image
		image = ImageEnhance.Color(image).enhance(0.35)
		yield 'Contrast...', image
		image = ImageEnhance.Contrast(image).enhance(0.7)
		yield 'Tint...', image
		image = colors.tint(image, 20, 35, 10, 150, 160, 230)
		yield 'Done', image


class IF7(BaseFilter):
	NAME = _('I-F 7')
	STEPS = 8
	CATEGORY = CATEGORY_BASE

	def process(self, image):
		yield 'Tint...', image
		image2 = colors.tint(image, 20, 35, 10, 150, 160, 230)
		yield 'Saturation...', image2
		image2 = ImageEnhance.Color(image2).enhance(0.6)
		yield 'Mixer...', image
		image = colors.color_mixer(image, [0.1, 0, 0], [0, 0.7, 0], [0, 0, 0.4])
		yield 'Saturation 2...', image
		image = ImageEnhance.Color(image).enhance(0.6)
		yield 'Contrast...', image
		image = ImageEnhance.Contrast(image).enhance(0.6)
		yield 'Multiply...', image
		image = ImageChops.multiply(image, image2)
		yield 'Brightness...', image
		image = ImageEnhance.Brightness(image).enhance(1.3)
		yield 'Done', image


class IF8(BaseFilter):
	NAME = _('I-F 8')
	STEPS = 9
	CATEGORY = CATEGORY_BASE

	def process(self, image):
		yield 'Blur...', image
		blur = image.filter(ImageFilter.BLUR)
		yield 'Background...', image
		back = Image.new(image.mode, image.size, (167, 118, 12))
		yield 'Nocolor...', image
		nocolor = ImageEnhance.Color(image).enhance(0)
		yield 'Merge overlay...', image
		image = layers.merge_layers_overlay(image, nocolor, 1)
		yield 'Merge blur...', image
		image = layers.merge_layers_soft_light(blur, image, 1)
		yield 'Merge color...', image
		image = layers.merge_layers_soft_light(back, image, 1)
		yield 'Saturation...', image
		image = ImageEnhance.Color(image).enhance(0.5)
		yield 'Contrast...', image
		image = ImageEnhance.Contrast(image).enhance(0.8)
		yield 'Done', image


class IF9(BaseFilter):
	NAME = _('I-F 9')
	STEPS = 11
	CATEGORY = CATEGORY_BASE

	def process(self, image):
		yield 'Blur...', image
		blur = image.filter(ImageFilter.SMOOTH)
		yield 'Saturation Blur...', image
		blur = ImageEnhance.Color(blur).enhance(0.2)
		yield 'Background...', image
		back = Image.new(image.mode, image.size, (193, 191, 170))
		yield 'Merge multiply...', image
		top = ImageChops.multiply(blur, back)
		yield 'Saturation...', top
		image = ImageEnhance.Color(image).enhance(0.2)
		yield 'Tint...', image
		image = colors.tint(image, 30, 45, 40, 110, 190, 110)
		yield 'Merge multiply 2...', image
		image = ImageChops.multiply(top, image)
		yield 'Brightness...', image
		image = ImageEnhance.Brightness(image).enhance(1.2)
		yield 'Sharpen...', image
		image = ImageEnhance.Sharpness(image).enhance(1.5)
		yield 'Contrast...', image
		image = ImageEnhance.Contrast(image).enhance(1.1)
		yield 'Done', image
