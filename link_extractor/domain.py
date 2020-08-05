single_domain_list = ['https://matters.news/', 'https://wemp.app',
	'http://www.gzhshoulu.wang/', 'https://www.douban.com/', 
	'https://medium.com/', 'http://zhishifenzi.com', 
	'https://ed.ted.com/', 'https://www.thepaper.cn', 
	'https://opinion.udn.com', 'https://www.twreporter.org/',
	'https://chuansongme.com']

def getDomain(site):
	if site == 'https://www.bbc.com/zhongwen/simp':
		return 'https://www.bbc.co.uk'
	for single_domain in single_domain_list:
		if single_domain in site:
			return single_domain
	return site

def getPrefix(site):
	if 'matters.news' in site:
		return site
	return getDomain(site)

def hasPrefix(link, site):
	prefix = getPrefix(site)
	if (link.strip('/') == prefix.strip('/') or 
		link.strip('/') == site.strip('/')):
		return False
	return prefix in link