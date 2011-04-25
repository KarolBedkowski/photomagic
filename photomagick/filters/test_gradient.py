#!usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Karol Będkowski"
__copyright__ = "Copyright (c) Karol Będkowski, 2011"
__version__ = "2011-04-24"

from photomagick.common import gradients
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_BASE


class TestGradient(BaseFilter):
	NAME = _("Test Gradient")
	STEPS = 3
	CATEGORY = CATEGORY_BASE

	def process(self, image):
		image = gradients.create_circular_gradient(image.size, 1.0, circle=False,
				offset=1.2)
		yield 'gradient 1', image
		image = gradients.create_circular_gradient(image.size, 0.7, 0.7, 0.7,
				circle=False, offset=1.2)
		yield 'Done', image
