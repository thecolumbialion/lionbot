import urllib.request as urllib2
import string
from bs4 import BeautifulSoup as bs

"""THIS FILE IS CURRENTLY NOT IN USE"""


def get_urls():
    """ Scrapes for all classrooms of a given semester

    Return:
        suburls (dict): dictionary of days of week/
    """
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
    # now we have the url to every class
    return suburls


def scrape_rooms(urls):
    """
    Creates a dict to hold: Day & Time & Location
    """
    dict = {"Day/Time": [], "Location": []}

    for url in urls:
        html = urllib2.urlopen(url).read()
        soup = bs(html, "lxml")

        for time in soup.find_all('b', text='Day/Time:'):
            if time is not None:
                time_info = time.next_sibling
                if time_info is not None:
                    time_info_list = time_info[1:-1].split(" ")
                    dict["Day/Time"].append(time_info_list)

        for location in soup.find_all('b', text='Location:'):
            if location is not None:
                locationInfo = location.next_sibling
                if locationInfo is not None:
                    dict["Location"].append(locationInfo)

    x = len(dict["Day/Time"])
    for i in range(x):
        print(dict["Day/Time"][i], dict["Location"][i])
    print(x)

# def parseRooms(roomInfoDict, day, time):


urls = get_urls()
scrape_rooms(urls)

# parse dict output of scrapeRooms
# for specified time parameters
# def findOpenRooms(day, time):
