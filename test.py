#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import link_extractor

def test():
	links = link_extractor.getLinks(
		'https://www.douban.com')
		# 'https://www.douban.com/people/180693708/notes')
		# 'http://www.gzhshoulu.wang/account_PourMarx.html')
		# 'https://wemp.app/posts/8ee508d2-592d-479d-9d1d-4b76a10e5442')
		# 'https://squatting2047.com/page/2')
		# 'https://www.bbc.com/zhongwen/simp', domain='https://www.bbc.co.uk')
		# 'https://cn.nytimes.com')
		# 'https://www.bbc.co.uk')
		# 'https://www.nytimes.com')
		# 'https://whogovernstw.org')
		# 'https://www.thinkingtaiwan.com')
		# 'https://matters.news/')
	for link, name in links:
		print(name, link)
	print(len(links))
	
if __name__=='__main__':
	test()