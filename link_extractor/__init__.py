#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'link_extractor'

from bs4 import BeautifulSoup
from telegram_util import matchKey
import cached_url
from datetime import date

def getItems(soup):
	for x in soup.find_all('div', class_='note-container'):
		item = x.find('a', title=True)
		item['href'] = x['data-url'] 
		yield item
	for x in soup.find_all('a', class_='title-link'):
		yield x
	for x in soup.find_all('a', class_='top-story'):
		yield x
	for x in soup.find_all():
		if not x.attrs:
			continue
		if 'Headline' not in str(x.attrs.get('class')):
			continue
		for y in x.find_all('a'):
			yield y
	year = '/' + date.today().strftime("%Y") + '/'
	for x in soup.find_all('a'):
		if 'href' not in x.attrs:
			continue
		link = x['href']
		if link.startswith(year) and link.endswith('html'):
			yield x
	for x in soup.find_all('a'):
		yield x 

def getName(item):
	if not item.text or not item.text.strip():
		return
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

def format(link, name, domain):
	if not '://' in link:
		link = domain + link
	if '#' in link:
		link = link[:link.find('#')]
	return link, name

def dedup(items):
	link_set = set()
	for l, n in items:
		if l in link_set:
			continue
		link_set.add(l)
		yield (l, n)

def getSortKey(x):
	index, link, name = x
	score = index
	if name and '代理服务器' in name:
		score = -1
	return score

def validSoup(item):
	if not item.attrs or 'href' not in item.attrs:
		return False
	if matchKey(str(item.attrs), ['footer-link']):
		return False
	return True

single_domain_list = ['https://squatting2047.com', 
	'https://matters.news/', 'https://wemp.app',
	'http://www.gzhshoulu.wang/', 'https://www.douban.com/']

def getLinks(webpage, domain=None):
	if not domain and webpage == 'https://www.bbc.com/zhongwen/simp':
		domain = 'https://www.bbc.co.uk'
	for single_domain in single_domain_list: # may need to revisit
		if not domain and single_domain in webpage:
			domain = single_domain
	if not domain:
		domain = webpage
	soup = BeautifulSoup(cached_url.get(webpage), 'html.parser')
	items = getItems(soup)
	items = [x for x in items if validSoup(x)]
	items = [(x['href'], getName(x)) for x in items]
	items = [format(link, name, domain) for link, name in items]
	items = [(link, name) for link, name in items if valid(link, name, domain)]
	items = dedup(items)
	items = sorted([(index, link, name) for index, (link, name) in enumerate(items)], 
		key=getSortKey)
	return [(link, name) for (index, link, name) in items]
