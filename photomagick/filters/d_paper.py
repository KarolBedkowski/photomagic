#!usr/bin/python
# -*- coding: utf-8 -*-

__plugins__ = ('DecPaperCurl', )
__version__ = '2011-03-20'
__author__ = 'Karol Będkowski'
__copyright__ = "Copyright (c) Karol Będkowski, 2011"

import Image

from photomagick.lib import appconfig
from photomagick.common.base_filter import BaseFilter
from photomagick.common.const import CATEGORY_DECORATOR


class DecPaperCurl(BaseFilter):
	STEPS = 4
	NAME = _('Paper Curl')
	CATEGORY = CATEGORY_DECORATOR

	def process(self, image):
		yield 'Frame..', image
		image = image.copy()
		width, height = image.size
		paperp = appconfig.AppConfig().get_data_file('paper_curl.png')
		paper = Image.open(paperp)
		pwidth, pheight = paper.size
		scale = max(float(pwidth) / width, float(pheight) / height) * 1.5
		paper = paper.resize((int(pwidth / scale), int(pheight / scale)),
				Image.ANTIALIAS)
		yield 'Merge...', paper
		pwidth, pheight = paper.size
		image.paste(paper, (width - pwidth, height - pheight), paper)
		yield 'Done', image
