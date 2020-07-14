#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'link_extractor'

from telegram_util import matchKey
from .domain import getDomain, hasPrefix
from .name import getName
from .util import hasYear
from .get_soup import getSoup

def validSoup(item):
	return not matchKey(str(item), ['footer-link', 
		'视频', '专题', 'Watch ', 'headlines'])

def isValidLink(link):
	parts = link.strip('/').split('/')

	if '.gzhshoulu.' in link:
		return 'article' in parts
	if '.douban.' in link:
		return set(['note', 'status', 'album', 'topic']) & set(parts)

	if set(['video', 'location', 'interactive', 'help', 'tools'
			'slideshow', 'accounts', 'page', 'category', 
			'collections', 'briefing', 'podcasts']) & set(parts):
		return False
	if matchKey(link, ['comment', 'follow']):
		return False

	if 'jacobinmag.' in link and len(parts) < 6:
		return False
	if '.nytimes.' in link:
		return 'topic' not in parts and hasYear(parts)

	return True

def genItems(soup):
	for x in soup.find_all('div', class_='note-container'): # douban notes
		item = x.find('a', title=True)
		item['href'] = x['data-url'] 
		yield item
	for x in soup.find_all('a'):
		yield x 

def formatLink(link, domain):
	if '://' not in link:
		link = domain.rstrip('/') + '/' + link.lstrip('/')
	for char in '#?':
		link = link.split(char)[0]
	return link

def getLink(item, site):
	if not item.attrs or 'href' not in item.attrs:
		return
	link = formatLink(item['href'], getDomain(site))

	if not hasPrefix(link, site) or not isValidLink(link):
		return

	if matchKey(link, ['.nytimes.', '.bbc.']) and not getName(item):
		return
	return link

def format(items, site):
	existing = set()
	for item in items:
		link = getLink(item, site)
		if not link or link in existing:
			continue
		yield link, item
		existing.add(link)

def getLinks(site):
	items = genItems(getSoup(site))
	items = [x for x in items if validSoup(x)]
	items = format(items, site)
	return [(link, getName(item)) for (link, item) in items]
