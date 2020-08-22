#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'link_extractor'

from telegram_util import matchKey
from .util import containYear, hasSignature
from .get_soup import getSoup
from .douban import getDoubanLinks
from .vocus import getVocusLinks
from collections import OrderedDict
import pkg_resources
import yaml

config = pkg_resources.resource_string(__name__, 'config.yaml')
config = yaml.load(config, Loader=yaml.FullLoader)

def yieldLinks(soup):
	for note in soup.find_all('div', class_='note-container'): # douban notes
		yield note.get('data-url')
	for item in soup.find_all('a', class_='top-story'): # bbc sorting
		yield item.get('href')
	for container in soup.find_all(): # bbc china sorting
		if container.attrs and 'Headline' in str(container.attrs.get('class')):
			for item in container.find_all('a'):
				yield item.get('href')
	for item in soup.find_all('a'):
		if 'newsDetail_forward' in str(item) and 'tiptitleImg' not in str(item):
			continue
		yield item.get('href')
	for item in soup.find_all('div'):
		yield item.get('data-link')

def formatRawLink(link, domain):
	if domain.startswith('cn.'):
		domain = domain[3:]
	if not link:
		return
	link = link.strip().lstrip('/')
	for char in '#?':
		link = link.split(char)[0]
	if domain not in link and 'http' in link:
		return
	parts = set(link.split('/'))
	for key, sub_config in config.items():
		if key in domain:
			must_contain_part = sub_config.get('must_contain_part')
			if must_contain_part and must_contain_part not in parts:
				return
			not_contain = sub_config.get('not_contain')
			if not_contain and matchKey(link, not_contain):
				return
			sig_len = sub_config.get('sig_len')
			if sig_len and not hasSignature(link, sig_len):
				return
			must_contain = sub_config.get('must_contain')
			if must_contain and must_contain not in link:
				return
	return link

def getSig(link):
	parts = link.split('/')
	sig = [len(parts), 'http' in link, containYear(link)]
	if sig[2]:
		return tuple([0] + sig)
	if (sig[1] and sig[0] > 4) or sig[0] > 1:
		return tuple([1] + sig)
	return tuple([2] + sig)

def getPreferedSig(links, site):
	dic = {}
	for link in links:
		sig = getSig(link)
		if sig in dic:
			dic[sig].append(link)
		else:
			dic[sig] = [link]
	bucket = [(len(dic[sig]), sig) for sig in dic]
	bucket.sort(reverse=True)
	for target in range(2):
		for size, sig in bucket:
			if sig[0] == target and size > 2:
				return sig
	for size, sig in bucket:
		return sig
	return (0, False, False, False) # shouldn't be here

def sigMatch(sigModel, sig):
	return sigModel[:3] == sig[:3] and ((not sigModel[3]) or sig[3])

def populateDomain(link, site):
	if 'http' in link:
		return link
	if link.startswith('zhuanlan.zhihu.com'):
		return 'https://' + link
	return '/'.join(site.split('/')[:3] + [link])

def getLinks(site):
	if 'vocus.cc' in site:
		return getVocusLinks(site)
	soup = getSoup(site)
	links = list(yieldLinks(soup))
	links = [formatRawLink(link, site.split('/')[2]) for link in links]
	# dedup, keep order
	links = [link for link in OrderedDict.fromkeys(links) if link]
	if '.douban.' in site:
		return getDoubanLinks(site, links, soup)
	prefered_sig = getPreferedSig(links, site)
	links = [populateDomain(link, site) for 
		link in links if sigMatch(prefered_sig, getSig(link))]
	if 'cn.nytimes.com/opinion' in site:
		return links[:3]
	return links