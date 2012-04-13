#!usr/bin/python
# -*- coding: utf-8 -*-

__plugins__ = ('ModCoffee', 'ModCanvas', 'ModFabric', 'ModInterlaced',
		'ModFilmGrain', 'ModScratch')
__version__ = '2011-03-20'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2011"

import random

import Image
import ImageChops
import ImageDraw
import ImageFilter
import ImageEnhance

from photomagick.lib import appconfig
from photomagick.common import colors
from photomagick.common import curves
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_MODIFICATOR


class ModCoffee(BaseFilter):
	STEPS = 2
	NAME = _('Coffee')
	CATEGORY = CATEGORY_MODIFICATOR
	_IMAGES = ('coffee/coffee1.png', 'coffee/coffee2.png', 'coffee/coffee3.png',
			'coffee/coffee4.png', 'coffee/coffee5.png')

	def _load_stain(self, scale):
		idx = random.randint(0, len(self._IMAGES) - 1)
		imgp = appconfig.AppConfig().get_data_file(self._IMAGES[idx])
		img = Image.open(imgp)
		scale *= random.random() + 0.5
		img = img.resize((int(img.size[0] * scale), int(img.size[1] * scale)),
				Image.ANTIALIAS)
		img = img.rotate(random.randint(0, 360))
		return img

	def process(self, image):
		yield 'Coffee...', image
		image = image.copy()
		width, height = image.size
		scale = min(width, height) / 600.
		for idx in xrange(random.randint(2, 6)):
			stain = self._load_stain(scale)
			x = random.randint(0, width)
			y = random.randint(0, height)
			image.paste(stain, (x, y), stain)
		yield 'Done', image


class ModCanvas(BaseFilter):
	STEPS = 4
	NAME = _('Canvas')
	CATEGORY = CATEGORY_MODIFICATOR
	_IMAGE = 'canvas.png'

	def process(self, image):
		yield 'Loading...', image
		imgp = appconfig.AppConfig().get_data_file(self._IMAGE)
		img = Image.open(imgp)
		width, height = image.size
		yield 'Create canvas...', img
		canvas = Image.new('RGB', image.size)
		for x in xrange(0, width, img.size[0]):
			for y in xrange(0, height, img.size[1]):
				canvas.paste(img, (x, y))
		yield 'Merge...', canvas
		image = ImageChops.multiply(image, canvas)
		yield 'Done', image


class ModFabric(BaseFilter):
	STEPS = 4
	NAME = _('Fabric')
	CATEGORY = CATEGORY_MODIFICATOR
	_IMAGE = 'fabric.png'

	def process(self, image):
		yield 'Loading...', image
		imgp = appconfig.AppConfig().get_data_file(self._IMAGE)
		img = Image.open(imgp)
		width, height = image.size
		yield 'Create fabric...', img
		canvas = Image.new('RGB', image.size)
		for x in xrange(0, width, img.size[0]):
			for y in xrange(0, height, img.size[1]):
				canvas.paste(img, (x, y))
		yield 'Merge...', canvas
		image = ImageChops.multiply(image, canvas)
		yield 'Done', image


class ModInterlaced(BaseFilter):
	STEPS = 2
	NAME = _('Interlaced')
	CATEGORY = CATEGORY_MODIFICATOR

	def process(self, image):
		yield 'Creating...', image
		image = image.copy()
		width, height = image.size
		draw = ImageDraw.Draw(image)
		fill = (0, 0, 0)
		for y in xrange(0, height, 2):
			draw.line((0, y, width, y), fill=fill)
		del draw
		yield 'Done', image


class ModFilmGrain(BaseFilter):
	STEPS = 2
	NAME = _('Film Grain')
	CATEGORY = CATEGORY_MODIFICATOR

	def process(self, image, maximum=1):
		yield 'Creating...', image
		width, height = image.size
		noise = colors.create_hls_noise(image.size, 0, 1, 0)
		yield 'Curves...', noise
		bcurv = list(curves.create_curve([(0, 255), (128, 220), (255, 255)]))
		noise = curves.apply_curves(noise, bcurv)
		if maximum < 1:
			noise = ImageEnhance.Brightness(noise).enhance(1.2 - maximum / 5.)
		yield 'merge...', noise
		image = ImageChops.multiply(image, noise)
		yield 'Done', image


class ModScratch(BaseFilter):
	STEPS = 4
	NAME = _('Scratch')
	CATEGORY = CATEGORY_MODIFICATOR

	def process(self, image):
		yield 'Creating...', image
		width, height = image.size
		count = width * height / 500
		layer = Image.new("L", image.size, 0)
		draw = ImageDraw.Draw(layer)
		fill = 16
		randint = random.randint
		height4 = height / 16
		for idx in xrange(count):
			x1 = randint(0, width)
			x2 = x1 + randint(-width, width)
			y1 = randint(0, height)
			y2 = y1 + randint(-height4, height4) * 2
			draw.line((x1, y1, x2, y2), fill=fill)
		del draw
		yield 'Smooth...', layer
		layer = layer.filter(ImageFilter.SMOOTH)
		layer = layer.convert("RGB")
		yield 'Merge...', layer
		image = ImageChops.add(image, layer)
		yield 'Done', image
