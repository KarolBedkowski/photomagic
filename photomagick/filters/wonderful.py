#!usr/bin/python
# -*- coding: utf-8 -*-

__plugins__ = ('Wonderful', )
__version__ = '2011-03-20'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2011"

import Image
import ImageFilter
import ImageEnhance
import ImageChops

from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_BASE


class Wonderful(BaseFilter):
	NAME = _('Wonderful')
	STEPS = 5
	CATEGORY = CATEGORY_BASE

	def process(self, image):
		yield 'Layer...', image
		lay = image.copy()
		lay = lay.filter(ImageFilter.BLUR)
		yield 'Brightness...', lay
		lay = ImageEnhance.Brightness(lay).enhance(1.0)
		yield 'Contrast...', lay
		lay = ImageEnhance.Contrast(lay).enhance(1.0)
		yield 'Mask...', lay
		mask = lay.convert("L")
		mask = ImageChops.invert(mask)
		image = Image.composite(image, lay, mask)
		yield 'Done', image
