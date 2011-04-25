#!usr/bin/python
# -*- coding: utf-8 -*-

__plugins__ = ('FilmFrame35mm', 'FilmFrame4x5')
__version__ = '2011-03-20'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2011"

import Image
import ImageChops

from photomagick.lib import appconfig
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_DECORATOR


class FilmFrame35mm(BaseFilter):
	STEPS = 4
	NAME = _('35mm Film Frame')
	CATEGORY = CATEGORY_DECORATOR

	def process(self, image):
		yield 'Frame..', image
		width, height = image.size
		framep = appconfig.AppConfig().get_data_file('frame35m.png')
		frame = Image.open(framep)
		frame = frame.convert("L")
		if height > width:
			frame = frame.rotate(90, Image.BILINEAR, 1)
		frame.thumbnail(image.size, Image.ANTIALIAS)
		frame = frame.convert("RGB")
		yield 'Scale..', frame
		if height > width:
			size = (int(frame.size[0] * 0.7), int(frame.size[1] * 0.95))
		else:
			size = (int(frame.size[0] * 0.95), int(frame.size[1] * 0.7))
		image = image.copy()
		image.thumbnail(size, Image.ANTIALIAS)
		yield 'Merge...', image
		ileft = (frame.size[0] - image.size[0]) / 2
		itop = (frame.size[1] - image.size[1]) / 2
		iwidth = image.size[0]
		iheight = image.size[1]
		frame.paste(image, (ileft, itop, ileft + iwidth, itop + iheight))
		yield 'Done', frame


class FilmFrame4x5(BaseFilter):
	STEPS = 7
	NAME = _('4x5 Film Frame')
	CATEGORY = CATEGORY_DECORATOR

	def process(self, image):
		yield 'Frame..', image
		width, height = image.size
		framep = appconfig.AppConfig().get_data_file('frame4x5.png')
		frame = Image.open(framep)
		frame.convert("L")
		if height < width:
			frame = frame.rotate(270, Image.BILINEAR, 1)
		frame.thumbnail(image.size, Image.ANTIALIAS)
		frame = frame.convert("RGB")
		yield 'Scale..', frame
		image.thumbnail(frame.size, Image.ANTIALIAS)
		image = image.copy()
		yield 'Mask..', image
		maskp = appconfig.AppConfig().get_data_file('frame4x5_mask.png')
		mask = Image.open(maskp)
		if height < width:
			mask = mask.rotate(270, Image.BILINEAR, 1)
		yield 'Scale..', mask
		mask = mask.resize(frame.size)
		mask = mask.convert("L")
		yield 'Merge...', mask
		back = Image.new("RGB", frame.size, (0, 0, 0))
		ileft = (back.size[0] - image.size[0]) / 2
		itop = (back.size[1] - image.size[1]) / 2
		iwidth = image.size[0]
		iheight = image.size[1]
		back.paste(image, (ileft, itop, ileft + iwidth, itop + iheight))
		yield 'Merge2...', back
		image = ImageChops.composite(back, frame, mask)
		yield 'Done', image
