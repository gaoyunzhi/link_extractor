#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import link_extractor
import os

tests = [
	'https://zhuanlan.zhihu.com/c_1220718229313753088'
]

def test():
	for site in tests:
		links = link_extractor.getLinks(site)
		for link, name in links:
			# with open(fn, 'a') as f:
			# 	f.write(name + ' ' + link + '\n')
			print(name, link)
		# 	...
		# with open(fn, 'a') as f:
		# 	f.write(str(len(links)) + '\n')
		print(site, len(links))
	
if __name__=='__main__':
	test()