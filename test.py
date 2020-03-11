#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import link_extractor

def test():
	links = link_extractor.getLinks(
		'https://www.bbc.com/zhongwen/simp', domain='https://www.bbc.co.uk')
	for link, name in links:
		print(name, link)
	
if __name__=='__main__':
	test()