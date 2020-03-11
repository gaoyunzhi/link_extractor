#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'link_extractor'

from bs4 import BeautifulSoup
from telegram_util import matchKey
import cached_url
from datetime import date

def getItems(soup):
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
		if link.startswith(year) and link.endswith('html') and \
			not matchKey(link, ['podcast', 'briefing', 'topic']):
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

def valid(link, name, domain):
	if not domain in link:
		return False
	if not name:
		return False
	if matchKey(name, ['\n', '视频', '音频', 'podcasts', 'Watch video', 'Watch:', '专题', '专栏']):
		return False
	if len(name) < 5: # 导航栏目
		return False
	return True

def format(link, name, domain):
	if not '://' in link:
		link = domain + link
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
	if '代理服务器' in name:
		score = -1
	return score

def getLinks(webpage, domain):
	soup = BeautifulSoup(cached_url.get(webpage), 'html.parser')
	items = list(getItems(soup))
	items = [x for x in items if x.attrs and 'href' in x.attrs]
	items = [(x['href'], getName(x)) for x in items]
	items = [format(link, name, domain) for link, name in items]
	items = [(link, name) for link, name in items if valid(link, name, domain)]
	items = dedup(items)
	items = sorted([(index, link, name) for index, (link, name) in enumerate(items)], 
		key=getSortKey)
	return [(link, name) for (index, link, name) in items]
