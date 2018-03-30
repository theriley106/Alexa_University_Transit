import requests
import threading

GET_ALL_ROUTES  = "https://feeds.transloc.com/3/stops?agencies={0}"
GET_CURRENT_INFO = "https://feeds.transloc.com/3/vehicle_statuses?agencies={0}"
GET_STOP_INFO = "https://feeds.transloc.com/3/stops?&agencies={0}"

def getRoutes(agencyId):


def grabAllInfo(agencyId):
	res = requests.get("")
