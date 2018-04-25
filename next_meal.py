#############################
# Feature to return on what days a desired meal will occur next
#
#
#
#
############################

from bs4 import BeautifulSoup
import requests
import datetime

#get no. of days
def get_days():
    diction = {'1': "one", '2': "two", '3': "three", '4': "four", '5': "five", '6': "six", '7': "seven", '8': "eight", '9': "nine", '0': "zero", "10": "ten", "11": "eleven", "12": "twelve"}
    links = [];
    date = datetime.datetime.now()
    times = ["breakfast", "lunch", "dinner"]
    halls = ["fbc", "john-jay", "jjs"]
    for i in range(5):
        day = date.strftime("%A").lower()
        #date and month
        daymon = date.strftime("%m") + date.strftime("%d")
        weekNum = str( int(date.strftime("%U"))-1 );#columbia dining uses school weeks
        for time in times:
            for hall in halls:
                links.append("http://dining.columbia.edu/" + daymon + 
                        "week-" + diction[weekNum] + day + time + "-" + hall);
        
        date += datetime.timedelta(days=1)
    return links


def get_food(food):
    links = get_days()
    for link in links:
        print(link)
        r = requests.get(link);
        soup = BeautifulSoup(r.content, "html.parser")
        meals = soup.findAll("a", rel="lightframe")
        available = []
        for meal in meals:
    #        print(meal.text)
            if food in meal.text.lower():
                hall = soup.findAll("h2", limit=1)
                when = soup.findAll(class_="field field-type-datetime field-field-menu-date", limit=1)
                available.append(hall[0].text + "\n" + when[0].text)
        
        return available


def get_food_message(food):
    try:
        message = get_food(food)

    except:
        message = "Sorry this food is not available at the moment"

    return message

"""
def get_items(food):
    load = {'form-L84ZRv2WoggvSzUqsJoMugji-hZq9FAoL8HVDRf5gOM':food}
    r = requests.get('http://dining.columbia.edu/menus', 
                    params=load)
    print(r.text)
    #soup = BeautifulSoup(r.content, "html.parser")
    #result = soup.findAll("td")
    #for p in result:print(p.text)

get_items("eggs")
"""


