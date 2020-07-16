import cached_url
import yaml

def getVocusLinks(site):
	pid = site.split('.cc/')[1].split('/')[0]
	api_link = 'https://api.sosreader.com/api/articles?publicationId=' + pid
	content = yaml.load(cached_url.get(api_link), Loader=yaml.FullLoader)
	result = []
	for article in content.get('articles'):
		result.append((int(article.get('likeCount', 0)), 
			'https://vocus.cc/' + pid + '/' + article.get('_id')))
	result.sort(reverse=True)
	return [(item[1], item[0]) for item in result]
