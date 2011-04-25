#!usr/bin/python
# -*- coding: utf-8 -*-

__plugins__ = ('Polaroid', )
__version__ = '2011-03-20'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2011"

import ImageEnhance
import ImageChops

from photomagick.common import curves
from photomagick.common import colors
from photomagick.common import gradients
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_BASE


class Polaroid(BaseFilter):
	STEPS = 5
	NAME = _('Polaroid')
	CATEGORY = CATEGORY_BASE

	def process(self, image):
		yield 'Curves...', image
		bred = list(curves.create_curve([(0, 0), (120, 150), (255, 255)]))
		bgre = list(curves.create_curve([(0, 0), (120, 140), (255, 255)]))
		bblu = list(curves.create_curve([(0, 0), (120, 160), (255, 255)]))
		image = curves.apply_curves(image, None, bred, bgre, bblu)
		yield 'Brightness...', image
		image = ImageEnhance.Brightness(image).enhance(1.1)
		yield 'Contrast...', image
		image = ImageEnhance.Contrast(image).enhance(0.7)
		yield 'Color...', image
		image = ImageEnhance.Color(image).enhance(0.9)
		yield 'Vignette...', image
		vig = gradients.create_gradient(image, 2, 3.0, 0.45, 0.48)
		yield 'Vignette created...', vig
		vig = colors.colorize(vig, (255, 150, 150))
		vig = ImageEnhance.Contrast(vig).enhance(0.9)
		yield 'Vignette 1 colored...', vig
		image = ImageChops.multiply(image, vig)
		yield 'Vignette...', image
		vig2 = gradients.create_gradient(image, 2, 3.0, 0.52, 0.6)
		yield 'Vignette 1 applied...', image
		vig2 = ImageEnhance.Contrast(vig2).enhance(0.9)
		vig2 = colors.colorize(vig2, (150, 220, 255))
		yield 'Vignette 2 colored...', vig2
		image = ImageChops.multiply(image, vig2)
		yield 'Done Colors...', image
