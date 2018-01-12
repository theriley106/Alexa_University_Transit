import requests
import re
from geopy.geocoders import GoogleV3
from geopy.distance import vincenty
geolocator = GoogleV3(api_key='AIzaSyDBZre20-q9hSY0BFXTqmiZr5-orJSuwr0')


def returnLatLong(busNumber):
	res = requests.get('https://catbus.transloc.com/m/feeds/vehicles/{}'.format(busNumber))
	string = str(res.text)
	a = string.partition('lat="')[2].partition('"')[0]
	b = string.partition('lng="')[2].partition('"')[0]
	return (a, b)

def convertLatLong(address):
	a = geolocator.geocode(address)
	return (a.latitude, a.longitude)
	
def createResponse(busNumber, distance=0, oos=False, location=None):
	if oos == True:
		return {
				"version": "1.0",
				"sessionAttributes": {},
				"response": {
				"outputSpeech": {
				"type": "PlainText",
				"text": "It looks like bus number {} is out of service at the moment".format(busNumber)
					},
					"shouldEndSession": True
				  }
				}
	else:
		return {
				"version": "1.0",
				"sessionAttributes": {},
				"response": {
				"outputSpeech": {
				"type": "PlainText",
				"text": "The bus is currently {} miles from your location in {}".format(str(distance), str(location))
					},
					"shouldEndSession": True
				  }
				}
		

def lambda_handler(event, context):
	deviceID = event["context"]["System"]['device']['deviceId']
	key = event["context"]["System"]['apiAccessToken']
	headers = {'Host': 'api.amazonalexa.com', 'Accept': 'application/json', 'Authorization': "Bearer {}".format(key)}
	url = 'https://api.amazonalexa.com/v1/devices/{}/settings/address'.format(deviceID)
	res = requests.get(url, headers=headers).json()
	print res
	busLatLong = returnLatLong(4010054)
	if len(str(busLatLong[0])) < 2:
		return createResponse(4010054, oos=True)
	myAddress = convertLatLong(res["addressLine1"] + " " + res["city"] + " " + res['stateOrRegion'])
	distance = vincenty(myAddress, busLatLong).miles
	distance = str(int(float(re.findall("\d+\.\d+", str(distance))[0])))
	return createResponse(4010054, distance=distance, location=res["city"])
	
	

#vincenty((34.7189472, -82.3064414), (34.6708859002, -82.8352496018))