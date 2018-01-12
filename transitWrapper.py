import transloc
import re
import requests
import json
import bs4
import geopy.distance
import random


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

class track(object):
	#placeholder bot class - will eventually merge a ton of stuff into this
	def __init__(self, latitude, longitude, routeName=None, busName=None, stopName=None):
		self.longitude = longitude
		self.latitude = latitude
		self.listOfStops = []
		self.agencyInfo = getAllAgencyInfo()
		self.busName = busName
		if self.busName == None:
			self.busName = self.findBusName()
		self.busNumber = convertBusNameToNumber(self.busName)
		self.listOfRoutes = self.findRoutesFromLatLong()
		#the idea is that you pick one of these routes...
		self.routeNumber = self.chooseRoute()
		self.stopDatabase = self.findAllStops()
		self.stopName = stopName
		if self.stopName == None:
			self.stopName = self.findClosestStop()
		self.stopNumber = self.stopName['code']
		self.notifcationCount = 0
		self.notificationMessages = []
		self.checkForNewAnnouncements()
		print self.getArrivalTimes()

	def checkForNewAnnouncements(self):
		res = requests.get('https://{}.transloc.com/m/feeds/announcements'.format(self.busName), headers=headers)
		self.notificationCount = re.findall('total="(\d+)', str(res.text))[0]
		if self.notificationCount > 0:
			page = bs4.BeautifulSoup(res.text, 'lxml')
			for val in page.select('.announcement'):
				self.notificationMessages.append(val.getText().strip())

	#def generateNearbyRoutes(self):

	def findBusName(self):
		for busses in self.agencyInfo:
			if checkInBounds(self.latitude, self.longitude, busses['bounds']) == True:
				return busses['name']

	def findAllStops(self):
		return requests.get('https://feeds.transloc.com/3/stops?&agencies={}'.format(self.busNumber), headers=headers).json()['stops']


	def generateRouteStops(self):
		information = {}
		res = requests.get('https://{}.transloc.com/m/feeds/stops/{}'.format(self.busName, self.routeNumber)).text.split('<stop')
		for var in res:
			ID = extractXMLElem(var, 'id')
			if ID != None:
				information[ID] = {"Name": extractXMLElem(var, 'name'), "Code": extractXMLElem(var, 'code')}
		return information

	def returnClosestStopsNames(self, n=5):
		return self.listOfStops[:n]

	def returnStopCodeFromStopName(self, stopName):
		for var in self.allStops:
			if var['name'] == stopName:
				return var['code']

	def returnStopIDFromStopName(self, stopName):
		for var in self.allStops:
			if var['name'] == stopName:
				return var['id']

	def returnStopNameFromID(self, stopID):
		for var in self.allStops:
			if var['id'] == stopID:
				return var['name']

	def returnStopCodeFromID(self, stopID):
		for var in self.allStops:
			if var['id'] == stopID:
				return var['code']

	def returnStopNameFromCode(self, stopCode):
		for var in self.allStops:
			if var['code'] == stopCode:
				return var['name']

	def returnStopIDFromCode(self, stopCode):
		for var in self.allStops:
			if var['code'] == stopCode:
				return var['id']

	def checkIfRouteActive(self, routeName):
		for var in self.listOfRoutes:
			if var['long_name'] == routeName:
				if 'false' in str(var['is_active']):
					return False
				else:
					return True

	def findClosestStop(self):
		lowestDistance = -1
		closestStop = None
		coords1 = (self.latitude, self.longitude)
		for var in self.stopDatabase():
			coords2 = (var['position'][0], var['position'][1])
			self.listOfStops.append({"Data": var, "Name": var['name'], "Distance": geopy.distance.vincenty(coords1, coords2).miles})
		self.listOfStops = sorted(self.listOfStops, key=lambda k: k['Distance']) 
		return self.listOfStops[0]['Data']

	def findRoutesFromLatLong(self):
		listOfRoutes = []
		res = requests.get('https://feeds.transloc.com/3/routes?agencies={}'.format(self.busNumber), headers=headers).json()
		for val in res["routes"]:
			try:
				if checkInBounds(self.latitude, self.longitude, val['bounds']) == True:
					if len(val['long_name']) > 1:
						listOfRoutes.append(val)
			except:
				pass
		return listOfRoutes

	def chooseRoute(self):
		for i, route in enumerate(self.listOfRoutes):
			i = i + 1
			print("{} - {}".format(i, route['long_name']))
		return self.listOfRoutes[int(raw_input("Select Route: ")) - 1]['id']

	def getArrivalTimes(self):
		arrivalTimes = []
		#print 'https://{}.transloc.com/m/feeds/arrivals/route/{}'.format(self.busName, self.routeNumber)
		res = requests.get('https://{}.transloc.com/m/feeds/arrivals/route/{}'.format(self.busName, self.routeNumber), headers=headers).text.split('stop')
		for var in res:
			info = extractArrivalsAndID(var)
			if info != None:
				if info['ID'] == str(self.stopName['id']):
					arrivalTimes.append(info)
		return arrivalTimes




def convertBusNameToNumber(busName):
	print busName
	for val in getAllAgencyInfo():
		if val['name'] == busName:
			return val['id']

def getAllAgencyInfo():
	with open('agencyInfo.json') as json_data:
		return json.load(json_data)['agencies']
			
def extractXMLElem(string, element):
	try:
		return re.findall('{}="(.*?)"'.format(element), string)[0]
	except Exception as exp:
		return None

def extractLong(bounds):
	#longitude is usually negative
	return (bounds[1], bounds[3])

def extractLat(bounds):
	return (bounds[0], bounds[2])

def checkInBounds(latitude, longitude, bounds):
	lat1, lat2 = extractLat(bounds)
	long1, long2 = extractLong(bounds)
	if (lat1 <= latitude <= lat2) and (long1 <= longitude <= long2):
		return True
	else:
		return False

def extractID(string):
	ID = re.findall('id="(\d+)', str(string))
	if len(ID) != 0:
		return ID[0]
	else:
		return None

def extractArrivalsAndID(string):
	ID = extractID(string)
	if ID != None:
		arrivals = re.findall('arrivals="(.*?)"', str(string))[0]
		if arrivals != None:
			return {"ID": ID, "Arrivals": re.findall('\d+', str(arrivals))}
		else:
			return None
	else:
		return None

if __name__ == "__main__":
	CLEMSON_LAT, CLEMSON_LONG = 34.654340, -82.858492
	YALE_LAT, YALE_LONG = 41.312529, -72.922985
	a = track(CLEMSON_LAT, CLEMSON_LONG)