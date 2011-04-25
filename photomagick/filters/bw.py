#!usr/bin/python
# -*- coding: utf-8 -*-

__plugins__ = ('BwLuminosity', 'BwGreen', 'BwOrange', 'BwRed', 'BwYellow',
		'BwInfrared')
__version__ = '2011-03-20'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2011"

import ImageOps

from photomagick.common import colors
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_BASE


class BwLuminosity(BaseFilter):
	STEPS = 3
	NAME = _("BW Luminosity")
	CATEGORY = CATEGORY_BASE

	def process(self, image):
		yield 'Start...', image
		image = colors.convert_to_luminosity(image)
		yield 'Contrast...', image
		image = ImageOps.autocontrast(image)
		yield 'Done', image


class _BwFilter(BaseFilter):
	STEPS = 3
	NAME = 'BW Filter'
	CATEGORY = CATEGORY_BASE
	_COLOR = (1, 1, 1)

	def process(self, image):
		yield 'Start...', image
		image = colors.color_mixer_monochrome(image, *self._COLOR)
		yield 'Contrast...', image
		image = ImageOps.autocontrast(image)
		yield 'Done', image


class BwGreen(_BwFilter):
	NAME = _('BW Green Filter')
	_COLOR = 0.04, 0.27, 0.08


class BwOrange(_BwFilter):
	NAME = _('BW Orange Filter')
	_COLOR = (0.31, 0.09, 0)


class BwRed(_BwFilter):
	NAME = _('BW Red Filter')
	_COLOR = (0.35, 0.04, 0)


class BwYellow(_BwFilter):
	NAME = _('BW Yellow Filter')
	_COLOR = (0.24, 0.11, 0.05)


class BwInfrared(_BwFilter):
	NAME = _('BW Infrared')
	_COLOR = (0.15, 1.15, -0.30)
