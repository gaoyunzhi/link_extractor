from telegram_util import matchKey

def getDoubanId(link):
	if not matchKey(link, ['note', 'group/topic', 'status', 'album']):
		return
	parts = link.split('/')
	for part in parts[:-1]:
		try:
			int(part)
			return part
		except:
			...

def countLike(link, soup):
	douban_id = getDoubanId(link)
	result = 0
	for item in soup.find_all():
		if item.attrs and douban_id in str(item.attrs):
			result += int(item.get('data-count', 0))
	return result

def sortDouban(links, soup):
	counted_items = [(countLike(link, soup), link) for link in links
		if getDoubanId(link)]
	counted_items.sort(reverse = True)
	return [(item[1], item[0]) for item in counted_items]