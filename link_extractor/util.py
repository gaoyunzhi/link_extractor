def isYear(part):
	try:
		if 1990 < int(part) < 2100:
			return True
		if 19900000 < int(part) < 21000000:
			return True
	except:
		...
	return False

def hasYear(parts):
	for part in parts:
		if isYear(part):
			return True
	return False

def _hasNumber(part):
	if not part:
		return False
	part = part.split('-')[-1]
	try:
		int(part)
		return True
	except:
		...
	return False

def hasNumber(parts):
	for part in parts:
		if _hasNumber(part):
			return True
	return False