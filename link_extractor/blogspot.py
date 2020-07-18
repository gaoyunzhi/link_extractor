import cached_url
import yaml

def getFromBlogspot(site):
	link = site.strip('/') + '/feeds/posts/default?alt=json'
	content = yaml.load(cached_url.get(link), Loader=yaml.FullLoader)
	for item in content['feed']['entry']:
		yield item['link'][4]['href'], None
