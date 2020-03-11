from bs4 import BeautifulSoup
import readee

def fact():
	return BeautifulSoup("<div></div>", features="lxml")

def getArticleHtml(name, link, index_loc):
	soup = readee.export(link)
	funcs = [
		lambda x: x.find('div', {'property': 'articleBody'}),
		lambda x: x.find('article'),
		lambda x: x.find('div', {'id': 'story-body'}),
	]
	for f in funcs:
		new_soup = f(soup)
		if new_soup:
			soup = new_soup
	for item in soup.find_all('h2'):
		new_item = fact().new_tag('h4')
		new_item.string = item.text
		item.replace_with(new_item)
	if len(soup.text) < 100:
		return
	return '''
<html>
	<body>
		<title>%s</title>
		<h1>%s</h1>
		<div><a href="%s">返回目录</a></div>
		%s
		<div><br/><a href="%s">原文</a></div>
		<div><br/><a href="%s">返回目录</a></div>
	</body>
</html>
	''' % (name, name, index_loc, str(soup), link, index_loc)