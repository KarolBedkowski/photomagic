#!usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Karol Będkowski"
__copyright__ = "Copyright (c) Karol Będkowski, 2011"
__version__ = "2011-04-24"

import logging

import Image
import ImageDraw

from photomagick.lib.debug import time_method

_LOG = logging.getLogger(__name__)
support_gradients = None
try:
	from photomagick.support import _gradients as support_gradients
except ImportError, err:
	_LOG.info('support_gradients NOT available %s', err)
else:
	_LOG.info('support_gradients loaded')


def create_gradient(image, off=1.0, size=1.0, center_w=0.5, center_h=0.5):
	return create_circular_gradient(image.size, size, center_w, center_h, False,
			off)


def create_linear_gradient(image_size, angle=0):
	glayer = Image.new("L", (256, 1))
	for x in xrange(256):
		glayer.putpixel((x, 0), x)
	glayer = glayer.resize(image_size, Image.ANTIALIAS)
	if angle:
		glayer = glayer.rotate(angle, Image.BILINEAR, 1)
	return glayer


@time_method
def create_circular_gradient(image_size, scale=1, x_offset=0.5, y_offset=0.5,
		circle=True, offset=1.0):
	dwidth, dheight = int(512. / scale), int(512. / scale)
	if circle:
		iwidth, iheight = image_size
		if iwidth < iheight:
			dwidth = int(float(dheight) * iwidth / iheight)
		else:
			dheight = int(float(dwidth) * iwidth / iheight)
	if support_gradients:
		glayer = Image.new("RGB", (dwidth, dheight))
		support_gradients.create_gradient(glayer, scale, offset, x_offset,
				y_offset)
	else:
		glayer = Image.new("L", (dwidth, dheight))
		draw = ImageDraw.Draw(glayer)
		c_x = x_offset * glayer.size[0]
		c_y = y_offset * glayer.size[1]
		for x in xrange(255, 0, -1):
			color = int(255 - pow(x / 255.0, offset) * 255.0)
			draw.ellipse((c_x - x, c_y - x, c_x + x, c_y + x), fill=color)
		del draw
	glayer = glayer.resize(image_size, Image.ANTIALIAS)
	return glayer


def create_rect_gradient(image_size, start=0, scale=1, x_offset=0.5,
		y_offset=0.5):
	dwidth, dheight = 512, 512
	glayer = Image.new("L", (dwidth, dheight))
	draw = ImageDraw.Draw(glayer)
	c_x = x_offset * glayer.size[0]
	c_y = y_offset * glayer.size[1]
	for x in xrange(255, 0, -1):
		dist = int(x * scale + start * 255)
		draw.rectangle((c_x - dist, c_y - dist, c_x + dist, c_y + dist),
				fill=(255 - x))
	del draw
	glayer = glayer.resize(image_size, Image.ANTIALIAS)
	return glayer
