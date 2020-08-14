#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'link_extractor'

from telegram_util import matchKey
from .util import containYear, containNumber, getDetails, hasSignature
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

def formatRawLink(link, domain):
	if not link:
		return
	if domain not in link and 'http' in link:
		return
	link = link.strip().lstrip('/')
	for char in '#?':
		link = link.split(char)[0]
	parts = set(link.split('/'))
	for key, sub_config in config.items():
		if key in domain:
			must_contain_parts = sub_config.get('must_contain_parts')
			if must_contain_parts and not (set(must_contain_parts) & parts):
				return
			not_contain = sub_config.get('not_contain')
			if not_contain and matchKey(link, not_contain):
				return
			if sub_config.get('signature') and not hasSignature(link):
				return
	return link

def getSig(link):
	parts = set(link.split('/'))
	details = set(getDetails(link))
	sig = [len(parts), 'http' in link, 
		containYear(link), containNumber(link)]
	if (parts & set(['a', 'p', 'content']) or 
			details & set(['newsDetail'])):
		return tuple([0] + sig)
	if sig[2]:
		return tuple([1] + sig)
	if sig[3]:
		return tuple([2] + sig)
	if (sig[1] and sig[0] > 4) or sig[0] > 1:
		return tuple([3] + sig)
	return tuple([4] + sig)

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
	for target in range(4):
		for size, sig in bucket:
			if sig[0] == target and size > 2:
				return sig
	for size, sig in bucket:
		return sig
	return (0, False, False, False) # shouldn't be here

def sigMatch(sigModel, sig):
	return (sigModel[:3] == sig[:3] and ((not sigModel[3]) or sig[3]) and 
		((not sigModel[4]) or sig[4]))

def getLinks(site):
	if 'vocus.cc' in site:
		return getVocusLinks(site)
	soup = getSoup(site)
	links = list(yieldLinks(soup))
	domain = site.split('/')[2]
	links = [formatRawLink(link, domain) for link in links]
	# dedup, keep order
	links = [link for link in OrderedDict.fromkeys(links) if link]
	if '.douban.' in site:
		return getDoubanLinks(site, links, soup)
	Prefered_sig = getPreferedSig(links, site)
	links = [link for link in links if sigMatch(Prefered_sig, getSig(link))]
	return links