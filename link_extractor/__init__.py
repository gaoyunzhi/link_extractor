#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'link_extractor'

from bs4 import BeautifulSoup
from telegram_util import matchKey
import cached_url
from .domain import getDomain

def genItems(soup):
	for x in soup.find_all('div', class_='note-container'): # douban notes
		item = x.find('a', title=True)
		item['href'] = x['data-url'] 
		yield item
	for x in soup.find_all('a'):
		yield x 

def getName(item):
	if not item.text or not item.text.strip():
		return ''
	for x in ['p', 'span']:
		subitem = item.find(x)
		if subitem and subitem.text and subitem.text.strip():
			return subitem.text.strip()
	return item.text.strip()

def meaningfulCount(link, domain):
	for x in [domain, 'section', '/', 'spotlight', 'video', 'subscription', 'digital',
		'html', 'eduation', 'nav', 'left', 'right', 'correction', 'column', 'editorial',
		'opinion', 'newsletters']:
		link = link.replace(x, '')
	return len(link)

def valid(link, name, domain):
	if not domain in link:
		return False
	if 'thinkingtaiwan' in link:
		return '/content/' in link
	if meaningfulCount(link, domain) < 10:
		return False
	if 'matters.news' in link:
		if len([x for x in link.split('/') if x]) <= 3 or '@' not in link:
			return False
	if 'wemp.app' in link:
		if matchKey(link, ['accounts/']):
			return False 
	if matchKey(link, ['#', 'cookie-setting', 'podcast', 'briefing',
		'bbcnewsletter', 'help/web', '?', 'news-event', 'obituaries', '/author/',
		'hi176', '/category/', '/format/', '/channel/', '/location/',
		'/department/', '/series/', '/javascript', '/doulist/', '/partner/brand',
		'/gallery/topic', '/group/explore']):
		return False
	if not name:
		return False
	if matchKey(name, ['\n', '视频', '音频', 'podcasts', 'Watch video', 'Watch:', 
		'专题', '专栏', 'BBC中文', 'News 中文', '最多人阅读内容', 'Homepage', 'Radio',
		'Matters改版', '社区诉讼']):
		return False
	if '.douban.' in link:
		if matchKey(link, ['/event/', '/about/legal']):
			return False
		if link.strip('/').split('/')[-2] in ['people', 'group']:
			return False
		return True
	if matchKey(link, ['topic', '/people/']) or len(name) < 7: # 导航栏目
		return False
	return True

def formatLink(link, domain):
	if '://' not in link:
		link = domain + link
	return link.split('#')[0]

def format(items, domain):
	existing = set()
	for item in items:
		if not item.attrs or 'href' not in item.attrs:
			continue
		link = formatLink(item['href'], domain)
		if link in existing:
			continue
		yield link, item
		existing.add(link)

def validSoup(item):
	return not matchKey(str(item), ['footer-link', ])

def getLinks(webpage, domain=None):
	domain = getDomain(webpage, domain)
	soup = BeautifulSoup(cached_url.get(webpage), 'html.parser')
	items = genItems(soup)
	items = [x for x in items if validSoup(x)]
	items = format(items, domain)
	return [(link, getName(item)) for (link, item) in items]
