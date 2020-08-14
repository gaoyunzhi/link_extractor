def isYear(part):
	try:
		if 1990 < int(part) < 2100:
			return True
		if 19900000 < int(part) < 21000000:
			return True
	except:
		...
	return False

def containYear(link):
	for part in link.split('/'):
		if isYear(part):
			return True
	return False

def hasSignature(link):
	return link[-13:][:1] == '-'