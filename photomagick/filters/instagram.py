#!usr/bin/python
# -*- coding: utf-8 -*-

__plugins__ = ('Apollo', 'EarlyBird', 'F1977', 'Gotham', 'Helfe', 'Lomo2',
		'LordKelvin', 'Nashvile', 'Sutro', 'Toaster', 'Valden', 'Xpro2', )
__version__ = '2012-04-12'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2012"

"""
Inspired by:
https://github.com/changneng/Instagram-image-filter.git
http://www.quora.com/Instagram/How-does-Instagram-develop-their-filters
"""


from photomagick.common import curves
from photomagick.common import vignette
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_SIMPLE
from photomagick.filters.m_dirt import ModFilmGrain


class Apollo(BaseFilter):
	NAME = _('Apollo')
	STEPS = 1 + ModFilmGrain.STEPS
	CATEGORY = CATEGORY_SIMPLE

	def process(self, image):
		yield 'Curves...', image
		rcurv = list(curves.create_curve(
			[(0, 1), (32, 36), (64, 81), (128, 159), (192, 214), (224, 228),
				(255, 243)]
		))
		gcurv = list(curves.create_curve(
			[(0, 1), (32, 58), (64, 103), (128, 182), (192, 224), (224, 238),
				(255, 253)]
		))
		bcurv = list(curves.create_curve(
			[(0, 35), (32, 67), (64, 104), (128, 168), (192, 217), (224, 229),
				(255, 240)]
		))
		image = curves.apply_curves(image, None, rcurv, gcurv, bcurv)
		for msg, image in ModFilmGrain().process(image, 0.3):
			yield msg, image
#		curves.draw_curve(image, rcurv, 100, 100, (255, 255, 255))
#		curves.draw_curve(image, gcurv, 400, 100, (255, 255, 255))
#		curves.draw_curve(image, bcurv, 100, 400, (255, 255, 255))


class EarlyBird(BaseFilter):
	NAME = _('EarlyBird')
	STEPS = 2
	CATEGORY = CATEGORY_SIMPLE

	def process(self, image):
		yield 'Curves...', image
		rcurv = list(curves.create_curve([(0, 12), (48, 71), (92, 100), (150, 169),
				(212, 212), (230, 226), (255, 245)]))
		gcurv = list(curves.create_curve([(0, 0), (16, 3), (92, 100), (172, 200),
				(220, 224), (255, 248)]))
		bcurv = list(curves.create_curve([(0, 18), (16, 46), (32, 68), (40, 78),
				(50, 90), (96, 142), (112, 170),
				(144, 202), (160, 215), (200, 230),
				(215, 236), (225, 242), (235, 245), (255, 255)]))
		image = curves.apply_curves(image, None, rcurv, gcurv, bcurv)
#		curves.draw_curve(image, rcurv, 100, 100, (255, 255, 255))
#		curves.draw_curve(image, gcurv, 400, 100, (255, 255, 255))
#		curves.draw_curve(image, bcurv, 100, 400, (255, 255, 255))
		yield 'Done', image


class F1977(BaseFilter):
	NAME = _('1977')
	STEPS = 2
	CATEGORY = CATEGORY_SIMPLE

	def process(self, image):
		yield 'Curves...', image

		rcurv = [65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65,
				66, 66, 66, 66, 66, 66, 66, 66, 66, 66, 66, 66, 66, 66, 66, 66,
				65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65,
				65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65,
				66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81,
				82, 83, 84, 85, 87, 88, 89, 90, 92, 93, 94, 95, 97, 98, 99, 100,
				102, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125,
				127, 129, 131, 133, 133, 134, 134, 135, 135, 136, 136, 137, 137,
				138, 138, 139, 139, 140, 140, 141, 142, 143, 144, 145, 146, 148,
				149, 150, 151, 152, 154, 155, 156, 157, 158, 160, 161, 162, 163,
				165, 166, 167, 168, 170, 171, 172, 173, 175, 176, 177, 178, 180,
				181, 182, 183, 184, 185, 186, 187, 189, 190, 191, 192, 193, 194,
				195, 196, 198, 198, 199, 200, 201, 202, 203, 204, 205, 205, 206,
				207, 208, 209, 210, 211, 212, 212, 212, 212, 212, 212, 212, 212,
				212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212,
				212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212,
				212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212,
				212, 213, 213, 213, 213, 213, 213, 213, 213, 213, 213, 213, 213,
				213, 213, 213, 213]
		gcurv = [58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58,
				58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58,
				58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58,
				58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58,
				59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74,
				76, 77, 78, 79, 80, 81, 82, 83, 85, 86, 87, 88, 89, 90, 91, 92,
				94, 95, 97, 99, 100, 102, 104, 105, 107, 109, 110, 112, 114, 115,
				117, 119, 121, 121, 121, 122, 122, 122, 123, 123, 124, 124, 124,
				125, 125, 125, 126, 126, 127, 128, 129, 130, 131, 132, 133, 134,
				135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147,
				148, 149, 150, 152, 153, 154, 155, 156, 157, 158, 159, 161, 162,
				163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175,
				176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188,
				189, 190, 191, 192, 194, 195, 196, 197, 198, 199, 200, 201, 202,
				203, 204, 205, 206, 207, 208, 209, 210, 210, 211, 212, 213, 214,
				215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 225, 226,
				227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239,
				240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240,
				240, 240, 240]
		bcurv = [82, 82, 82, 82, 82, 82, 82, 82, 82, 82, 82, 82, 82, 82, 82, 82,
				83, 83, 83, 83, 83, 83, 83, 83, 83, 83, 83, 83, 83, 83, 83, 83,
				83, 83, 83, 83, 83, 83, 83, 83, 83, 83, 83, 83, 83, 83, 83, 83,
				83, 83, 84, 85, 86, 86, 87, 88, 89, 89, 90, 91, 92, 92, 93, 94,
				95, 96, 97, 98, 99, 100, 101, 102, 104, 105, 106, 107, 108, 109,
				110, 111, 113, 114, 115, 116, 117, 118, 119, 120, 122, 123, 124,
				125, 126, 127, 128, 129, 131, 132, 134, 136, 137, 139, 141, 142,
				144, 146, 147, 149, 151, 152, 154, 156, 158, 158, 158, 159, 159,
				159, 160, 160, 161, 161, 161, 162, 162, 162, 163, 163, 164, 165,
				166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178,
				179, 181, 182, 183, 184, 185, 186, 187, 188, 190, 191, 192, 193,
				194, 195, 196, 197, 199, 200, 201, 202, 203, 204, 205, 206, 207,
				208, 209, 210, 211, 212, 213, 214, 216, 216, 217, 217, 218, 218,
				219, 219, 220, 221, 221, 222, 222, 223, 223, 224, 225, 225, 225,
				225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225,
				225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225,
				225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225,
				225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225,
				225, 225, 225, 225, 225, 225, 225, 225, 225]
		image = curves.apply_curves(image, None, rcurv, gcurv, bcurv)
		#curves.draw_curve(image, rcurv, 100, 100, (255, 255, 255))
		#curves.draw_curve(image, gcurv, 400, 100, (255, 255, 255))
		#curves.draw_curve(image, bcurv, 100, 400, (255, 255, 255))
		yield 'Done', image


class Gotham(BaseFilter):
	NAME = _('Gotham')
	STEPS = 2
	CATEGORY = CATEGORY_SIMPLE

	def process(self, image):
		yield 'Curves...', image
		rcurv = list(curves.create_curve(
			[(0, 0), (32, 4), (64, 15), (128, 77), (192, 143), (224, 189),
				(255, 252)]
		))
		gcurv = list(curves.create_curve(
			[(0, 0), (32, 3), (64, 12), (128, 59), (192, 152), (224, 205),
				(255, 253)]
		))
		bcurv = list(curves.create_curve(
			[(0, 0), (32, 7), (64, 20), (128, 53), (192, 151), (224, 207),
				(255, 253)]
		))
		image = curves.apply_curves(image, None, rcurv, gcurv, bcurv)
#		curves.draw_curve(image, rcurv, 100, 100, (255, 255, 255))
#		curves.draw_curve(image, gcurv, 400, 100, (255, 255, 255))
#		curves.draw_curve(image, bcurv, 100, 400, (255, 255, 255))
		yield 'Done', image


class Helfe(BaseFilter):
	NAME = _('Helfe')
	STEPS = 1 + ModFilmGrain.STEPS
	CATEGORY = CATEGORY_SIMPLE

	def process(self, image):
		yield 'Curves...', image
		rcurv = list(curves.create_curve(
			[(0, 1), (32, 4), (64, 28), (128, 129), (192, 208), (224, 220),
				(255, 234)]
		))
		gcurv = list(curves.create_curve(
			[(0, 1), (32, 8), (64, 44), (128, 171), (192, 226), (224, 241),
				(255, 254)]
		))
		bcurv = list(curves.create_curve(
			[(0, 35), (32, 44), (64, 97), (128, 193), (192, 230), (224, 244),
				(255, 254)]
		))
		image = curves.apply_curves(image, None, rcurv, gcurv, bcurv)
		for msg, image in ModFilmGrain().process(image, 0.4):
			yield msg, image
#		curves.draw_curve(image, rcurv, 100, 100, (255, 255, 255))
#		curves.draw_curve(image, gcurv, 400, 100, (255, 255, 255))
#		curves.draw_curve(image, bcurv, 100, 400, (255, 255, 255))


class Lomo2(BaseFilter):
	NAME = _('Lomo 2')
	STEPS = 3
	CATEGORY = CATEGORY_SIMPLE

	def process(self, image):
		yield 'Curves...', image
		curv = list(curves.create_curve([(0, 0), (20, 1), (40, 12), (65, 40),
				(150, 235), (180, 244), (200, 248), (210, 250), (225, 252),
				(255, 255)]))
		image = curves.apply_curves(image, None, curv, curv, curv)
		yield 'vignette...', image
		image = vignette.vignette(image)
#		curves.draw_curve(image, curv, 100, 100, (255, 255, 255))
		yield 'Done', image


class LordKelvin(BaseFilter):
	NAME = _('Lord Kelvin')
	STEPS = 2
	CATEGORY = CATEGORY_SIMPLE

	def process(self, image):
		yield 'Curves...', image
		rcurv = list(curves.create_curve(
			[(0, 69), (32, 69), (64, 69), (128, 92), (192, 114), (224, 121),
				(255, 122)]
		))
		for x in xrange(82):
			rcurv[x] = 69
		gcurv = list(curves.create_curve(
			[(0, 36), (32, 36), (64, 67), (128, 137), (192, 180), (224, 190),
				(255, 192)]
		))
		for x in xrange(32):
			gcurv[x] = 36
		bcurv = list(curves.create_curve(
			[(0, 43), (32, 81), (64, 132), (128, 210), (192, 243), (224, 250),
				(255, 254)]
		))
		image = curves.apply_curves(image, None, rcurv, gcurv, bcurv)
#		curves.draw_curve(image, rcurv, 100, 100, (255, 255, 255))
#		curves.draw_curve(image, gcurv, 400, 100, (255, 255, 255))
#		curves.draw_curve(image, bcurv, 100, 400, (255, 255, 255))
		yield 'Done', image


class Nashvile(BaseFilter):
	NAME = _('Nashvile')
	STEPS = 2
	CATEGORY = CATEGORY_SIMPLE

	def process(self, image):
		yield 'Curves...', image
		rcurv = list(curves.create_curve(
			[(0, 97), (32, 109), (64, 126), (128, 154), (192, 169), (224, 173),
				(255, 173)]
		))
		gcurv = list(curves.create_curve(
			[(0, 37), (32, 59), (64, 97), (128, 170), (192, 209), (224, 217),
				(255, 222)]
		))
		bcurv = list(curves.create_curve(
			[(0, 57), (32, 57), (64, 69), (128, 188), (192, 242), (224, 251),
				(255, 254)]
		))
		for x in xrange(50):
			bcurv[x] = 57
		image = curves.apply_curves(image, None, rcurv, gcurv, bcurv)
#		curves.draw_curve(image, rcurv, 100, 100, (255, 255, 255))
#		curves.draw_curve(image, gcurv, 400, 100, (255, 255, 255))
#		curves.draw_curve(image, bcurv, 100, 400, (255, 255, 255))
		yield 'Done', image


class Sutro(BaseFilter):
	NAME = _('Sutro')
	STEPS = 1 + ModFilmGrain.STEPS
	CATEGORY = CATEGORY_SIMPLE

	def process(self, image):
		yield 'Curves...', image
		rcurv = list(curves.create_curve([(0, 12), (48, 71), (92, 100), (150, 169),
				(212, 212), (230, 226), (255, 245)]))
		gcurv = list(curves.create_curve([(0, 0), (16, 3), (92, 100), (172, 200),
				(220, 224), (255, 248)]))
		bcurv = list(curves.create_curve([(0, 18), (16, 46), (32, 68), (40, 78),
				(50, 90), (96, 142), (112, 170),
				(144, 202), (160, 215), (200, 230),
				(215, 236), (225, 242), (235, 245), (255, 255)]))
		image = curves.apply_curves(image, None, rcurv, gcurv, bcurv)
		for msg, image in ModFilmGrain().process(image, 0.5):
			yield msg, image


class Toaster(BaseFilter):
	NAME = _('Toaster')
	STEPS = 1 + ModFilmGrain.STEPS
	CATEGORY = CATEGORY_SIMPLE

	def process(self, image):
		yield 'Curves...', image
		rcurv = list(curves.create_curve([(0, 0), (65, 62), (160, 173), (200, 196),
				(225, 206), (255, 217)]))
		for x in xrange(65):
			rcurv[x] = 62
		gcurv = list(curves.create_curve([(0, 0), (64, 69), (140, 190), (200, 230),
				(255, 255)]))
		bcurv = list(curves.create_curve([(0, 104), (50, 136), (100, 189),
				(180, 231), (255, 255)]))
		image = curves.apply_curves(image, None, rcurv, gcurv, bcurv)
		for msg, image in ModFilmGrain().process(image, 0.4):
			yield msg, image
#		curves.draw_curve(image, rcurv, 100, 100, (255, 255, 255))
#		curves.draw_curve(image, gcurv, 400, 100, (255, 255, 255))
#		curves.draw_curve(image, bcurv, 100, 400, (255, 255, 255))


class Valden(BaseFilter):
	NAME = _('Valden')
	STEPS = 1 + ModFilmGrain.STEPS
	CATEGORY = CATEGORY_SIMPLE

	def process(self, image):
		yield 'Curves...', image
		rcurv = list(curves.create_curve(
				[(0, 25), (32, 44), (64, 72), (128, 155), (192, 214), (224, 231),
				(255, 244)]))
		gcurv = list(curves.create_curve(
				[(0, 12), (32, 31), (64, 62), (128, 163), (192, 222), (224, 238),
				(255, 247)]))
		bcurv = list(curves.create_curve(
				[(0, 6), (32, 23), (64, 52), (128, 158), (192, 223), (224, 239),
				(255, 250)]))
		image = curves.apply_curves(image, None, rcurv, gcurv, bcurv)
		for msg, image in ModFilmGrain().process(image, 0.3):
			yield msg, image
#		curves.draw_curve(image, rcurv, 100, 100, (255, 255, 255))
#		curves.draw_curve(image, gcurv, 400, 100, (255, 255, 255))
#		curves.draw_curve(image, bcurv, 100, 400, (255, 255, 255))


class Xpro2(BaseFilter):
	NAME = _('X-Pro II')
	STEPS = 2
	CATEGORY = CATEGORY_SIMPLE

	def process(self, image):
		yield 'Curves...', image
		rcurv = list(curves.create_curve([(0, 25), (128, 118), (255, 255)]))
		curv = list(curves.create_curve([(0, 0), (64, 13), (128, 104),
				(225, 249), (255, 255)]))
		image = curves.apply_curves(image, None, rcurv, curv, curv)
#		curves.draw_curve(image, curv, 100, 100, (255, 255, 255))
		yield 'Done', image
