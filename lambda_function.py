import random
import re
from geopy.geocoders import GoogleV3
import requests
from geopy.distance import vincenty
geolocator = GoogleV3(api_key='AIzaSyDBZre20-q9hSY0BFXTqmiZr5-orJSuwr0')
import transitWrapper

Notation = ["R", "R'", "L", "L'", "U", "U'", "F", "F'", "B", "B'"]

def convertLatLong(address):
	a = geolocator.geocode(address)
	return (a.latitude, a.longitude)


def lambda_handler(event, context):
	deviceID = event["context"]["System"]['device']['deviceId']
	key = event["context"]["System"]['apiAccessToken']
	if event["request"]["type"] == "LaunchRequest":
		return on_launch(event["request"], event["session"])
	elif event["request"]["type"] == "IntentRequest":
		return on_intent(event["request"], event["session"], deviceID=deviceID, apiKEY=key)
	else:
		handle_session_end_request()
		
def on_launch(launch_request, session):
	return get_welcome_response()

def Generator(length):
	Scramble = []
	while len(Scramble) < length:
		Move = random.choice(Notation)
		MoveStr = " ".join(re.findall("[a-zA-Z]+", str(Move)))
		PreviousMove = Scramble[-1:]
		PreviousMove = " ".join(re.findall("[a-zA-Z]+", str(PreviousMove)))
		if MoveStr != PreviousMove:
			Num = random.randint(1,3)
			if Num == 1 or Num == 3:
				Scramble.append(Move)
			else:
				if "'" in str(Move):
					Move = str(Move).replace("'", "")
				Scramble.append('{}2'.format(Move))
	T = ""
	for moves in Scramble:
		T = T + " " + str(moves)
	return T
	
def returnScrambleResponse():
    scramble = Generator(25)
    response = ''
    moves = scramble.split(' ')
    for move in moves:
        response = response + str(' '.join(list(move))) + '. '
    response = response.replace("'", ' inverted ').replace('R', "Right").replace("L", "Left").replace("U", "Up").replace("D", "Down").replace("B", "Back").replace("F", "Front")
    if response[0] == '.':
        response = response[1:]
    return {
				"version": "1.0",
				"sessionAttributes": {},
				"response": {
				"outputSpeech": {
				"type": "PlainText",
				"text": response
					},
					"shouldEndSession": True
				  }
				}
				
def devInfo():
	text = "created in December 2017 by Christopher Lambert.  This alexa skill is completely open sourced.  Please check out the skill on Git Hub or contact me for more information"
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
    
    
	
def on_intent(intent_request, session, deviceID=None, apiKEY=None):
	intent = intent_request["intent"]
	intent_name = intent_request["intent"]["name"]
	if intent_name == "distance_To_Stop_Clemson_Area_Transit":
		headers = {'Host': 'api.amazonalexa.com', 'Accept': 'application/json', 'Authorization': "Bearer {}".format(apiKEY)}
		url = 'https://api.amazonalexa.com/v1/devices/{}/settings/address'.format(deviceID)
		res = requests.get(url, headers=headers).json()
		try:
			myAddress = convertLatLong(res["addressLine1"] + " " + res["city"] + " " + res['stateOrRegion'])
		except Exception as exp:
			print exp
			myAddress = None
		a = transitWrapper.track(myAddress[0], myAddress[1])
		text = 'the following busses near you are running ' + ' '.join(a.returnNearbyActiveRoutes())
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
	elif intent_name == 'aboutDev':
		return devInfo()
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
	session_attributes = {}
	card_title = "Rubik's Cube Scramble Generator"
	speech_output = "Welcome to the Rubiks Cube Scramble Generator Amazon Alexa Skill," \
					"I can generate Rubiks Cube scrambles that coincide with WCA regulations."
	reprompt_text = "Please ask me to generate a scramble.  You can also ask about the Developer of this application"
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
	"text": "Thanks for checking out Rubiks Scrambler!"
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