from bs4 import BeautifulSoup
import requests
import datetime

#get no. of days
def get_days():
    diction = {'1': "one", '2': "two", '3': "three", '4': "four", '5': "five", '6': "six",
            '7': "seven", '8': "eight", '9': "nine", '0': "zero"}
    links = [];
    date = datetime.datetime.now()
    times = ["breakfast", "lunch", "dinner"]
    halls = ["fbc", "john-jay", "jjs"]
    for i in range(5):
        day = date.strftime("%A").lower()
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
        r = requests.get(link);
        soup = BeautifulSoup(r.content, "html.parser")
        meals = soup.findAll("a", rel="lightframe")
        
        for meal in meals:
    #        print(meal.text)
            if food in meal.text.lower():
                hall = soup.findAll("h2", limit=1)
                when = soup.findAll(class_="field field-type-datetime field-field-menu-date", limit=1)
                print(hall[0].text + "\n" + when[0].text)


get_food("egg")


"""
def get_items(food):
    load = {'food':food}
    r = requests.post('http://dining.columbia.edu/menus/mood-search', 
            data=load)

    #soup = BeautifulSoup(r.content, "html.parser")
    #result = soup.findAll("div", id="mood-wrapper")
    print(r.text)

get_items("eggs")
"""


