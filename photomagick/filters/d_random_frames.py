#!usr/bin/python
# -*- coding: utf-8 -*-

__version__ = '2011-03-20'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2011"

from random import randint

import Image
import ImageFilter
import ImageDraw
import ImageChops

from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_DECORATOR


class LinesFrame(BaseFilter):
	STEPS = 5
	NAME = _('Random Frame - Lines')
	CATEGORY = CATEGORY_DECORATOR
	DISABLED = True
	_BORDER_WIDTH = 0.04
	_BORDER_MARGIN = 0.01
	_LINES = 0.01
	_LINES_COLOR = (0, 0, 0)

	def process(self, image):
		iwidth, iheight = image.size
		yield 'Creating frame...', image
		width, height = iwidth, iheight
		frame = Image.new("RGB", (width, height), (255, 255, 255))
		draw = ImageDraw.Draw(frame)
		margin_x = int(self._BORDER_MARGIN * width)
		margin_y = int(self._BORDER_MARGIN * height)
		b_width = int(self._BORDER_WIDTH * width)
		b_height = int(self._BORDER_WIDTH * height)
		b_width2 = b_width / 2
		b_height2 = b_height / 2
		line_width = max(max(b_width, b_height) / 10, 3)
		for x in xrange(int(width + height) * self._LINES):
			# left
			x1 = margin_x + randint(0, b_width)
			x2 = margin_x + randint(0, b_width)
			y1 = randint(0, b_height2)
			y2 = height - randint(0, b_height2)
			draw.line((x1, y1, x2, y2), fill=self._LINES_COLOR, width=line_width)
			# right
			x1 = width - (margin_x + randint(0, b_width))
			x2 = width - (margin_x + randint(0, b_width))
			y1 = randint(0, b_height2)
			y2 = height - randint(0, b_height2)
			draw.line((x1, y1, x2, y2), fill=self._LINES_COLOR, width=line_width)
			# top
			x1 = randint(0, b_width2)
			x2 = width - randint(0, b_width2)
			y1 = margin_y + randint(0, b_height)
			y2 = margin_y + randint(0, b_height)
			draw.line((x1, y1, x2, y2), fill=self._LINES_COLOR, width=line_width)
			# bottom
			x1 = randint(0, b_width2)
			x2 = width - randint(0, b_width2)
			y1 = height - (margin_y + randint(0, b_height))
			y2 = height - (margin_y + randint(0, b_height))
			draw.line((x1, y1, x2, y2), fill=self._LINES_COLOR, width=line_width)
		del draw
		yield 'Smooth...', frame
		frame = frame.filter(ImageFilter.SMOOTH_MORE)
		yield 'Rescale...', frame
		frame = frame.resize((iwidth, iheight), Image.ANTIALIAS)
		yield 'Merge...', frame
		image = ImageChops.multiply(image, frame)
		yield 'Done', image


class Lines2Frame(BaseFilter):
	STEPS = 8
	NAME = _('Random Frame - Lines2')
	CATEGORY = CATEGORY_DECORATOR
	_BORDER_WIDTH = 0.04
	_BORDER_MARGIN = 0.04
	_BORDER_OFF = 0.02
	_LINES_COLOR = (0, 0, 0)
	_LINES_COLOR2 = (128, 128, 128)

	def process(self, image):
		width, height = image.size
		yield 'Creating frame...', image
		frame = Image.new("RGB", (width, height), (255, 255, 255))
		draw = ImageDraw.Draw(frame)
		m_width_height = min(width, height)
		margin_x = margin_y = int(self._BORDER_MARGIN * m_width_height)
		b_width = b_height = int(self._BORDER_WIDTH * m_width_height)
		b_width2 = int(b_width * 1.2)
		b_height2 = int(b_height * 1.2)
		o_width = o_height = int(self._BORDER_OFF * m_width_height)
		line_width = max(b_width / 7, 3)
		iwidth, iheight = width - 2 * margin_x, height - 2 * margin_y
		yield 'Creating frame 1...', image
		for x in xrange(o_width, width - o_width, line_width):
			# top
			y1 = margin_y + randint(o_height, b_height2)
			y2 = max(0, margin_y - randint(o_height, b_height2))
			draw.line((x, y1, x, y2), fill=self._LINES_COLOR2, width=line_width)
			# bottom
			y1 = height - max(0, margin_y - randint(o_height, b_height2))
			y2 = height - margin_y - randint(o_height, b_height2)
			draw.line((x, y1, x, y2), fill=self._LINES_COLOR2, width=line_width)
		yield 'Creating frame 2...', image
		for y in xrange(o_height, height - o_height, line_width):
			# right
			x1 = width - (margin_x + randint(o_width, b_width2))
			x2 = width - max(0, margin_x - randint(o_width, b_width2))
			draw.line((x1, y, x2, y), fill=self._LINES_COLOR2, width=line_width)
			# left
			x1 = max(0, margin_x - randint(o_width, b_width2))
			x2 = margin_x + randint(o_width, b_width2)
			draw.line((x1, y, x2, y), fill=self._LINES_COLOR2, width=line_width)
		yield 'Creating frame 3...', image
		for x in xrange(o_width, width - o_width, line_width):
			# top
			y1 = margin_y + randint(o_height, b_height)
			y2 = max(0, margin_y - randint(o_height, b_height))
			draw.line((x, y1, x, y2), fill=self._LINES_COLOR, width=line_width)
			# bottom
			y1 = height - max(0, margin_y - randint(o_height, b_height))
			y2 = height - margin_y - randint(o_height, b_height)
			draw.line((x, y1, x, y2), fill=self._LINES_COLOR, width=line_width)
		yield 'Creating frame 4...', image
		for y in xrange(o_height, height - o_height, line_width):
			# right
			x1 = width - (margin_x + randint(o_width, b_width))
			x2 = width - max(0, margin_x - randint(o_width, b_width))
			draw.line((x1, y, x2, y), fill=self._LINES_COLOR, width=line_width)
			# left
			x1 = max(0, margin_x - randint(o_width, b_width))
			x2 = margin_x + randint(o_width, b_width)
			draw.line((x1, y, x2, y), fill=self._LINES_COLOR, width=line_width)
		del draw
		yield 'Smooth...', frame
		frame = frame.filter(ImageFilter.SMOOTH_MORE)
		yield 'Border...', frame
		image = image.resize((iwidth, iheight), 1)
		yield 'Frame...', image
		bimage = Image.new('RGB', (width, height), (255, 255, 255))
		bimage.paste(image, ((width - iwidth) / 2, (height - iheight) / 2))
		yield 'Merge...', frame
		image = ImageChops.multiply(bimage, frame)
		yield 'Done', image
