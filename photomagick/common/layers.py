#!usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Karol Będkowski"
__copyright__ = "Copyright (c) Karol Będkowski, 2011"
__version__ = "2011-04-24"

import logging
from itertools import izip

import Image
import ImageChops

from photomagick.lib.debug import time_method

_LOG = logging.getLogger(__name__)
support_layers = None
try:
	from photomagick.support import _layers as support_layers
except ImportError, err:
	_LOG.info('support_layers NOT available %s', err)
else:
	_LOG.info('support_layers loaded')


def _set_opacity_layer(layer, opacity):
	if opacity >= 1:
		return layer
	opacity = max(min(opacity, 1), 0)
	color = int(opacity * 255)
	olayer = Image.new("RGB", layer.size, (color, color, color))
	return ImageChops.multiply(layer, olayer)


@time_method
def merge_layers_screen(layer1, layer2, opacity2):
	opacity2 = max(min(opacity2, 1), 0)
	if opacity2 < 1:
		layer2 = _set_opacity_layer(layer2, opacity2)
	return ImageChops.screen(layer1, layer2)


@time_method
def merge_layers_soft_light(layer1, layer2, opacity2):
	layer2 = _set_opacity_layer(layer2, opacity2)
	img = layer1.copy()
	if support_layers:
		support_layers.merge_layers_soft_light(layer1, layer2, img)
		return img
	points = [(int((r1 * r2 * (255 - r1) + r2 * (65025 - (255 - r1) * \
					(255 - r2))) / 65025),
			int((g1 * g2 * (255 - g1) + g2 * (65025 - (255 - g1) * \
					(255 - g2))) / 65025),
			int((b1 * b2 * (255 - b1) + b2 * (65025 - (255 - b1) * \
					(255 - b2))) / 65025))
			for (r1, g1, b1), (r2, g2, b2)
			in izip(layer1.getdata(), layer2.getdata())]
	img.putdata(points)
	return img


@time_method
def merge_layers_overlay(layer1, layer2, opacity2):
	layer2 = _set_opacity_layer(layer2, opacity2)
	img = layer1.copy()
	if support_layers:
		support_layers.merge_layers_overlay(layer1, layer2, img)
		return img
	points = [(int(r1 / 255. * (r1 + 2 * r2 / 255. * (255 - r1))),
			int(g1 / 255. * (g1 + 2 * g2 / 255. * (255 - g1))),
			int(b1 / 255. * (b1 + 2 * b2 / 255. * (255 - b1))))
			for (r1, g1, b1), (r2, g2, b2)
			in izip(layer1.getdata(), layer2.getdata())]
	img.putdata(points)
	return img
