#!usr/bin/python
# -*- coding: utf-8 -*-

__plugin_name__ = 'Warming cooling'
__plugins__ = ('Wratten80', 'Wratten82', 'Wratten81', 'Wratten85')
__version__ = '2011-03-20'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2011"

import ImageEnhance

from photomagick.common import colors
from photomagick.common import layers
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_SIMPLE


class _Wratten(BaseFilter):
	STEPS = 4
	NAME = ''
	CATEGORY = CATEGORY_SIMPLE
	_COLOR = (0, 0, 0)

	def process(self, image):
		yield 'Start', image
		color = colors.fill_with_color(image.copy(), self._COLOR)
		yield 'Merge', color
		image = layers.merge_layers_overlay(image, color, 0.15)
		yield 'Brightness', image
		image = ImageEnhance.Brightness(image).enhance(1.5)
		yield 'Done', image


class Wratten80(_Wratten):
	NAME = _('Wratten 80 C')
	_COLOR = (0, 109, 255)


class Wratten82(_Wratten):
	NAME = _('Wratten 82 C')
	_COLOR = (0, 181, 255)


class Wratten81(_Wratten):
	NAME = _('Wratten 81 W')
	_COLOR = (235, 177, 19)


class Wratten85(_Wratten):
	NAME = _('Wratten 85 W')
	_COLOR = (237, 138, 0)
