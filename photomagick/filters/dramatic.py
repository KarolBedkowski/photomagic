#!usr/bin/python
# -*- coding: utf-8 -*-

__plugins__ = ('Dramatic', )
__version__ = '2011-03-20'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2011"

from photomagick.common import colors
from photomagick.common import layers
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_SIMPLE


class Dramatic(BaseFilter):
	STEPS = 7
	NAME = _('Dramatic')
	CATEGORY = CATEGORY_SIMPLE

	def process(self, image):
		yield 'Red layer', image
		redlayer = colors.color_mixer_monochrome(image, -1., 1., 1.)
		yield 'Green layer', redlayer
		greenlayer = colors.color_mixer_monochrome(image, 1., -1., 1.)
		yield 'Blue layer', greenlayer
		bluelayer = colors.color_mixer_monochrome(image, 1., 1., -1.)
		yield 'Merge red', bluelayer
		image = layers.merge_layers_overlay(image, redlayer, 1.0)
		yield 'Merge green', image
		image = layers.merge_layers_overlay(image, greenlayer, 1.0)
		yield 'Merge blue', image
		image = layers.merge_layers_overlay(image, bluelayer, 1.0)
		yield 'Done', image
