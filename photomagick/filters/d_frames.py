#!usr/bin/python
# -*- coding: utf-8 -*-

__version__ = '2011-03-20'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2011"

import Image

from photomagick.lib.appconfig import AppConfig
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_DECORATOR


class FrameLines(BaseFilter):
	STEPS = 4
	CATEGORY = CATEGORY_DECORATOR
	NAME = 'Frame Lines Mask'

	def process(self, image):
		yield 'Loading Mask...', image
		frame_file_p = AppConfig().get_data_file('frame_lines.png')
		mask_file_p = AppConfig().get_data_file('frame_lines_mask.png')
		frame = Image.open(frame_file_p).convert("RGB")
		mask = Image.open(mask_file_p).convert("L")
		yield 'Scale...', mask
		width, height = image.size
		if width > height:
			frame = frame.rotate(270, Image.BILINEAR, True)
			mask = mask.rotate(270, Image.BILINEAR, True)
		frame = frame.resize(image.size, Image.ANTIALIAS)
		mask = mask.resize(image.size, Image.ANTIALIAS)
		yield 'Merge...', mask
		image = Image.composite(image, frame, mask)
		image = image.convert("RGB")
		yield 'Done', image


class OldPhotoFrame(BaseFilter):
	STEPS = 5
	CATEGORY = CATEGORY_DECORATOR
	NAME = 'Old photo frame'

	def process(self, image):
		yield 'Loading frame...', image
		frame_file_p = AppConfig().get_data_file('old_photo_frame.png')
		frame = Image.open(frame_file_p)
		yield 'Scale frame...', frame
		width, height = image.size
		if width > height:
			frame = frame.rotate(90, Image.BILINEAR, True)
		frame = frame.resize(image.size, Image.ANTIALIAS)
		frame = frame.convert("RGB")
		yield 'Scale image...', frame
		margin = int(max(width * 0.03, height * 0.03))
		width = int(width - 2 * margin)
		height = int(height - 2 * margin)
		image = image.resize((width, height), Image.ANTIALIAS)
		yield 'Merge...', image
		frame.paste(image, (margin, margin))
		yield 'Done', frame
