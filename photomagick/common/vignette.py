#!usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Karol Będkowski"
__copyright__ = "Copyright (c) Karol Będkowski, 2011"
__version__ = "2011-04-24"

import ImageFilter
import ImageChops
import ImageEnhance

from photomagick.lib.debug import time_method

from gradients import create_circular_gradient
from colors import create_clouds_bw
import curves


@time_method
def vignette(image, off=0.2, stop=0.7, center_w=0.5, center_h=0.5):
	width, height = image.size
	vlayer = create_circular_gradient(image.size, 1.3, center_w, center_h, False)
	curv = list(curves.create_curve([(0, 0), (96, 200), (255, 255)]))
	vlayer = curves.apply_curves(vlayer, curv)
	vlayer = vlayer.filter(ImageFilter.BLUR).convert("RGB")
	clouds = create_clouds_bw(vlayer.size, 3)
	clouds = ImageEnhance.Brightness(clouds).enhance(3)
	clouds = ImageEnhance.Contrast(clouds).enhance(0.9)
	clouds = ImageChops.multiply(clouds, ImageChops.invert(vlayer))
	return ImageChops.multiply(image, ImageChops.invert(clouds))
