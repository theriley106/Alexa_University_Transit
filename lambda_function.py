import random
import re
from geopy.geocoders import GoogleV3
import requests
from geopy.distance import vincenty
import alexaHelper
geolocator = GoogleV3(api_key='AIzaSyDBZre20-q9hSY0BFXTqmiZr5-orJSuwr0')
import transitWrapper
import display

def lambda_handler(event, context):
	if event["request"]["type"] == "LaunchRequest":
		locationInfo = alexaHelper.extractLatLong(event, context)

		return alexaHelper.returnTestDisplay([locationInfo['Longitude'], locationInfo["Latitude"]])
		return on_launch(event["request"], event["session"])
	elif event["request"]["type"] == "IntentRequest":
		locationInfo = alexaHelper.extractLatLong(event, context)
		return on_intent(event["request"], event["session"], locationInfo=locationInfo)
	else:
		handle_session_end_request()

def on_launch(launch_request, session):
	return get_welcome_response()

def longLat(deviceID, apiKey):
	headers = {'Host': 'api.amazonalexa.com', 'Accept': 'application/json', 'Authorization': "Bearer {}".format(apiKey)}
	print deviceID
	print apiKey
	url = 'https://api.amazonalexa.com/v1/devices/{}/settings/address'.format(deviceID)
	res = requests.get(url, headers=headers).json()

	print res
	return convertLatLong(res["addressLine1"] + " " + res["city"] + " " + res['stateOrRegion'])

def nearbyBusses(deviceID, apiKEY):
	headers = {'Host': 'api.amazonalexa.com', 'Accept': 'application/json', 'Authorization': "Bearer {}".format(apiKEY)}
	url = 'https://api.amazonalexa.com/v1/devices/{}/settings/address'.format(deviceID)
	res = requests.get(url, headers=headers).json()
	try:
		myAddress = convertLatLong(res["addressLine1"] + " " + res["city"] + " " + res['stateOrRegion'])
	except Exception as exp:
		print exp
		myAddress = None
	a = transitWrapper.track(myAddress[0], myAddress[1])
	routesNearMe = []
	activeRoutes = a.returnNearbyActiveRoutes()
	for i, val in enumerate(activeRoutes):
		if i == len(activeRoutes) - 1 and len(activeRoutes) > 1:
			routesNearMe.append("and " + val['long_name'])
		else:
			routesNearMe.append(val['long_name'])
	if len(activeRoutes) > 1:
		text = 'There are {} busses running near your location.  {}'.format(len(routesNearMe), ' '.join(routesNearMe))
	else:
		text = 'There is 1 bus running near your location.  The route is entitled {}'.format(routesNearMe[0])
	return {
				"version": "1.0",
				"sessionAttributes": {},
				"response": {
				"outputSpeech": {
				"type": "PlainText",
				"text": text
					},
					"shouldEndSession": True
				  }
				}

def testEnvironment():
	a = transitWrapper.track(agencyNum=639)
	routesNearMe = []
	activeRoutes = a.returnNearbyActiveRoutes()
	for i, val in enumerate(activeRoutes):
		if i == len(activeRoutes) - 1 and len(activeRoutes) > 1:
			routesNearMe.append("and " + val['long_name'])
		else:
			routesNearMe.append(val['long_name'])
	if len(activeRoutes) > 1:
		text = 'There are {} busses running near your location.  {}'.format(len(routesNearMe), ' '.join(routesNearMe))
	else:
		text = 'There is 1 bus running near your location.  The route is entitled {}'.format(routesNearMe[0])
	return {
				"version": "1.0",
				"sessionAttributes": {},
				"response": {
				"outputSpeech": {
				"type": "PlainText",
				"text": text
					},
					"shouldEndSession": True
				  }
				}

def convertVal(feet):
	if feet < 5280:
		return "{} Feet".format(str(int(feet)))
	else:
		return "{} Miles".format(int(feet) / 5280)

def nearbyStops(locationInfo):
	#return returnSpeech("{} {}".format(locationInfo["Latitude"], locationInfo["Longitude"]))
	try:
		a = transitWrapper.track(agencyNum=639, longitude=locationInfo["Longitude"], latitude=locationInfo["Latitude"])
		val = a.findClosestStop()
		distance = val["Distance"]
		try:
			name = val['Name']
			text = "It looks like there is a stop called {} that is {} from you.".format(name, convertVal(distance))
		except:
			text = "It looks like no nearby stops can be found.  This is usually caused by misconfigured location settings in the Alexa Skills app.  Please check that your address is correct by going to the settings menu in the Alexa Skills application.  If problems persist, you can set default Stop IDs by saying. set default stop. followed by the route ID found on the transloc website"
	except:
		text = 'function failed'
	return returnSpeech(text)
	return {
					"version": "1.0",
					"sessionAttributes": {},
					"response": {
					"outputSpeech": {
					"type": "PlainText",
					"text": text
						},
						"shouldEndSession": True
					  }
					}

def on_intent(intent_request, session, deviceID=None, apiKEY=None, locationInfo=None):
	intent = intent_request["intent"]
	intent_name = intent_request["intent"]["name"]
	if intent_name == "active_Busses_Clemson_Area_Transit":
		return nearbyBusses(deviceID, apiKEY)
	elif intent_name == 'distance_To_Stop_Clemson_Area_Transit':
		return nearbyStops(deviceID, apiKEY)
	elif intent_name == 'findStop':
		# This finds the nearest bus stop
		return nearbyStops(locationInfo)
	elif intent_name == 'test_Environment_Clemson_Area_Transit':
		return testEnvironment()
	elif intent_name == 'aboutDev':
		return alexaHelper.devInfo()
	elif intent_name == "AMAZON.HelpIntent":
		return get_help_response()
	elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
		return handle_session_end_request()

def returnSpeech(speech, endSession=True):
	return {
		"version": "1.0",
		"sessionAttributes": {},
		"response": {
		"outputSpeech": {
		"type": "PlainText",
		"text": speech
			},
			"shouldEndSession": endSession
		  }
		}

def get_help_response():
	output = "Please ask me to generate a scramble.  You can also ask about the Developer of this application.  What can I help you with?"
	return returnSpeech(output, False)


def get_welcome_response():
	return {
		"version": "1.0",
		"sessionAttributes": {},
		"response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "Test"
            },
            "directives": [{
                "type": "Display.RenderTemplate",
                "template": {
                    "type": "BodyTemplate1",
                    "token": "T123",
                    "backButton": "HIDDEN",
                    "backgroundImage": {
                        "contentDescription": "StormPhoto",
                        "sources": [{
                            "url": "https://s3.amazonaws.com/hurricane-data/hurricaneBackground.png"
                        }]
                    },
                    "title": "Hurricane Center",
                    "textContent": {
                        "primaryText": {
                            "text": "cardInfo",
                            "type": "PlainText"
                        }
                    }
                }
            }],
            "shouldEndSession": False
        }}
	session_attributes = {}
	card_title = "Transit Tracker"
	speech_output = "Thanks for checking out the clemson university bus tracker by Christopher Lambert.  You can ask me to find the closest bus stop or you can find time estimates for the Clemson University bus system"
	reprompt_text = "Thanks for checking out the clemson university bus tracker by Christopher Lambert.  You can ask me to find the closest bus stop or you can find time estimates for the Clemson University bus system"
	should_end_session = False
	return build_response(session_attributes, build_speechlet_response(
		card_title, speech_output, reprompt_text, should_end_session))

def build_response(session_attributes, speechlet_response):
	return {
		"version": "1.0",
		"sessionAttributes": session_attributes,
		"response": speechlet_response
	}

def handle_session_end_request():
	return {
	"version": "1.0",
	"sessionAttributes": {},
	"response": {
	"outputSpeech": {
	"type": "PlainText",
	"text": "Goodbye!"
		},
		"shouldEndSession": True
	  }
	}

def build_speechlet_response_without_card(output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_speechlet_response(title, output, reprompt_text, should_end_session):
	return {
		"outputSpeech": {
			"type": "PlainText",
			"text": output
		},
		"card": {
			"type": "Simple",
			"title": title,
			"content": output
		},
		"reprompt": {
			"outputSpeech": {
				"type": "PlainText",
				"text": reprompt_text
			}
		},
		"shouldEndSession": should_end_session
	}
