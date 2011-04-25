#!usr/bin/python
# -*- coding: utf-8 -*-

__plugins__ = ('Tonemapping', )
__version__ = '2011-03-20'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2011"

import ImageChops
import ImageFilter

from photomagick.common import colors
from photomagick.common import layers
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_BASE


class Tonemapping(BaseFilter):
	NAME = _('Tonemapping')
	STEPS = 6
	CATEGORY = CATEGORY_BASE

	def process(self, base):
		yield 'Desaturate...', base
		lay1 = colors.convert_to_luminosity(base)
		yield 'Invert...', lay1
		lay1 = ImageChops.invert(lay1)
		yield 'Smoth...', lay1
		lay1 = lay1.filter(ImageFilter.BLUR)
		yield 'Merge...', lay1
		lay2 = base.copy()
		lay2 = ImageChops.blend(lay1, lay2, 0.75)
		yield 'Mege softlight...', lay2
		image = base.copy()
		image = layers.merge_layers_soft_light(image, lay2, 0.9)
		yield 'Done', image
