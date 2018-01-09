import requests
import bs4
import re

def grabAnnouncements(busName):
	announcements = []
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	res = requests.get('https://{}.transloc.com/m/announcements'.format(busName), headers=headers)
	page = bs4.BeautifulSoup(res.text, 'lxml')
	for val in page.select('.announcement'):
		announcements.append(val.getText().strip())
	return announcements

def grabCurrentRoutes(busName):
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	res = requests.get('https://{}.transloc.com/m/feeds/index'.format(busName), headers=headers)
	return re.findall('id="(\d+)', str(res.text))

print grabCurrentRoutes('catbus')