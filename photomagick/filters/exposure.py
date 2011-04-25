#!usr/bin/python
# -*- coding: utf-8 -*-

__plugins__ = ('LowContrast', 'HiContrast', 'OverExposed', 'UnderExposed')
__version__ = '2011-03-20'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2011"

import ImageEnhance

from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_BASE


class LowContrast(BaseFilter):
	NAME = _('Low Contrast')
	STEPS = 2
	CATEGORY = CATEGORY_BASE

	def process(self, image):
		yield 'Contrast...', image
		image = ImageEnhance.Contrast(image).enhance(0.8)
		yield 'Done', image


class HiContrast(BaseFilter):
	NAME = _('Hi Contrast')
	STEPS = 2
	CATEGORY = CATEGORY_BASE

	def process(self, image):
		yield 'Contrast...', image
		image = ImageEnhance.Contrast(image).enhance(1.4)
		yield 'Done', image


class OverExposed(BaseFilter):
	NAME = _('Over Exposed')
	STEPS = 2
	CATEGORY = CATEGORY_BASE

	def process(self, image):
		yield 'Contrast...', image
		image = ImageEnhance.Brightness(image).enhance(1.4)
		yield 'Done', image


class UnderExposed(BaseFilter):
	NAME = _('Under Exposed')
	STEPS = 2
	CATEGORY = CATEGORY_BASE

	def process(self, image):
		yield 'Contrast...', image
		image = ImageEnhance.Brightness(image).enhance(0.8)
		yield 'Done', image
