#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'link_extractor'

from telegram_util import matchKey
from .domain import getDomain, hasPrefix
from .name import getName
from .util import containYear, containNumber, getDetails
from .get_soup import getSoup
from .douban import getDoubanLinks
from .vocus import getVocusLinks
from .ted import sortTed
from collections import OrderedDict

def validSoup(item):
	if 'newsDetail_forward' in str(item): # the paper filters
		return 'tiptitleImg' in str(item)
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

	if matchKey(link, ['whats-current']): # feministcurrent
		return False
	if 'feministcurrent' in link and matchKey(link, ['podcast']):
		return False

	if 'jacobinmag.' in link and len(parts) < 6:
		return False
	if '.nytimes.' in link:
		return 'topic' not in parts and hasYear(parts)
	if 'cnpolitics' in link:
		return hasYear(parts)
	if matchKey(link, ['matters.news', 'chuansongme.com']):
		return len(parts) == 5
	if matchKey(link, ['zhishifenzi']):
		return len(parts) == 6
	if matchKey(link, ['shityoushouldcareabout']):
		return len(parts) == 8
	if 'opinion.udn.com' in link:
		return 'page' not in parts and len(parts) == 7
	if 'twreporter.org' in link:
		return 'a' in parts and len(parts) == 5
	if 'zhihu.' in link:
		return 'p' in parts
	if '.thinkingtaiwan.' in link:
		return 'content' in parts
	if matchKey(link, ['chinaworker.', 'pinknews.', 
			'colgatefeminism', 'thesocietypages', 'feministcurrent']):
		return hasYear(parts)
	if 'medium' in link:
		return parts[-1][-13:][:1] == '-'
	if '.thepaper.' in link:
		return 'newsDetail_forward_' in link
	return True

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

def formatLink(link, domain):
	if '://' not in link:
		link = domain.rstrip('/') + '/' + link.lstrip('/')
	for char in '#?':
		link = link.split(char)[0]
	return link.strip()

def formatRawLink(link, domain):
	if not link:
		return
	if domain not in link and 'http' in link:
		return
	link = link.strip().lstrip('/')
	for char in '#?':
		link = link.split(char)[0]
	parts = set(link.split('/'))
	if '.zhihu.' in domain and (not set(['p']) & parts):
		return 
	if 'feministcurrent' in domain and matchKey(link, ['podcast', 'whats-current']):
		return
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
	# if 'douban.' in domain and (set(['channel', 'doulist', 'location', 'group', 'event']) & parts):
	# 	return

def getLinksOld(site):
	if '.douban.' in site:
		return sortDouban(items, soup)
	if 'cn.nytimes.com/opinion' in site:
		items = list(items)[:3] # may need to revisit later
	if 'ed.ted.com' in site:
		return sortTed(items)
	return [(link, getName(item)) for (link, item) in items]
