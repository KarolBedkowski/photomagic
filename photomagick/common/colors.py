#!usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Karol Będkowski"
__copyright__ = "Copyright (c) Karol Będkowski, 2011"
__version__ = "2011-04-24"

import math
from itertools import imap, chain
import colorsys
import operator
from random import random
import logging

import Image
import ImageDraw
import ImageChops
import ImageFilter

from photomagick.lib.debug import time_method, log

_LOG = logging.getLogger(__name__)
support_colors = None
try:
	from photomagick.support import _colors as support_colors
except ImportError, err:
	_LOG.info('support_colors NOT available %s', err)
else:
	_LOG.info('support_colors loaded')


@time_method
def apply_color(image, color, opacity=1.0):
	vlayer = Image.new("RGB", image.size, color)
	if opacity < 1 and opacity > 0:
		olayer = Image.new("RGB", image.size, (255, 255, 255))
		vlayer = ImageChops.blend(olayer, vlayer, opacity)
	return ImageChops.multiply(image, vlayer)


@time_method
def fill_with_color(image, color):
	draw = ImageDraw.Draw(image)
	width, height = image.size
	draw.rectangle((0, 0, width, height), fill=color)
	del draw
	return image


@time_method
def color_mixer(image, red=None, green=None, blue=None):
	image = image.copy()
	if not (red or green or blue):
		return image
	params = []
	for color in (red, green, blue):
		if color:
			b_mul = sum(color)
			b_mul = 0 if b_mul == 0 else 1. / b_mul
			params.extend(x * b_mul for x in color)
			params.append(0)
		else:
			params.extend((0, 0, 0, 0))
	return image.convert("RGB", params)


@time_method
def color_mixer_monochrome(image, b_red, b_green, b_blue):
	div = 1. / (b_red + b_green + b_blue)
	b_red *= div
	b_green *= div
	b_blue *= div
	return image.convert("L", [b_red, b_green, b_blue, 0]).convert("RGB")


@log
@time_method
def colorize(image, color):
	r_color, g_color, b_color = color
	h_color, l_color, s_color = colorsys.rgb_to_hls(r_color / 255.,
			g_color / 255., b_color / 255.)
	colors_map = [colorsys.hls_to_rgb(h_color,
			min(255, max(0, lum / 255.)), s_color)
			for lum in xrange(256)]
	cmap = map(lambda x: int(x * 255),
			chain(imap(operator.itemgetter(0), colors_map),
			imap(operator.itemgetter(1), colors_map),
			imap(operator.itemgetter(2), colors_map)))
	return image.convert("L").convert("RGB").point(cmap)


@log
@time_method
def colorize_hls(image, hls):
	h_color, l_color, s_color = hls
	colors_map = [colorsys.hls_to_rgb(h_color,
			min(255, max(0, lum / 255. + l_color)), s_color)
			for lum in xrange(256)]
	cmap = map(lambda x: int(x * 255),
			chain(imap(operator.itemgetter(0), colors_map),
			imap(operator.itemgetter(1), colors_map),
			imap(operator.itemgetter(2), colors_map)))
	return image.convert("L").convert("RGB").point(cmap)


@time_method
def convert_to_luminosity(image):
	return image.convert("L", [0.21, 0.72, 0.07, 0]).convert("RGB")


@time_method
def convert_to_lightness(image):
	data = [((min(rgb) + max(rgb)) / 2)
			for rgb in image.getdata()]
	image = Image.new("L", image.size)
	image.putdata(data)
	return image


@time_method
def convert_to_average(image):
	return image.convert("L", [0.333, 0.333, 0.333, 0]).convert("RGB")


@time_method
def apply_hue_lightness_saturation(image, hue=0, lighness=0, saturation=0,
		keep_luminance=False):
	res = image.copy()
	if support_colors:
		support_colors.apply_hue_lightness_saturation(image, res,
				hue, lighness, saturation, keep_luminance)
		return res
	data = []
	data_append = data.append
	rgb_to_hls = colorsys.rgb_to_hls
	hls_to_rgb = colorsys.hls_to_rgb
	for red, green, blue in image.getdata():
		p_h, p_l, p_s = rgb_to_hls(red / 255., green / 255., blue / 255.)
		p_h += hue
		if p_h > 1:
			p_h -= 1
		elif p_h < 0:
			p_h += 1
		p_s += saturation
		if not keep_luminance:
			p_l += lighness
		red, green, blue = hls_to_rgb(p_h, max(min(p_l, 1), 0), max(min(p_s, 1), 0))
		data_append((int(red * 255), int(green * 255), int(blue * 255)))
	res.putdata(data)
	return res


@time_method
def create_hls_noise(image_size, hue=1, lightnes=1, saturation=1):
	image = Image.new("RGB", image_size)
	if support_colors:
		support_colors.create_hls_noise(image, hue, lightnes, saturation)
		return image
	data = []
	data_append = data.append
	hls_to_rgb = colorsys.hls_to_rgb
	iwidth, iheight = image_size
	for idx in xrange(iwidth * iheight):
		red, green, blue = hls_to_rgb(random() * hue, random() * lightnes,
				random() * saturation)
		data_append((int(red * 255), int(green * 255), int(blue * 255)))
	image.putdata(data)
	return image


@time_method
def create_rgb_noise(image_size, red=1, green=1, blue=1):
	data = []
	data_append = data.append
	iwidth, iheight = image_size
	for idx in xrange(iwidth * iheight):
		data_append((int(red * random() * 255), int(green * random() * 255),
			int(blue * random * 255)))
	image = Image.new("RGB", image_size)
	image.putdata(data)
	return image


@time_method
def create_clouds_bw(image_size, factor=2):
	iwidth = image_size[0] / pow(2, factor)
	iheight = image_size[1] / pow(2, factor)
	c_lay = create_hls_noise((iwidth, iheight), 0, 1, 0)
	c_lay = c_lay.filter(ImageFilter.BLUR)
	c_lay = c_lay.filter(ImageFilter.SMOOTH_MORE)
	c_lay = c_lay.crop((iwidth / 4, iheight / 4, iwidth * 3 / 4, iheight * 3 / 4))
	c_lay = c_lay.resize(image_size, Image.ANTIALIAS)
	return c_lay


def _create_tint_table(min_val, max_val):
	step = 255. / (max_val - min_val)
	for x in xrange(256):
		yield min(max(int((x - min_val) * step), 0), 255)


@time_method
def tint(image, min_r, min_g, min_b, max_r, max_g, max_b):
	r_table = list(_create_tint_table(min_r, max_r))
	g_table = list(_create_tint_table(min_g, max_g))
	b_table = list(_create_tint_table(min_b, max_b))
	colors = list(image.split())
	colors[0] = colors[0].point(r_table)
	colors[1] = colors[1].point(g_table)
	colors[2] = colors[2].point(b_table)
	return Image.merge(image.mode, colors)


def _create_posterize_table(levels):
	step = math.floor(255. / levels)
	for x in xrange(256):
		yield min(max(int((math.floor(x / step) * step)), 0), 255)


@time_method
def posterize(image, levels):
	table = list(_create_posterize_table(levels))
	colors = list(image.split())
	colors[0] = colors[0].point(table)
	colors[1] = colors[1].point(table)
	colors[2] = colors[2].point(table)
	return Image.merge(image.mode, colors)


@time_method
def adjust_saturation(image, saturation):
	res = image.copy()
	data = []
	data_append = data.append
	rgb_to_hls = colorsys.rgb_to_hls
	hls_to_rgb = colorsys.hls_to_rgb
	for red, green, blue in image.getdata():
		p_h, p_l, p_s = rgb_to_hls(red / 255., green / 255., blue / 255.)
		p_s *= saturation
		red, green, blue = hls_to_rgb(p_h, p_l, max(min(p_s, 1), 0))
		data_append((int(red * 255), int(green * 255), int(blue * 255)))
	res.putdata(data)
	return res


def _create_bias_table(value):
	value = float(value)
	for x in xrange(256):
		x2 = x / 255.
		yield min(max(x * (x2 / ((1 / value - 1.9) * (0.9 - x2) + 1)), 0), 255)


@time_method
def bias(image, value):
	table = list(_create_bias_table(value))
	colors = list(image.split())
	colors[0] = colors[0].point(table)
	colors[1] = colors[1].point(table)
	colors[2] = colors[2].point(table)
	return Image.merge(image.mode, colors)


@time_method
def brightness(image, value):
	""" Alternatywna jasność """
	value = int(value)
	table = [min(max(x + value, 0), 255)
			for x in xrange(256)]
	colors = list(image.split())
	colors[0] = colors[0].point(table)
	colors[1] = colors[1].point(table)
	colors[2] = colors[2].point(table)
	return Image.merge(image.mode, colors)


@time_method
def contrast(image, value):
	''' alternatywny kontrast '''
	table = [min(max(int((x - 128.) * value) + 128, 0), 255)
			for x in xrange(256)]
	colors = list(image.split())
	colors[0] = colors[0].point(table)
	colors[1] = colors[1].point(table)
	colors[2] = colors[2].point(table)
	return Image.merge(image.mode, colors)
