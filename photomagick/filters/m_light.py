#!usr/bin/python
# -*- coding: utf-8 -*-

__plugins__ = ('ModBurn', 'ModSunBurn', 'ModGlow')
__version__ = '2011-03-20'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2011"

import random

import Image
import ImageChops
import ImageDraw
import ImageFilter
import ImageEnhance

from photomagick.lib.debug import log
from photomagick.common import curves
from photomagick.common import gradients
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


class ModSunBurn(BaseFilter):
	STEPS = 4
	NAME = _('SunBurn')
	CATEGORY = CATEGORY_MODIFICATOR

	def process(self, image):
		yield 'Blink...', image
		width, height = image.size
		pos = random.random() * 0.25
		size = random.random() * 0.3 + 1.0 + pos * 0.3
		print size, pos
		if random.randint(0, 1):
			pos = 1 - pos
		grad = gradients.create_circular_gradient(image.size, size, pos, 0.0,
				False)
		yield 'Gradient', grad
		grad = grad.convert("RGB")
		bred = list(curves.create_curve([(0, 0), (120, 150), (255, 255)]))
		bgre = list(curves.create_curve([(0, 0), (200, 150), (255, 255)]))
		bblu = list(curves.create_curve([(0, 0), (160, 10), (255, 255)]))
		grad_color = curves.apply_curves(grad, None, bred, bgre, bblu)
		yield 'Merge..', grad_color
		image = ImageChops.add(image, grad_color)
		yield 'Done', image


class ModGlow(BaseFilter):
	STEPS = 5
	NAME = _('Glow')
	CATEGORY = CATEGORY_MODIFICATOR
	DISABLED = True

	def process(self, image):
		width, height = image.size
		yield 'Glow...', image
		highlights = self._draw_glow(image)
		yield 'Contrast, Brightness...', highlights
		highlights = highlights.filter(ImageFilter.GaussianBlur(20))
		yield 'Blur...', highlights
		highlights = highlights.filter(ImageFilter.BLUR)
		highlights = highlights.filter(ImageFilter.GaussianBlur(20))
		yield 'Merge..', highlights
		image = ImageChops.add(image, highlights)
		yield 'Done...', image

	def _draw_glow(self, image, minval=0.95):
		width, height = image.size
		outimg = Image.new('RGB', image.size, (0, 0, 0))
		draw = ImageDraw.Draw(outimg)
		divs = [lambda x: 0,
				lambda x: int(x / 3.),
				lambda x: int(x / 4.),
				lambda x: int(x / 8.),
				lambda x: int(x / 12.),
				lambda x: int(x / 20.),
				lambda x: int(x / 30.),
				lambda x: int(x / 50.),
				lambda x: int(x / 60.),
				lambda x: int(x / 80.),
				lambda x: int(x / 100.), ]
		minval = int(minval * 255 * 3)
		for gidx in xrange(10, 0, -1):
			for idx, rgb in enumerate(image.getdata()):
				srgb = sum(rgb)
				if srgb < minval:
					continue
				y, x = divmod(idx, width)
				g_size = int(srgb / 100. * gidx)
				if g_size > 0:
					rgb2 = tuple(map(divs[gidx], rgb))
					draw.ellipse((x - g_size, y - g_size, x + g_size, y + g_size),
							fill=rgb2)
		del draw
		return outimg


class ModGlow2(BaseFilter):
	STEPS = 23
	NAME = _('Glow2')
	CATEGORY = CATEGORY_MODIFICATOR

	def process(self, image):
		width, height = image.size
		yield 'Glow...', image
		result = []
		for src in image.split():
			maxv = int(src.getextrema()[1] * 0.98)
			result.append(src.point(lambda i: i > maxv and 255 or 0))
		highlights = Image.merge("RGB", tuple(result))
		for x in xrange(10):
			yield 'Contrast, Brightness...', highlights
			highlights = ImageEnhance.Brightness(highlights).enhance(1.5)
			yield 'Blur...', highlights
			highlights = highlights.filter(ImageFilter.BLUR)
			highlights = highlights.filter(ImageFilter.GaussianBlur(10))
		highlights = ImageEnhance.Brightness(highlights).enhance(0.3)
		yield 'Merge..', highlights
		image = ImageChops.add(image, highlights)
		yield 'Done...', image
