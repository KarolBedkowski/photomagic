#!usr/bin/python
# -*- coding: utf-8 -*-

__plugins__ = ('Vivid', )
__version__ = '2011-03-20'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2011"

from photomagick.common import curves
from photomagick.common import colors
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_BASE


class Vivid(BaseFilter):
	NAME = _('Vivid')
	STEPS = 3
	CATEGORY = CATEGORY_BASE

	def process(self, image):
		yield 'Mixer...', image
		amount = 0.1
		image = colors.color_mixer(image,
				(1 + amount, -amount, -amount),
				(-amount, 1 + amount, -amount),
				(-amount, -amount, 1 + amount))
		yield 'Curves...', image
		bcurv = list(curves.create_curve([(0, 0), (63, 60), (191, 194), (255, 255)]))
		image = curves.apply_curves(image, bcurv)
#		curves.draw_curve(image, bcurv, 100, 100, (255, 255, 255))
		yield 'Done', image
