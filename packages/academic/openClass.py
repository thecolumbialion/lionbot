from bs4 import BeautifulSoup as bs
import urllib.request as urllib2
import re
import string

"""THIS FILE IS CURRENTLY NOT IN USE"""

#scrape for all classrooms of a given semester
#return dictionary of days of week/
def getUrls():
	SEMESTER = "Spring"
	YEAR = "2017"

	parent = "http://www.columbia.edu/cu/bulletin/uwb/sel/subj-"
	sub = list(string.ascii_uppercase)
	urls = [parent + item + ".html" for item in sub]

	# then use these created links to crawl the link of each subject.
	html_suburls = []
	for url in urls:
	    html = urllib2.urlopen(url).read()
	    soup = bs(html, "lxml")

	    for a in soup.find_all('a', href=True):
    		if str(SEMESTER+YEAR) in a:
    			html_suburls.append(a['href'])

	suburls = ["http://www.columbia.edu" + item for item in html_suburls]
	#now we have the url to every class
	
	return suburls

def scrapeRooms(urls):
	#we create a dict to hold: Day & Time & Location
	dict = {"Day/Time": [], "Location": []}

	for url in urls:
	    html = urllib2.urlopen(url).read()
	    soup = bs(html, "lxml")

	    for time in soup.find_all('b',text='Day/Time:'):
	    	if time is not None:	
	    		timeInfo = time.next_sibling 
	    		if timeInfo is not None:
	    			timeInfoList = timeInfo[1:-1].split(" ")
	    			dict["Day/Time"].append(timeInfoList)
	    	

	    for location in soup.find_all('b',text='Location:'):
	    	if location is not None:
	    		locationInfo = location.next_sibling
	    		if locationInfo is not None:
	    			dict["Location"].append(locationInfo)

	x = len(dict["Day/Time"]) 
	
	for i in range(x):
		print(dict["Day/Time"][i], dict["Location"][i])
	print(x)
		

#def parseRooms(roomInfoDict, day, time):


urls = getUrls()
scrapeRooms(urls)




#parse dict output of scrapeRooms
#for specified time parameters 
#def findOpenRooms(day, time):

