#!usr/bin/python
# -*- coding: utf-8 -*-

__plugins__ = ('SimpleFrame', 'BlackBorder', 'PinStripe', 'BlackBigBorder',
		'WhiteBorder', 'Telescope', 'Portrait', 'WhiteBorder2',
		'RoundedBlackFrame', 'RoundedWhiteFrame')
__version__ = '2011-03-20'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2011"

import Image
import ImageFilter
import ImageDraw
import ImageChops

from photomagick.lib.appconfig import AppConfig
from photomagick.common import gradients
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_DECORATOR


class SimpleFrame(BaseFilter):
	STEPS = 4
	NAME = _('Simple frame')
	CATEGORY = CATEGORY_DECORATOR

	def process(self, image):
		yield 'Scale..', image
		width, height = image.size
		fleft = int(width * 0.05)
		fwidth = width - 2 * fleft
		ftop = int(height * 0.05)
		fheight = height - 2 * ftop
		iwidth = fwidth - 2 * fleft
		iheight = fheight - 2 * ftop
		ileft = (width - iwidth) / 2
		itop = (height - iheight) / 2
		image = image.resize((iwidth, iheight), 1)
		yield 'Frame...', image
		bimage = Image.new('RGB', (width, height), (255, 255, 255))
		draw = ImageDraw.Draw(bimage)
		draw.rectangle((fleft, ftop, fleft + fwidth, ftop + fheight),
				fill=(50, 50, 50))
		del draw
		bimage = bimage.filter(ImageFilter.BLUR)
		draw = ImageDraw.Draw(bimage)
		draw.rectangle((fleft, ftop, fleft + fwidth, ftop + fheight),
			fill=(255, 255, 255), outline=(50, 50, 50))
		del draw
		yield 'Merge...', bimage
		bimage.paste(image, (ileft, itop, ileft + iwidth, itop + iheight))
		yield 'Done', bimage


class BlackBorder(BaseFilter):
	STEPS = 4
	NAME = _('Black Border')
	CATEGORY = CATEGORY_DECORATOR

	def process(self, image):
		yield 'Scale..', image
		width, height = image.size
		fwidth = max(2, int(width * 0.01))
		iwidth = width - 2 * fwidth
		iheight = height - 2 * fwidth
		image = image.resize((iwidth, iheight), 1)
		yield 'Frame...', image
		bimage = Image.new('RGB', (width, height), (0, 0, 0))
		yield 'Merge...', bimage
		bimage.paste(image, (fwidth, fwidth, fwidth + iwidth, fwidth + iheight))
		yield 'Done', bimage


class BlackBigBorder(BaseFilter):
	STEPS = 4
	NAME = _('Black Big  Border')
	CATEGORY = CATEGORY_DECORATOR

	def process(self, image):
		yield 'Scale..', image
		width, height = image.size
		fwidth = max(2, int(width * 0.05))
		iwidth = width - 2 * fwidth
		iheight = height - 2 * fwidth
		image = image.resize((iwidth, iheight), 1)
		yield 'Frame...', image
		bimage = Image.new('RGB', (width, height), (0, 0, 0))
		yield 'Merge...', bimage
		bimage.paste(image, (fwidth, fwidth, fwidth + iwidth, fwidth + iheight))
		yield 'Done', bimage


class WhiteBorder(BaseFilter):
	STEPS = 4
	NAME = _('White Border')
	CATEGORY = CATEGORY_DECORATOR

	def process(self, image):
		yield 'Scale..', image
		width, height = image.size
		fwidth = max(2, int(width * 0.05))
		iwidth = width - 2 * fwidth
		iheight = height - 2 * fwidth
		image = image.resize((iwidth, iheight), 1)
		yield 'Frame...', image
		bimage = Image.new('RGB', (width, height), (255, 255, 255))
		yield 'Merge...', bimage
		bimage.paste(image, (fwidth, fwidth, fwidth + iwidth, fwidth + iheight))
		yield 'Done', bimage


class PinStripe(BaseFilter):
	STEPS = 4
	NAME = _('Pin Stripe')
	CATEGORY = CATEGORY_DECORATOR

	def process(self, image):
		yield 'Scale..', image
		width, height = image.size
		fwidth = max(2, int(width * 0.01))
		iwidth = width - 8 * fwidth
		iheight = height - 8 * fwidth
		image = image.resize((iwidth, iheight), 1)
		yield 'Frame...', image
		bimage = Image.new('RGB', (width, height), (0, 0, 0))
		draw = ImageDraw.Draw(bimage)
		draw.rectangle((fwidth, fwidth, width - fwidth, height - fwidth),
				fill=(255, 255, 255))
		draw.rectangle((fwidth * 3, fwidth * 3, width - fwidth * 3,
				height - fwidth * 3), fill=(0, 0, 0))
		del draw
		yield 'Merge...', bimage
		bimage.paste(image, (fwidth * 4, fwidth * 4, fwidth * 4 + iwidth,
				fwidth * 4 + iheight))
		yield 'Done', bimage


class Telescope(BaseFilter):
	STEPS = 3
	NAME = _('Telescope')
	CATEGORY = CATEGORY_DECORATOR

	def process(self, image):
		yield 'Mask..', image
		width, height = image.size
		radius = int(min(width, height) * 0.48)
		lay = Image.new('L', (width, height), 0)
		draw = ImageDraw.Draw(lay)
		center_w, center_h = width / 2, height / 2
		draw.ellipse((center_w - radius, center_h - radius,
			center_w + radius, center_h + radius), fill=255)
		del draw
		lay = lay.filter(ImageFilter.BLUR)
		lay = lay.filter(ImageFilter.BLUR)
		lay = lay.convert("RGB")
		yield 'Merge...', lay
		image = ImageChops.multiply(image, lay)
		yield 'Done', image


class Portrait(BaseFilter):
	STEPS = 3
	NAME = _('Portrait')
	CATEGORY = CATEGORY_DECORATOR

	def process(self, image):
		yield 'Mask..', image
		gradient = gradients.create_gradient(image, 4.0, 0.95)
		gradient = gradient.convert("L")
		lay = Image.new('RGB', image.size, (255, 255, 255))
		yield 'Merge...', lay
		image = Image.composite(image, lay, gradient)
		yield 'Done', image


class WhiteBorder2(BaseFilter):
	STEPS = 3
	NAME = _('White border 2')
	CATEGORY = CATEGORY_DECORATOR

	def process(self, image):
		yield 'Loading...', image
		borderp = AppConfig().get_data_file('border1.png')
		border = Image.open(borderp)
		borderr = float(border.size[0]) / border.size[1]
		yield 'Top...', border
		width, height = image.size
		top = border.resize((width, int(width / borderr)), Image.ANTIALIAS)
		image.paste(top, (0, 0), top)
		yield 'Bottom...', image
		bottom = top.rotate(180, Image.BILINEAR)
		image.paste(bottom, (0, height - bottom.size[1]), bottom)
		yield 'Left...', image
		left = border.rotate(90).resize((int(height / borderr), height),
				Image.ANTIALIAS)
		image.paste(left, (0, 0), left)
		yield 'Right...', image
		right = left.rotate(180, Image.BILINEAR)
		image.paste(right, (width - right.size[0], 0), right)
		yield 'Done', image


class RoundedBlackFrame(BaseFilter):
	STEPS = 3
	NAME = _('Rounded Black Frame')
	CATEGORY = CATEGORY_DECORATOR
	_COLOR = 0

	def process(self, image):
		yield 'Creating frame...', image
		width, height = image.size
		border = int(min(width, height) * 0.05)
		flay = Image.new("L", image.size, 0)
		draw = ImageDraw.Draw(flay)
		border2 = 2 * border
		border3 = 3 * border
		draw.rectangle((border2, border, width - border2, height - border), 255)
		draw.rectangle((border, border2, width - border, height - border2), 255)
		draw.ellipse((border, border, border3, border3), 255)
		draw.ellipse((width - border3, border, width - border, border3), 255)
		draw.ellipse((border, height - border3, border3, height - border), 255)
		draw.ellipse((width - border3, height - border3, width - border,
				height - border), 255)
		del draw
		flay = flay.filter(ImageFilter.SMOOTH_MORE)
		yield 'Merge...', flay
		blay = Image.new("RGB", image.size, (self._COLOR, self._COLOR,
				self._COLOR))
		image = Image.composite(image, blay, flay)
		yield 'Done', image


class RoundedWhiteFrame(RoundedBlackFrame):
	STEPS = 3
	NAME = _('Rounded White Frame')
	CATEGORY = CATEGORY_DECORATOR
	_COLOR = 255


class _MaskedFrame(BaseFilter):
	STEPS = 4
	CATEGORY = CATEGORY_DECORATOR
	_MASK_FILE = None

	def process(self, image):
		yield 'Loading Mask...', image
		mask_file_p = AppConfig().get_data_file(self._MASK_FILE)
		mask = Image.open(mask_file_p)
		yield 'Scale...', mask
		width, height = image.size
		mwidth, mheight = mask.size
		if (width > height and mwidth < mheight) or \
				(width < height and mwidth > mheight):
			mask = mask.rotate(90, Image.BILINEAR, True)
		mask = mask.resize(image.size, Image.ANTIALIAS)
		mask = mask.convert("RGB")
		mask = mask.filter(ImageFilter.SMOOTH)
		yield 'Merge...', mask
		image = ImageChops.multiply(image, mask)
		yield 'Done', image


class MaskedFrame1(_MaskedFrame):
	NAME = 'Frame 1'
	_MASK_FILE = 'mask_1.png'


class MaskedFrame2(_MaskedFrame):
	NAME = 'Frame 2'
	_MASK_FILE = 'mask_2.png'


class MaskedFrame3(_MaskedFrame):
	NAME = 'Frame 3'
	_MASK_FILE = 'mask_3.png'


class MaskedFrame4(_MaskedFrame):
	NAME = 'Frame 4'
	_MASK_FILE = 'mask_4.png'


class MaskedFrame5(_MaskedFrame):
	NAME = 'Frame 5'
	_MASK_FILE = 'mask_5.png'
