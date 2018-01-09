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

def extractNumLabel(string):
	#this will extract the bus number and label from a string
	ID = re.findall('id="(\d+)', str(string))
	if len(ID) != 0:
		ID = ID[0]
		if len(ID) > 2:
			try:
				label = re.findall('label="(.*?)"', str(string))[0]
			except:
				label = "UNKNOWN"
		return (ID, label)
	else:
		return (None, None)
	

def grabCurrentRoutes(busName):
	information = []
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	res = requests.get('https://{}.transloc.com/m/feeds/index'.format(busName), headers=headers).text.split('<route')
	for value in res:
		busNum, label = extractNumLabel(value)
		if busNum != None:
			information.append({"ID": busNum, "Label": label})
	return information

def getAnnouncementCount(busName):
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	res = requests.get('https://{}.transloc.com/m/feeds/announcements'.format(busName), headers=headers)
	return re.findall('total="(\d+)', str(res.text))[0]

print grabCurrentRoutes('catbus')