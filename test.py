#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import link_extractor
import msvcrt as m

tests = [
	'http://tagesschau.de',
	'http://www.gzhshoulu.wang/account_PourMarx.html',
	'https://cn.nytimes.com',
	'https://jacobinmag.com/',
	'https://matters.news/@Margaux1848',
	'https://matters.news/@zoezhao',
	'https://squatting2047.com',
	'https://wemp.app/accounts/12c2c49c-305d-4de3-85c8-00d372e7a47a',
	'https://www.bbc.co.uk',
	'https://www.bbc.com/zhongwen/simp',
	'https://www.douban.com/',
	'https://www.douban.com/explore/',
	'https://www.douban.com/people/180693708/notes',
	'https://www.douban.com/people/80620968/notes',
	'https://www.nytimes.com',
]

def test():
	for site in tests:
		links = link_extractor.getLinks(site)
		for link, name in links:
			print(name, link)
		print(len(links))
		m.getch()
	
if __name__=='__main__':
	test()