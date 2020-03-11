import os
from bs4 import BeautifulSoup
import yaml
from telegram_util import matchKey
import cached_url
from datetime import date

SOURCE = {
	'bbc': 'https://www.bbc.com/zhongwen/simp',
	'nyt': 'https://cn.nytimes.com',
	'bbc英文': 'https://www.bbc.co.uk',
	'nyt英文': 'https://www.nytimes.com',
	'菜市场政治学': 'https://whogovernstw.org',
}

DOMAIN = {
	'bbc': 'https://www.bbc.co.uk',
	'nyt': 'https://cn.nytimes.com',
	'bbc英文': 'https://www.bbc.co.uk',
	'nyt英文': 'https://www.nytimes.com',
	'菜市场政治学': 'https://whogovernstw.org',
}

def getItems(soup, news_source):
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

def getDomain(news_source):
	return DOMAIN[news_source]

def findName(item):
	if not item.text or not item.text.strip():
		return
	for x in ['p', 'span']:
		subitem = item.find(x)
		if subitem and subitem.text and subitem.text.strip():
			return subitem.text.strip()
	return item.text.strip()

def findLinks(news_source='bbc'):
	soup = BeautifulSoup(cached_url.get(SOURCE[news_source]), 'html.parser')
	links = {}
	domain = getDomain(news_source)
	link_set = set()
	for item in getItems(soup, news_source):
		name = findName(item)
		if not name:
			continue
		if matchKey(name, ['\n', '视频', '音频', 'podcasts', 'Watch video', 'Watch:', '专题', '专栏']):
			continue
		if len(name) < 5: # 导航栏目
			continue
		if len(links) > 10 and '代理服务器' not in name:
			continue
		links[name] = item['href'].strip()
		if not '://' in links[name]:
			links[name] =  domain +  links[name]
		if links[name] in link_set:
			del links[name]
		else:
			link_set.add(links[name])
	return links
