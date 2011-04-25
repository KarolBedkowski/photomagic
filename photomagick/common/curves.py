#!usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Karol Będkowski"
__copyright__ = "Copyright (c) Karol Będkowski, 2011"
__version__ = "2011-04-24"

from itertools import izip, imap

import Image
import ImageDraw

from photomagick.lib.debug import time_method


@time_method
def apply_curves(image, lum=None, red=None, green=None, blue=None):
	if lum:
		image = image.point(lambda x: lum[x])
	if red or green or blue:
		colors = list(image.split())
		if red:
			colors[0] = colors[0].point(red)
		if green:
			colors[1] = colors[1].point(green)
		if blue:
			colors[2] = colors[2].point(blue)
		image = Image.merge(image.mode, colors)
	return image


@time_method
def create_curve(xys):
	len_xys = len(xys)
	m = map(lambda (x, y): map(lambda (a, b): b ** a,
			enumerate([float(x)] * len_xys)) + [float(y)], xys)
	for i in xrange(len_xys):
		k = i
		while m[k][i] == 0:
			k += 1
		if i < k:
			m = m[:i] + [m[k]] + m[i + 1:k] + [m[i]] + m[k + 1:]
		elif i > k:
			m = m[:k] + [m[i]] + m[k + 1:i] + [m[k]] + m[i + 1:]
		m = m[:i] + [map(lambda n: n / m[i][i], m[i])] + m[i + 1:]
		for j in xrange(len_xys):
			if j != i and m[j][i] != 0:
				m = m[:j] + [map(sum, izip(imap(lambda n: -n * m[j][i], m[i]),
					m[j]))] + m[j + 1:]
	m = [(a, b[-1]) for a, b in enumerate(m) if b[-1]]
	for x in xrange(256):
		value = sum(x ** a * b for a, b in m)
		yield max(min(int(value), 255), 0)


def draw_curve(image, curve, xoffset, yoffset, color=(255, 255, 255)):
	draw = ImageDraw.Draw(image)
	draw.rectangle((xoffset, yoffset, 256 + xoffset, 256 + yoffset),
			fill=0)
	fill = (128, 128, 128)
	draw.line((xoffset + 64, yoffset, xoffset + 64, yoffset + 255), fill=fill)
	draw.line((xoffset + 128, yoffset, xoffset + 128, yoffset + 255), fill=fill)
	draw.line((xoffset + 192, yoffset, xoffset + 192, yoffset + 255), fill=fill)
	draw.line((xoffset, yoffset + 64, xoffset + 255, yoffset + 64), fill=fill)
	draw.line((xoffset, yoffset + 128, xoffset + 255, yoffset + 128), fill=fill)
	draw.line((xoffset, yoffset + 192, xoffset + 255, yoffset + 192), fill=fill)
	for x, y in enumerate(curve):
		draw.point((x + xoffset, yoffset + 256 - y), fill=color)


if __name__ == '__main__':
	curv = list(enumerate(create_curve(
		[(0, 0), (64, 10), (128, 128), (192, 225), (255, 255)])))
	print curv
