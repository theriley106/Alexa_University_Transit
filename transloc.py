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
	ID = extractID(string)
	if ID != None:
		if len(ID) > 2:
			try:
				label = re.findall('label="(.*?)"', str(string))[0]
			except:
				label = "UNKNOWN"
		return (ID, label)
	else:
		return (None, None)

def extractID(string):
	ID = re.findall('id="(\d+)', str(string))
	if len(ID) != 0:
		return ID[0]
	else:
		return None

def extractArrivalFromString(string):
	arrivals = re.findall('arrivals="(.*?)"', str(string))
	if len(arrivals) != 0:
		arrivals = arrivals[0]
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

def convertBusNameToNumber(busName):
	for val in getAllAgencyInfo():
		if val['name'] == busName:
			return val['id']


def findRoutesFromLatLong(latitude, longitude, busName=None):
	if busName == None:
		busName = findByLatLong(latitude, longitude)
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	res = requests.get('https://feeds.transloc.com/3/routes?agencies={}'.format(convertBusNameToNumber(busName)), headers=headers).json()
	for val in res["routes"]:
		if checkInBounds(latitude, longitude, val['bounds']) == True:
			return val


def trackByRouteNumber(busName, routeNum):
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	res = requests.get("https://{}.transloc.com/m/route/{}#list".format(busName, routeNum), headers=headers)

def getArrivalTimes(busName, routeNum):
	arrivalTimes = []
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	res = requests.get('https://{}.transloc.com/m/feeds/arrivals/route/{}'.format(busName, routeNum), headers=headers).text.split('stop')
	for var in res:
		info = extractArrivalsAndID(var)
		if info != None:
			arrivalTimes.append(info)
	return arrivalTimes

def findByLatLong(latitude, longitude):
	for busses in DATABASE:
		if checkInBounds(latitude, longitude, busses['bounds']) == True:
			return busses['name']
	
def getAllAgencyInfo():
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	res = requests.get('https://feeds.transloc.com/agencies?', headers=headers)
	return res.json()['agencies']

def returnInfoByName(busName):
	for value in DATABASE:
		if value['name'] == busName:
			return value

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

def extractXMLElem(string, element):
	try:
		return re.findall('{}="(.*?)"'.format(element), string)[0]
	except Exception as exp:
		return None

def genStopDict(busName, routeNum):
	information = {}
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	print 'https://{}.transloc.com/m/feeds/stops/{}'.format(busName, routeNum)
	res = requests.get('https://{}.transloc.com/m/feeds/stops/{}'.format(busName, routeNum)).text.split('<stop')
	for var in res:
		ID = extractXMLElem(var, 'id')
		if ID != None:
			information[ID] = {"Name": extractXMLElem(var, 'name'), "Code": extractXMLElem(var, 'code')}
		#print ID
	return information



if __name__ == "__main__":
	DATABASE = getAllAgencyInfo()
	#print returnInfoByName('yale')
	#busSystem = 
	#print 
	var = findByLatLong(41.312529, -72.922985)
	print var
	routes = findRoutesFromLatLong(41.312529, -72.922985)['id']
	print routes
	stopDict = genStopDict(var, routes)
	for var in getArrivalTimes(var, routes):
		print("The Bus at {} will arrive in {} minutes".format(stopDict[str(var['ID'])]['Name'], str(var['Arrivals'])))
