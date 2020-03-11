#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import news_2_pdf
import os
import sys

def test():
	# news_2_pdf.gen(news_source='bbc')
	pdf_name = news_2_pdf.gen(news_source='nyt英文')
	os.system('open %s -g' % pdf_name)
	
test()