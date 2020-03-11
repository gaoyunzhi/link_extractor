from datetime import date
from bs4 import BeautifulSoup
from telegram_util import cleanFileName

def getIndexHtml(news_source, links):
	today = date.today().strftime("%m%d")

	index_html = '''
<html>
   <body>
     <h1>今日新闻 %s %s</h1>
     <br/>
     <p style="text-indent:0pt">
     </p>
     <br/>
     <br/>
     <p style="text-indent:0pt">
     	来源：
     	<a href="https://t.me/news_pdf">新闻播报</a>
     </p>
     <p style="text-indent:0pt">
        <a href="https://github.com/gaoyunzhi/telegram_news_2_pdf_bot/tree/master/pdf_result">镜像</a>
     </p>
   </body>
</html>
	''' % (news_source.upper(), today)

	soup = BeautifulSoup(index_html, 'html.parser')
	content_list = soup.find('p')
	for name in links:
		item = '<a href="%s.html">%s</a>' % \
            (cleanFileName(name), cleanFileName(name))
		content_list.append(BeautifulSoup(item, 'html.parser'))
		content_list.append(BeautifulSoup('<br/><br/>', 'html.parser'))
	return str(soup)