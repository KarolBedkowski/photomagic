#!usr/bin/python
# -*- coding: utf-8 -*-

__plugins__ = ('Andy1', 'Andy2', 'Andy3', 'Andy9')
__version__ = '2011-03-20'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2011"

import ImageFilter
import ImageEnhance
import ImageChops
import ImageOps

from photomagick.common import colors
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_SIMPLE


class Andy1(BaseFilter):
	NAME = _('Andy1')
	STEPS = 10
	CATEGORY = CATEGORY_SIMPLE

	def _apply_color(self, img, color, mask):
		img = colors.apply_color(img, color)
		img = ImageChops.multiply(img, mask)
		return img

	def process(self, image):
		yield 'Start...', image
		simage = ImageOps.autocontrast(image, 20)
		s_width, s_height = image.size[0] / 2, image.size[1] / 2
		simage = image.resize((s_width, s_height))
		simage = colors.convert_to_luminosity(simage)
		simage = simage.filter(ImageFilter.SMOOTH)
		yield 'Mask...', simage
		mask = ImageEnhance.Brightness(simage).enhance(2)
		mask = ImageOps.posterize(mask, 2)
		mask = ImageOps.autocontrast(mask, 20)
		yield 'Curves...', mask
		simage = ImageEnhance.Contrast(simage).enhance(2)
		yield 'posterize...', simage
		simage = ImageOps.posterize(simage, 2)
		yield 'Red...', simage
		red_img = self._apply_color(simage, (255, 0, 0), mask)
		yield 'green...', red_img
		green_img = self._apply_color(simage, (0, 255, 0), mask)
		yield 'blue...', green_img
		blue_img = self._apply_color(simage, (0, 0, 255), mask)
		yield 'yellow...', blue_img
		yellow_img = self._apply_color(simage, (255, 255, 0), mask)
		yield 'Merge...', yellow_img
		image = image.copy()
		image.paste(red_img, (0, 0, s_width, s_height))
		image.paste(green_img, (s_width, 0, s_width * 2, s_height))
		image.paste(yellow_img, (0, s_height, s_width, s_height * 2))
		image.paste(blue_img, (s_width, s_height, s_width * 2, s_height * 2))
		yield 'Done', image


class Andy2(BaseFilter):
	NAME = _('Andy2')
	STEPS = 9
	CATEGORY = CATEGORY_SIMPLE

	def _apply_color(self, img, color, mask):
		oimg = colors.apply_hue_lightness_saturation(img, color, 0, 1, True)
		oimg = ImageChops.multiply(oimg, mask)
		return oimg

	def process(self, image):
		yield 'Start...', image
		simage = ImageOps.autocontrast(image, 20)
		s_width, s_height = image.size[0] / 2, image.size[1] / 2
		simage = image.resize((s_width, s_height))
		simage = simage.filter(ImageFilter.SMOOTH)
		yield 'Mask...', simage
		mask = ImageEnhance.Brightness(simage).enhance(2)
		mask = ImageOps.posterize(mask, 2)
		mask = ImageOps.autocontrast(mask, 20)
		yield 'posterize...', mask
		simage = ImageEnhance.Brightness(simage).enhance(2)
		simage = ImageOps.equalize(simage)
		simage = simage.filter(ImageFilter.SMOOTH_MORE)
		simage = ImageOps.posterize(simage, 1)
		yield 'Red...', simage
		red_img = self._apply_color(simage, 0.25, mask)
		yield 'green...', red_img
		green_img = self._apply_color(simage, 0.75, mask)
		yield 'blue...', green_img
		blue_img = self._apply_color(simage, 1, mask)
		yield 'yellow...', blue_img
		yellow_img = self._apply_color(simage, 0.5, mask)
		yield 'Merge...', yellow_img
		image = image.copy()
		image.paste(red_img, (0, 0, s_width, s_height))
		image.paste(green_img, (s_width, 0, s_width * 2, s_height))
		image.paste(yellow_img, (0, s_height, s_width, s_height * 2))
		image.paste(blue_img, (s_width, s_height, s_width * 2, s_height * 2))
		yield 'Done', image


class Andy3(BaseFilter):
	NAME = _('Andy3')
	STEPS = 11
	CATEGORY = CATEGORY_SIMPLE

	def _apply_color(self, img, color):
		oimg = colors.apply_hue_lightness_saturation(img, color, 0, 1, True)
		return oimg

	def process(self, image):
		yield 'Start...', image
		s_width, s_height = image.size[0] / 2, image.size[1] / 2
		simage = image.resize((s_width, s_height))
		yield 'posterize...', simage
		simage = simage.convert("L")
		yield 'posterize 2...', simage
		simage = ImageEnhance.Brightness(simage).enhance(2)
		simage = ImageOps.equalize(simage)
		yield 'posterize 3...', simage
		simage = ImageOps.autocontrast(simage, 20)
		yield 'posterize 4...', simage
		simage = ImageOps.posterize(simage, 1)
		colors = []
		colors.extend([255] * 128)
		colors.extend([0] * 128)
		colors.extend([0] * 128)
		colors.extend([255] * 128)
		colors.extend([0] * 256)
		simage = simage.convert("RGB").point(colors)
		yield 'Red...', simage
		red_img = self._apply_color(simage, 0.82)
		yield 'green...', red_img
		green_img = self._apply_color(simage, 0.75)
		yield 'blue...', green_img
		blue_img = self._apply_color(simage, 0)
		yield 'yellow...', blue_img
		yellow_img = self._apply_color(simage, 0.6)
		yield 'Merge...', yellow_img
		image = image.copy()
		image.paste(red_img, (0, 0, s_width, s_height))
		image.paste(green_img, (s_width, 0, s_width * 2, s_height))
		image.paste(yellow_img, (0, s_height, s_width, s_height * 2))
		image.paste(blue_img, (s_width, s_height, s_width * 2, s_height * 2))
		yield 'Done', image


class Andy9(BaseFilter):
	NAME = _('Andy9')
	STEPS = 13
	CATEGORY = CATEGORY_SIMPLE

	def process(self, image):
		yield 'Start...', image
		s_width, s_height = image.size[0] / 3, image.size[1] / 3
		simage = image.resize((s_width, s_height))
		yield 'posterize...', simage
		simage = simage.convert("L")
		simage = ImageEnhance.Brightness(simage).enhance(2)
		simage = ImageOps.equalize(simage)
		simage = ImageOps.autocontrast(simage, 20)
		simage = ImageOps.posterize(simage, 1)
		yield 'colors...', simage
		colormap = []
		colormap.extend([255] * 128)
		colormap.extend([0] * 128)
		colormap.extend([0] * 128)
		colormap.extend([255] * 128)
		colormap.extend([0] * 256)
		simage = simage.convert("RGB").point(colormap)
		image = image.copy()
		for x in xrange(3):
			for y in xrange(3):
				yield 'Img %d...' % (x * 3 + y + 1), simage
				simg = colors.apply_hue_lightness_saturation(simage,
						((x * 3 + (2.9 - y)) / 10.), 0, 1, True)
				image.paste(simg, (x * s_width, y * s_height,
						(x + 1) * s_width, (y + 1) * s_height))
		yield 'Done', image
