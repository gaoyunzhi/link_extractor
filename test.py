#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import link_extractor
import os

with open('example_sites.txt') as f:
	tests = [x for x in f.readlines() if x]
	tests = [x.strip() for x in tests if x.strip()]

def test():
	fn = 'result_2.txt'
	with open(fn, 'w') as f:
		f.write('')
	for site in tests:
		links = link_extractor.getLinks(site)
		for link in links:
			with open(fn, 'a') as f:
				f.write(link + '\n')
			print(link)
		with open(fn, 'a') as f:
			f.write(site + ' ' + str(len(links)) + '\n\n')
		print(site, len(links))
	
if __name__=='__main__':
	test()