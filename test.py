#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import link_extractor
import os

tests = [
	'https://vocus.cc/5a12023feceaed97b40204c9/home',
	# 'http://tagesschau.de',
	# 'http://www.gzhshoulu.wang/account_PourMarx.html',
	# 'https://jacobinmag.com/',
	# 'https://matters.news',
	# 'https://matters.news/@Margaux1848',
	# 'https://matters.news/@zoezhao',
	# 'https://opinion.cw.com.tw/',
	# 'https://squatting2047.com',
	# 'https://wemp.app/accounts/12c2c49c-305d-4de3-85c8-00d372e7a47a',
	# 'https://whogovernstw.org',
	'https://www.douban.com/',
	'https://www.douban.com/explore/',
	'https://www.douban.com/people/180693708/notes',
	'https://www.douban.com/people/80620968/notes',
	# 'https://www.thinkingtaiwan.com',
	# 'https://www.bbc.co.uk',
	# 'https://cn.nytimes.com',
	'https://www.nytimes.com',
	# 'https://www.bbc.com/zhongwen/simp',
]

def test():
	for site in tests:
		links = link_extractor.getLinks(site)
		for link, name in links:
			# with open(fn, 'a') as f:
			# 	f.write(name + ' ' + link + '\n')
			# print(name, link)
			...
		# with open(fn, 'a') as f:
		# 	f.write(str(len(links)) + '\n')
		# print(len(links))
		input()
	
if __name__=='__main__':
	test()