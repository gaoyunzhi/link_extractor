#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import link_extractor

def test():
	links = link_extractor.getLinks(
		'https://www.bbc.com/zhongwen/simp', domain='https://www.bbc.co.uk')
	print(links)
	
if __name__=='__main__':
	test()