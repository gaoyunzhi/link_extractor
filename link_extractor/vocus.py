import cached_url
import yaml

def getVocusLinks(site):
	pid = site.split('.cc/')[1].split('/')[0]
	api_link = 'https://api.sosreader.com/api/articles?publicationId=' + pid
	content = yaml.load(cached_url.get(api_link), Loader=yaml.FullLoader)
	return ['https://vocus.cc/' + pid + '/' + article.get('_id') for 
		article in content.get('articles')]
