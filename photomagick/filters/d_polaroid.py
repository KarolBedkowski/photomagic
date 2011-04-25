#!usr/bin/python
# -*- coding: utf-8 -*-

__plugins__ = ('PolaroidFrame', )
__version__ = '2011-03-20'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2011"

import Image

from photomagick.lib import debug
from photomagick.lib.appconfig import AppConfig
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_DECORATOR


class PolaroidFrame(BaseFilter):
	STEPS = 5
	NAME = _('Polaroid frame')
	CATEGORY = CATEGORY_DECORATOR

	def process(self, image):
		width, height = image.size
		yield 'Loading background...', image
		back_p = AppConfig().get_data_file('polaroid_back.png')
		back = Image.open(back_p)
		yield 'Scale', back
		if width > height:
			back = self._scale_back(image, back)
			back = back.convert("RGB")
			yield 'Merge', back
			image = self._process_landscape(image, back)
		else:
			back = back.rotate(270, Image.BILINEAR, True)
			back = self._scale_back(image, back)
			back = back.convert("RGB")
			yield 'Merge', back
			image = self._process_portrait(image, back)
		yield 'Done', image

	@debug.log
	def _process_portrait(self, image, back):
		width, height = image.size
		bwidth, bheight = back.size
		iwidth, iheight = int(bwidth * 0.85), int(bheight * 0.80)
		img = self._scale_img(image, iwidth, iheight)
		width, height = img.size
		img_left = (bwidth - width) / 2
		img_top = int((bheight * 0.9 - height) / 2)
		back.paste(img, (img_left, img_top))
		return back

	@debug.log
	def _process_landscape(self, image, back):
		width, height = image.size
		bwidth, bheight = back.size
		iwidth, iheight = int(bwidth * 0.80), int(bheight * 0.85)
		img = self._scale_img(image, iwidth, iheight)
		width, height = img.size
		img_left = int((bwidth * 0.9 - width) / 2)
		img_top = (bheight - height) / 2
		back.paste(img, (img_left, img_top))
		return back

	def _scale_img(self, img, width, height):
		iwidth, iheight = img.size
		scale = min(float(iwidth) / width, float(iheight) / height)
		iwidth = int(iwidth / scale)
		iheight = int(iheight / scale)
		img = img.resize((iwidth, iheight), Image.ANTIALIAS)
		if iwidth > width:
			margin = int(iwidth - width) / 2
			img = img.crop((margin, 0, iwidth - margin, iheight))
		if iheight > height:
			margin = int(iheight - height) / 2
			print locals()
			img = img.crop((0, margin, iwidth, iheight - margin))
		return img

	def _scale_back(self, image, back):
		width, height = image.size
		bwidth, bheight = back.size
		scale = max(float(bwidth) / width, float(bheight) / height)
		back = back.resize((int(bwidth / scale), int(bheight / scale)),
				Image.ANTIALIAS)
		return back
