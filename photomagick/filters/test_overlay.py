#!usr/bin/python
# -*- coding: utf-8 -*-

__plugin_name__ = 'test_overlay'
__author__ = "Karol Będkowski"
__copyright__ = "Copyright (c) Karol Będkowski, 2011"
__version__ = "2011-04-24"

from photomagick.common import colors
from photomagick.common import layers
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_BASE


class TestOverlay(BaseFilter):
	NAME = _("Test Overlay")
	STEPS = 3
	CATEGORY = CATEGORY_BASE

	def process(self, image):
		yield 'Red layer', image
		redlayer = colors.color_mixer_monochrome(image, -1., 1., 1.)
		yield 'Red Layer finis', redlayer
		base = image.copy()
		for x in xrange(11):
			yield 'Merge ' + str(x), image
			image = layers.merge_layers_overlay(base, redlayer, x / 10.)
		yield 'Done', image
