#!usr/bin/python
# -*- coding: utf-8 -*-

__plugins__ = ('CrossProcess', )
__version__ = '2011-03-20'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2011"

import ImageEnhance

from photomagick.common import curves
from photomagick.common import colors
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_BASE


class CrossProcess(BaseFilter):
	NAME = _('Cross Process')
	STEPS = 4
	CATEGORY = CATEGORY_BASE

	def process(self, image):
		yield 'Curves...', image
		bred = list(curves.create_curve([(0, 0), (88, 47), (220, 255)]))
		bgre = list(curves.create_curve([(0, 0), (65, 57), (184, 208), (255, 255)]))
		bblu = list(curves.create_curve([(0, 29), (255, 226)]))
		image = curves.apply_curves(image, None, bred, bgre, bblu)

#		curves.draw_curve(image, bred, 100, 100, (255, 0, 0))
#		curves.draw_curve(image, bgre, 100, 400, (0, 255, 0))
#		curves.draw_curve(image, bblu, 100, 700, (0, 0, 255))

		yield 'Contrast...', image
		image = ImageEnhance.Contrast(image).enhance(1.1)
		yield 'Color...', image
		image = colors.apply_color(image, (0xff, 0xff, 0xe0))
		yield 'Done', image
