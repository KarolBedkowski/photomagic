#!usr/bin/python
# -*- coding: utf-8 -*-

__plugin_name__ = 'Vintage'
__plugins__ = ('Vintage1', 'Vintage2', 'Vintage3')
__copyright__ = "Copyright (c) Karol Będkowski, 2011"
__version__ = "2011-04-24"

import ImageEnhance
import ImageChops

from photomagick.common import curves
from photomagick.common import colors
from photomagick.common import layers
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_SIMPLE


class Vintage1(BaseFilter):
	NAME = _('Vintage')
	STEPS = 7
	CATEGORY = CATEGORY_SIMPLE

	def process(self, base):
		yield 'Colors...', base
		image = ImageEnhance.Color(base).enhance(1.15)
		yield 'Contrast...', image
		image = ImageEnhance.Contrast(image).enhance(1.1)
		yield 'Curves...', image
		cur_r = list(curves.create_curve([(0, 0), (88, 47), (170, 188), (221, 249),
				(255, 255)]))
		cur_g = list(curves.create_curve([(0, 0), (65, 57), (184, 208), (255, 255)]))
		cur_b = list(curves.create_curve([(0, 29), (255, 255)]))
		image = curves.apply_curves(image, None, cur_r, cur_g, cur_b)
		yield 'Sepia...', image
		lsepia = base.copy()
		lsepia = colors.colorize_hls(lsepia, (0.08, -0.4, 0.4))
		lsepia = ImageEnhance.Contrast(lsepia).enhance(1.3)
		yield 'Sepia merging...', lsepia
		image = ImageChops.add(image, lsepia)
		yield 'Magenta...', image
		lmagenta = base.copy()
		lmagenta = colors.fill_with_color(lmagenta, (255, 0, 220))
		image = layers.merge_layers_screen(image, lmagenta, 0.04)
		yield 'Done', image


class Vintage2(BaseFilter):
	NAME = _('Vintage 2')
	STEPS = 2
	CATEGORY = CATEGORY_SIMPLE

	def process(self, image):
		yield 'Curves...', image
		cur_0 = list(curves.create_curve([(0, 0), (100, 120), (255, 255)]))
		cur_r = list(curves.create_curve([(0, 0), (150, 100), (255, 255)]))
		cur_b = list(curves.create_curve([(0, 64), (160, 96), (255, 224)]))
		cur_g = list(curves.create_curve([(0, 0), (150, 100), (255, 255)]))
		image = curves.apply_curves(image, cur_0, cur_r, cur_g, cur_b)
		yield 'Done', image


class Vintage3(BaseFilter):
	NAME = _('Vintage 3')
	STEPS = 6
	CATEGORY = CATEGORY_SIMPLE

	def process(self, image):
		yield 'Contrast...', image
		image = ImageEnhance.Contrast(image).enhance(1.2)
		yield 'Colors...', image
		image = colors.apply_hue_lightness_saturation(image, -0.04, 0, 0.21)
		yield 'Curves...', image
		cur_r = list(curves.create_curve([(0, 0), (100, 120), (200, 255),
				(255, 255)]))
		cur_g = list(curves.create_curve([(0, 0), (64, 80), (224, 235), (255, 255)]))
		cur_b = list(curves.create_curve([(0, 35), (255, 235)]))
		image = curves.apply_curves(image, None, cur_r, cur_g, cur_b)
		yield 'Colors2...', image
		image = colors.apply_hue_lightness_saturation(image, -0.02, 0.09, -0.15)
		yield 'Pink...', image
		lcolor = image.copy()
		lcolor = colors.fill_with_color(lcolor, (255, 0, 90))
		image = ImageChops.blend(image, lcolor, 0.05)
		yield 'Done', image
