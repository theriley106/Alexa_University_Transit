import requests
import threading

GET_ALL_ROUTES  = "https://feeds.transloc.com/3/routes?agencies={0}"
GET_CURRENT_INFO = "https://feeds.transloc.com/3/vehicle_statuses?agencies={0}"
GET_STOP_INFO = "https://feeds.transloc.com/3/stops?&agencies={0}"

def getRoutes(agencyId):
	url = GET_ALL_ROUTES.format(agencyId)
	tempDict["Routes"] = requests.get(url).json()

def getStatus(agencyId):
	url = GET_CURRENT_INFO.format(agencyId)
	tempDict["currentInfo"] = requests.get(url).json()

def getStopInfo(agencyId):
	url = GET_STOP_INFO.format(agencyId)
	tempDict["Stops"] = requests.get(url).json()

def grabAllInfo(agencyId):
	tempDict = {}
	threads = []
	threads.append(threading.Thread(target=getStopInfo, args=(agencyId,)))
	threads.append(threading.Thread(target=getStatus, args=(agencyId,)))
	threads.append(threading.Thread(target=getRoutes, args=(agencyId,)))
	res = requests.get("")
