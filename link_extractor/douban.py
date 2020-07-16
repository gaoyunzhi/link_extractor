def getDoubanId(link):
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

def sortDouban(items, soup):
	counted_items = []
	for link, _ in items:
		counted_items.append((countLike(link, soup), link))
	counted_items.sort(reverse = True)
	return [(item[1], item[0]) for item in counted_items]