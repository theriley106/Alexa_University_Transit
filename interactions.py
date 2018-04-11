import requests
import threading
import time
import json

GET_ALL_ROUTES  = "https://feeds.transloc.com/3/routes?agencies={0}"
GET_CURRENT_INFO = "https://feeds.transloc.com/3/vehicle_statuses?agencies={0}"
GET_STOP_INFO = "https://feeds.transloc.com/3/stops?&agencies={0}"
GET_ANNOUNCEMENTS = "https://feeds.transloc.com/3/announcements?agencies={0}"
GET_ARRIVALS = "https://feeds.transloc.com/3/arrivals?agencies={0}"
GET_SEGMENTS = "https://feeds.transloc.com/3/segments?agencies={0}"


def downloadURL(url):
	for i in range(2):
		res = requests.get(url, timeout=3)
		if res != None:
			return res

def grabAllInfo(agencyId):
	tempDict = {}
	def getAnnouncements(agencyId):
		url = GET_ANNOUNCEMENTS.format(agencyId)
		tempDict["Announcements"] = downloadURL(url).json()

	def getRoutes(agencyId):
		url = GET_ALL_ROUTES.format(agencyId)
		tempDict["Routes"] = downloadURL(url).json()

	def getSegments(agencyId):
		url = GET_SEGMENTS.format(agencyId)
		tempDict["Segments"] = downloadURL(url).json()

	def getStatus(agencyId):
		url = GET_CURRENT_INFO.format(agencyId)
		tempDict["currentInfo"] = downloadURL(url).json()

	def getStopInfo(agencyId):
		url = GET_STOP_INFO.format(agencyId)
		tempDict["Stops"] = downloadURL(url).json()

	def getArrivals(agencyId):
		url = GET_ARRIVALS.format(agencyId)
		tempDict["Arrivals"] = downloadURL(url).json()

	threads = []
	threads.append(threading.Thread(target=getStopInfo, args=(agencyId,)))
	threads.append(threading.Thread(target=getStatus, args=(agencyId,)))
	threads.append(threading.Thread(target=getRoutes, args=(agencyId,)))
	threads.append(threading.Thread(target=getAnnouncements, args=(agencyId,)))
	threads.append(threading.Thread(target=getArrivals, args=(agencyId,)))
	threads.append(threading.Thread(target=getSegments, args=(agencyId,)))
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	return tempDict

if __name__ == '__main__':
	start = time.time()
	a = grabAllInfo('639')
	end = time.time()
	print(end - start)
	with open('example.json', 'w') as outfile:
		json.dump(a, outfile)
