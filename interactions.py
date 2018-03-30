import requests
import threading
import time
import json

GET_ALL_ROUTES  = "https://feeds.transloc.com/3/routes?agencies={0}"
GET_CURRENT_INFO = "https://feeds.transloc.com/3/vehicle_statuses?agencies={0}"
GET_STOP_INFO = "https://feeds.transloc.com/3/stops?&agencies={0}"


def grabAllInfo(agencyId):
	tempDict = {}
	def getRoutes(agencyId):
		url = GET_ALL_ROUTES.format(agencyId)
		tempDict["Routes"] = requests.get(url).json()

	def getStatus(agencyId):
		url = GET_CURRENT_INFO.format(agencyId)
		tempDict["currentInfo"] = requests.get(url).json()

	def getStopInfo(agencyId):
		url = GET_STOP_INFO.format(agencyId)
		tempDict["Stops"] = requests.get(url).json()
	threads = []
	threads.append(threading.Thread(target=getStopInfo, args=(agencyId,)))
	threads.append(threading.Thread(target=getStatus, args=(agencyId,)))
	threads.append(threading.Thread(target=getRoutes, args=(agencyId,)))
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	return tempDict
if __name__ == '__main__':
	start = time.time()
	a = grabAllInfo('128')
	end = time.time()
	print(end - start)
	with open('data.json', 'w') as outfile:
		json.dump(a, outfile)
