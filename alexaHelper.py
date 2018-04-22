import requests
from geopy.geocoders import GoogleV3
geolocator = GoogleV3(api_key='AIzaSyDBZre20-q9hSY0BFXTqmiZr5-orJSuwr0')
import display
def convertLatLong(address):
	a = geolocator.geocode(address)
	return {"Latitude": a.latitude, "Longitude": a.longitude}

def extractLatLong(event, context):
	try:
		deviceID = event["context"]["System"]['device']['deviceId']
	except:
		deviceID = "Test"
	try:
		key = event["context"]["System"]['apiAccessToken']
	except:
		key = ""
		deviceID = "Test"
	# This returns a dictionary object
	headers = {'Host': 'api.amazonalexa.com', 'Accept': 'application/json', 'Authorization': "Bearer {}".format(key)}
	url = 'https://api.amazonalexa.com/v1/devices/{}/settings/address'.format(deviceID)
	res = requests.get(url, headers=headers).json()
	return convertLatLong(res["addressLine1"] + " " + res["city"] + " " + res['stateOrRegion'])


def returnTestDisplay(e=['test', 'test']):
	return {
		"version": "1.0",
		"sessionAttributes": {},
		"response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "Thanks for checking out the clemson university bus tracker by Christopher Lambert.  You can ask me to find the closest bus stop or you can find time estimates for the Clemson University bus system"
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
                            "url": display.genMap(tuple(e))
                        }]
                    },
                    "title": "Hurricane Center",
                    "textContent": {
                        "primaryText": {
                            "text": "{} - {}".format(str(e[0]), str(e[1])),
                            "type": "PlainText"
                        }
                    }
                }
            }],
            "shouldEndSession": False
        }}

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

def devInfo(text=None):
	if text == None:
		text = "created in December 2017 by Christopher Lambert.  This alexa skill is completely open sourced.  Please check out the skill on Git Hub or contact me for more information"
	return returnSpeech(text)

def get_welcome_response(skillName, initialSpeech, repeatSpeech):
	session_attributes = {}
	card_title = skillName
	speech_output = initialSpeech
	reprompt_text = repeatSpeech
	should_end_session = False
	return build_response(session_attributes, build_speechlet_response(
		card_title, speech_output, reprompt_text, should_end_session))

def build_response(session_attributes, speechlet_response):
	return {
		"version": "1.0",
		"sessionAttributes": session_attributes,
		"response": speechlet_response
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

def get_help_response(helpText):
	return returnSpeech(helpText, False)

def handle_session_end_request(text="Exiting now..."):
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
