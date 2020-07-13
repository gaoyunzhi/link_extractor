single_domain_list = ['https://squatting2047.com', 
	'https://matters.news/', 'https://wemp.app',
	'http://www.gzhshoulu.wang/', 'https://www.douban.com/']

def getDomain(webpage, domain):
	if domain:
		return domain
	if webpage == 'https://www.bbc.com/zhongwen/simp':
		return 'https://www.bbc.co.uk'
	for single_domain in single_domain_list:
		if single_domain in webpage:
			return single_domain
	return webpage