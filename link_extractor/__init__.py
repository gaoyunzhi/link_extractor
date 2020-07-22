#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'link_extractor'

from telegram_util import matchKey
from .domain import getDomain, hasPrefix
from .name import getName
from .util import hasYear, hasNumber
from .get_soup import getSoup
from .douban import sortDouban
from .vocus import getVocusLinks
from .blogspot import getFromBlogspot

def validSoup(item):
	# BBC filters
	return not matchKey(str(item), ['视频', '专题', 'Watch ', 'headlines'])

def isValidLink(link):
	parts = link.strip('/').split('/')

	if '.gzhshoulu.' in link:
		return 'article' in parts
	if '.douban.' in link:
		return (set(['note', 'status', 'album', 'topic']) & set(parts) and
			not set(['gallery']) & set(parts)) and hasNumber(parts)

	if set(['accounts', # wemp.app
			'interactive', 'briefing', 'podcasts', 'slideshow', # nyt
			'collections', 'sport', # bbc
			'guaishi', # chinaworker
			]) & set(parts):
		return False

	if 'jacobinmag.' in link and len(parts) < 6:
		return False
	if '.nytimes.' in link:
		return 'topic' not in parts and hasYear(parts)
	if 'matters.news' in link:
		return len(parts) == 5
	if 'zhishifenzi' in link:
		return len(parts) == 6
	if '.thinkingtaiwan.' in link:
		return 'content' in parts
	if matchKey(link, ['chinaworker.', 'pinknews.', 
			'colgatefeminism', 'thesocietypages']):
		return hasYear(parts)
	if 'medium' in link:
		return parts[-1][-13:][:1] == '-'
	return True

# deal with sorting for bbc and nyt, no need for other sites
def genItems(soup): 
	for note in soup.find_all('div', class_='note-container'): # douban notes
		item = note.find('a', title=True)
		item['href'] = note['data-url'] 
		yield item
	for item in soup.find_all('a', class_='top-story'): # bbc sorting
		yield item
	for container in soup.find_all(): # bbc china sorting
		if container.attrs and 'Headline' in str(container.attrs.get('class')):
			for item in container.find_all('a'):
				yield item
	for item in soup.find_all('a'):
		yield item 

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
	if 'vocus.cc' in site:
		return getVocusLinks(site)
	if 'realfeministphilosophers.blogspot' in site:
		return list(getFromBlogspot(site))
	soup = getSoup(site)
	items = genItems(soup)
	items = [x for x in items if validSoup(x)]
	items = format(items, site)
	if '.douban.' in site:
		return sortDouban(items, soup)
	if 'pinknews' in site:
		items = list(items)[:14]
	return [(link, getName(item)) for (link, item) in items]
