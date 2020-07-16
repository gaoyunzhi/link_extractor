import cached_url
import yaml

def getVocusLinks(site):
	pid = site.split('.cc/')[1].split('/')[0]
	api_link = 'https://api.sosreader.com/api/articles?publicationId=' + pid
	cached_url.get(api_link)
	return []