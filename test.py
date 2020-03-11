#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import link_extractor
import os
import sys

def test():
	# link_extractor.gen(news_source='bbc')
	pdf_name = link_extractor.gen(news_source='nyt英文')
	os.system('open %s -g' % pdf_name)
	
test()