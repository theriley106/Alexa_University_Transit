import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import requests
import csv
import bs4

url = 'https://www.charlestonworks.com'

information = []

def saveToCSV(listItem):
	with open("{}.csv".format('schools'), "a") as fp:
	    wr = csv.writer(fp, dialect='excel')
	    tr = getTopResult(listItem)
	    wr.writerow([listItem, tr])

def getTopResult(companyName):
	try:
		url = 'https://www.google.com/search?source=hp&q={}+transloc'.format(companyName.replace(' ', '+'))
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
		res = requests.get(url, headers=headers)
		page = bs4.BeautifulSoup(res.text, 'lxml')
		print("done")
		return str(page.select("#rso a")[0]).partition('href="')[2].partition('"')[0]
	except Exception as exp:
		print exp
		return ""

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
res = requests.get('http://translocrider.com/our-agencies', headers=headers)
page = bs4.BeautifulSoup(res.text, 'lxml')
listOfSchools = page.select('#x-section-1 p')[0].getText().split('\n')

for e in listOfSchools:
	saveToCSV(e)
