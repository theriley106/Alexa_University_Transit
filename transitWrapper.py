import transloc
import re
import requests
import json

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

class track(object):
	#placeholder bot class - will eventually merge a ton of stuff into this
	def __init__(self, longitude, latitude, busName=None, stopName=None):
		self.longitude = longitude
		self.latitude = latitude
		self.busName = busName
		self.stopName = stopName
		self.notifcationCount = 0
		self.notificationMessages = []

	def checkForNewAnnouncements(self):
		res = requests.get('https://{}.transloc.com/m/feeds/announcements'.format(self.busName), headers=headers)
		self.notificationCount = re.findall('total="(\d+)', str(res.text))[0]
		if self.notificationCount > 0:
			page = bs4.BeautifulSoup(res.text, 'lxml')
			for val in page.select('.announcement'):
				self.notificationMessages.append(val.getText().strip())



def convertBusNameToNumber(busName):
	for val in getAllAgencyInfo():
		if val['name'] == busName:
			return val['id']

def getAllAgencyInfo():
	with open('agencyInfo.json') as json_data:
		return json.load(json_data)['agencies']
			
