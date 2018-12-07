import re
import bs4
import requests
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
import datetime as dt


SCHOOLS = {"SEAS":14,
          "CC":11,
          "GS":15,
          "All":"All"}
          
TERMS = {"fall":6,
         "spring":7,
         "summer":8}
          
def get_school(name):
    if name and name in SCHOOLS:
        return SCHOOLS[name]
    return "All"

def get_yearnum(termnum,year):
    result = year - termnum - 1976
    if termnum == 8:
            result += 1
    return result


def get_current_termnum():
    """returns number corresponding to current term in url param"""
    month = dt.date.today().month;
    if month <= 5:
        return 7
    elif month <= 8:
        return 8
    else:
        return 6
    
def get_current_yearnum(termnum=None):
    """returns number corresponding to current Ac. year in url param"""
    if termnum == None:
        termnum = get_current_termnum()
    return get_yearnum(termnum,dt.date.today().year)


def get_params(school="11",term=None,year=None):
    params = {"acschool":school}
    if term:
        params["acterm"] = term
    else:
        params["acterm"] = get_current_termnum()
    if year:
        params["acfy"] = year
    else:
        params["acfy"] = get_current_yearnum()
    return params

def get_cal_url(params={}):
    """Returns url for cal with params"""
    urlparams = urlencode(params)
    return "http://registrar.columbia.edu/event/academic-calendar?" + urlparams
    
    
def get_cal_soup(url="http://registrar.columbia.edu/event/academic-calendar"):
    """returns BS of only the content of the calendar"""
    calPage = requests.get(url)
    pageSoup = bs4.BeautifulSoup(calPage.text, "html.parser")
    calSoup = pageSoup.select("#block-system-main > div > div > div.view-content")[0] #Exact selector: #block-system-main > div > div > div.view-content
    return calSoup
    
##block-system-main div.view-content
    
def search2array(text):
    txtlower = text.lower()
    txtarray = re.split(";\\s*",txtlower)
    return txtarray

def searchfor(searchterms, doc):
    for i in searchterms:
        if i in doc:
            return True
    return False

CDATE ="field-name-field-event-date1"
CEVENT = "field-name-event-title"
EVENTDES = "field-type-text-with-summary"
def get_events(search,url):
    soup = get_cal_soup(url)
    #search = "Holiday" #input("Event? ")
    eventnamesdes = soup.find_all((lambda x: 
                                x.get('class') and 
                                (CEVENT in x.get('class') or EVENTDES in x.get('class')) and 
                                searchfor(search2array(search), x.get_text().lower())))
    eventnames = []
    for x in eventnamesdes:
        if EVENTDES in x.get('class'):
            eventnames.append(x.find_previous_sibling(class_=CEVENT))
        else:
            eventnames.append(x)
    
    events = {x.get_text().strip() : x.find_previous_sibling(class_=CDATE).get_text() for x in eventnames}
    return events
    
def cal_message(event, school, term, year):
    if school == "":
        school = "CC"
    if term == "":
        termnum = get_current_termnum()
    else:
        termnum = TERMS[term.lower()]
    if year == "":
        yearnum = get_current_yearnum();
    else:
        year = int(year)
        yearnum = get_yearnum(termnum,year)
    params = get_params(school=SCHOOLS[school.upper()],year=yearnum,term=termnum)
    url = get_cal_url(params)
    events = get_events(event,url)
    message = "\n".join([k + " is on " + v + "." for k,v in events.items()])
    message += "\n\nI found this information at " + url + " (please double check my results for important dates.)"
    return message
    

def main():
    term = input("What term? ")
    year = input("What year? ")
    school = input("What school? ")
    event = input("Event? ").lower()
    print(cal_message(event, school, term, year))
    
                             
def calendar_msg(result):
    """Interface Function"""
    calschool = result['parameters']['school']
    calyear = result['parameters']["year"]
    calterm = result['parameters']['term']
    calevent = result['parameters']['cal_event']
    try:
        msg = cal_message(calevent, calschool, calterm, calyear)
    except:
        msg = "Looks like I couldn't find that. Try that again?"
    
    return msg

if __name__ == "__main__":
    main()
