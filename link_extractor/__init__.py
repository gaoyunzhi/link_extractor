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

def getItemText(item):
	if not item or not item.text:
		return ''
	return ' '.join(item.text.strip().split())

def getName(item):
	for tag in ['p', 'span']:
		text = getItemText(item.find(tag))
		if text:
			return text
	return getItemText(text)

def isValidLink(link):
	parts = link.strip('/').split('/')
	if len(parts) <= 5:
		return False
	if set(parts) & set(['video', 'location', 'interactive']):
		return False
	return True

def formatLink(link, domain):
	if '://' not in link:
		link = domain + link
	for char in '#?':
		link = link.split(char)[0]
	return link

def getLink(item, domain):
	if not item.attrs or 'href' not in item.attrs:
		return
	link = formatLink(item['href'], domain)
	if not domain in link or not isValidLink(link):
		return
	if matchKey(link, ['.nytimes.', '.bbc.']) and not getName(item):
		return
	return link

def format(items, domain):
	existing = set()
	for item in items:
		link = getLink(item, domain)
		if not link or link in existing:
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
