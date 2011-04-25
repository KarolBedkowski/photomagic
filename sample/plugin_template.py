#!usr/bin/python
# -*- coding: utf-8 -*-

__version__ = "2011-04-27"
__author__ = "Karol Będkowski"
__copyright__ = "Copyright (c) Karol Będkowski, 2011"

from photomagick.common import colors
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_BASE


class PluginTemplate(BaseFilter):
	NAME = _('Plugin Template')  # visible name of plugin
	STEPS = 1  # number of plugin steps (number of "yield" in process
	CATEGORY = CATEGORY_BASE  # category of plugin

	def process(self, image):
		yield 'Start...', image   # yield always step name and current image
		img = image.copy()  # always copy image for processing
		yield 'Processing...', img
		# do something with img, in example: convert to bw
		img = colors.convert_to_luminosity(img)
		yield 'Done', img  # return processed image
