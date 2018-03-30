import requests
import threading

GET_ALL_ROUTES  = "https://feeds.transloc.com/3/stops?agencies={0}"
GET_CURRENT_INFO = "https://feeds.transloc.com/3/vehicle_statuses?agencies={0}"
GET_STOP_INFO = "https://feeds.transloc.com/3/stops?&agencies={0}"

def getRoutes(agencyId):
	url = GET_ALL_ROUTES.format(agencyId)
	tempDict["Routes"] = requests.get(url).json()

def getStatus(agencyId):
	url = GET_CURRENT_INFO.format(agencyId)
	tempDict["currentInfo"] = requests.get(url).json()

def grabAllInfo(agencyId):
	res = requests.get("")
