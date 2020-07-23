def getCount(item):
	view = item.parent.find('p', class_='tdd-lcard__views')
	if not view:
		return 0
	return int(''.join(view.text.strip().split()[0].split(',')))

def sortTed(items):
	counted_items = []
	for link, item in items:
		counted_items.append((getCount(item), link))
	counted_items.sort(reverse = True)
	return [(item[1], item[0]) for item in counted_items[:20]]