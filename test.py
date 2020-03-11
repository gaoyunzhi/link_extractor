#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import link_extractor

def test():
	links = link_extractor.getLinks(
		# 'https://www.bbc.com/zhongwen/simp', domain='https://www.bbc.co.uk')
		# 'https://cn.nytimes.com')
		# 'https://www.bbc.co.uk')
		'https://www.nytimes.com')
	for link, name in links:
		print(name, link)
	print(len(links))
	
if __name__=='__main__':
	test()