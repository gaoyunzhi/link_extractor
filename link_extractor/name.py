def getItemText(item):
	if not item or not item.text:
		return ''
	return ' '.join(item.text.strip().split())

def getName(item):
	for tag in ['p', 'span']:
		text = getItemText(item.find(tag))
		if text:
			return text
	return getItemText(item)