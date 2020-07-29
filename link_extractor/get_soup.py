from bs4 import BeautifulSoup
import cached_url

offtopic_tags = ['nav', 'footer', 'aside', 'header']

def getSoup(site):
	soup = BeautifulSoup(cached_url.get(site), 'html.parser')
	for item in soup.find_all('a', rel='author'):
		item.decompose()
	for tag in offtopic_tags:
		for item in soup.find_all(tag):
			item.decompose()
	for item in soup.find_all():
		if item.attrs and 'footer' in str(item.attrs):
			item.decompose()
	return soup