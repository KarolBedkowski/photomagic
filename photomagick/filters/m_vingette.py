#!usr/bin/python
# -*- coding: utf-8 -*-

__plugins__ = ('ModVignette', )
__version__ = '2011-03-20'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2011"


import random

from photomagick.common import vignette
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_MODIFICATOR


class ModVignette(BaseFilter):
	STEPS = 2
	NAME = _('Vignette')
	CATEGORY = CATEGORY_MODIFICATOR

	def process(self, image):
		yield 'vignette...', image
		image = vignette.vignette(image,
				random.random() * 0.2 + 0.1, random.random() * 0.2 + 0.6,
				random.random() * 0.1 + 0.45, random.random() * 0.1 + 0.45)
		yield 'Done', image
