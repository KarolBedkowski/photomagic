#!usr/bin/python
# -*- coding: utf-8 -*-

__plugins__ = ('ModBurn', )
__version__ = '2011-03-20'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2011"

import random

import Image
import ImageChops
import ImageDraw
import ImageFilter

from photomagick.lib.debug import log
from photomagick.common import curves
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_MODIFICATOR


class ModBurn(BaseFilter):
	STEPS = 6
	NAME = _('Burn')
	CATEGORY = CATEGORY_MODIFICATOR

	def process(self, image):
		yield 'Coffe...', image
		width, height = image.size
		burn_layer_size = (width / 6, height / 6)
		burn_layer = Image.new("RGB", burn_layer_size, (0, 0, 0))
		burn_width = burn_layer_size[0] / 3
		burn_height = burn_layer_size[1] / 3
		burn_l = burn_layer_size[0] / 3
		burn_t = burn_layer_size[1] / 3
		burn_r = burn_l + burn_width
		burn_b = burn_t + burn_height
		draw = ImageDraw.Draw(burn_layer)
		self._burn_x(burn_layer, draw, burn_l,
				burn_t + random.randint(0, 1) * burn_height)
		self._burn_x(burn_layer, draw, burn_r,
				burn_t + random.randint(0, 1) * burn_height)
		self._burn_y(burn_layer, draw,
				burn_l + random.randint(0, 1) * burn_width,
				burn_t)
		self._burn_y(burn_layer, draw,
				burn_l + random.randint(0, 1) * burn_width,
				burn_b)
		del draw
		burn_layer = burn_layer.filter(ImageFilter.SMOOTH_MORE)
		yield 'Coffe resize..', burn_layer
		burn_layer = burn_layer.crop((burn_l, burn_t, burn_r, burn_b))
		burn_layer = burn_layer.resize((width, height), 2)
		yield 'Coffe Colorize...', burn_layer
		bred = list(curves.create_curve([(0, 0), (120, 150), (255, 255)]))
		bgre = list(curves.create_curve([(0, 0), (200, 150), (255, 255)]))
		bblu = list(curves.create_curve([(0, 0), (160, 10), (255, 255)]))
		burn_layer = curves.apply_curves(burn_layer, None, bred, bgre, bblu)
		yield 'Coffe blur...', burn_layer
		burn_layer = burn_layer.filter(ImageFilter.BLUR)
		burn_layer = burn_layer.filter(ImageFilter.BLUR)
		burn_layer = burn_layer.filter(ImageFilter.BLUR)
		yield 'Merge...', burn_layer
		image = ImageChops.add(image, burn_layer)
		yield 'Done', image

	@log
	def _burn_x(self, image, draw, x, y):
		width, height = image.size
		radius_x = int(width * (random.random() * 0.015 + 0.005))
		radius_y = int(height * (random.random() + 0.1))
		draw.ellipse((x - radius_x, y - radius_y, x + radius_x, y + radius_y),
				fill=(255, 255, 255))

	@log
	def _burn_y(self, image, draw, x, y):
		width, height = image.size
		radius_x = int(width * (random.random() + 0.1))
		radius_y = int(height * (random.random() * 0.015 + 0.005))
		draw.ellipse((x - radius_x, y - radius_y, x + radius_x, y + radius_y),
				fill=(255, 255, 255))
