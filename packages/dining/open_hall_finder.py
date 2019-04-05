"""Finds all the dining halls that are currently open.
"""
import sys
import datetime
import requests
import ast
import html
import json
from bs4 import BeautifulSoup


def find_open():
    """ Returns a list of the dining halls on Columbia's dining website of all the currently open halls
    """
    file = requests.get('http://dining.columbia.edu/')
    soup = BeautifulSoup(file.content, "html.parser")
    halls = {}
    open_hall = soup.find_all("div", class_="content")
    halls = open_hall[6].find_all("li")
    hall_name_text = []
    for hall in halls:
        hallname = hall.get_text()  # .encode('utf-8')
        # print(hallname)
        hall_name_text.append(hallname)
        # print(hall_name_text)

        # adding barnard halls

    now = datetime.datetime.now()
    day = int(now.strftime("%w"))
    hour = int(now.hour)
    # diana

    cond1 = 0 < day < 6 and 9 < hour < 15
    cond2 = 0 < day < 5 and 17 < hour < 20
    cond3 = day < 5 and 20 < hour < 23
    if cond1 or cond2 or cond3:
        hall_name_text.append("Diana")
    # hewitt
    cond4 = day < 6 and 8 < hour < 17
    cond5 = day % 6 == 0 and 10 < hour < 15
    cond6 = day < 6 and 17 < hour < 20
    cond7 = day == 6 and 17 < hour < 19
    if cond4 or cond5 or cond6 or cond7:
        hall_name_text.append("Hewitt")
    # print(hall_name_text)
    return hall_name_text


def printhalls(halls):
    """ Prints the open dining halls to terminal. Gets rid of <li> tags
    """
    for hall in halls:
        hallname = hall.get_text()  # .encode('utf-8')
        print("\n\nDINING HALL: " + hallname)


def isOpen(args):

    #what the website returns on the 'network' section for each dining hall
    time_nodes = {
        "JJ's Place" : 66,
        "John Jay Dining Hall" : 67,
        "Ferris Booth" : 64,
        "Uris Deli" : 69,
        "Blue Java" : 58,
        "Cafe East" : 62
    }

    weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    #the specific entity
    dining_hall = args[0]

    if dining_hall in time_nodes.keys():

        #columbia dining url
        url = "https://dining.columbia.edu/ajax/location-node/load/" + str(time_nodes[dining_hall])

        #parsing through weird html format, columbia website made it a pain in the ass
        r = requests.get(url).text
        r = ast.literal_eval(r)
        html.unescape(r)
        r = r['location']

        #gets the hours on the specific dining hall
        soup = BeautifulSoup(r, 'html.parser')
        time_info = soup.find('div', attrs = {'class':'views-field-field-location-hoursdisplay-value'}).text.split('\n')
        while '' in time_info:
            time_info.remove('')


        #creating a dict for times (values) by weekdays (keys)
        timesbydays = {}

        for item in time_info:

            #the dash indicates that this is for a set of days
            if '-' in item:
                start = item[:item.find('-')].strip()
                end = item[item.find('-')+1:item.find(':')].strip()

                i = weekdays.index(start)

                #continously adds to a dictionary the times the dining hall is open to each day of the weel
                while weekdays[i] != end:
                    if i == len(weekdays) - 1:
                        i = 0
                    timesbydays[weekdays[i]] = item[item.find(':')+1:]
                    i = i + 1

                timesbydays[weekdays[i]] = item[item.find(':')+1:]

            #if it's a singular day span
            else:

                weekday = item[:item.find(':')].strip()
                timesbydays[weekday] = item[item.find(':')+1:]


        #only displays hours for that specific day and dining hall

        current_weekday = datetime.datetime.today().strftime('%A')

        #only displays if the dining hall is open on the day the user asks
        if current_weekday in timesbydays:
            current_hours = timesbydays[current_weekday]
            response = dining_hall + " is open today from " + current_hours
            return response


    #displays info on all the dining halls, if the user wants general dining hall info
    #or if the dining hall requested is not open
    
    if len(args) < 2:
        halls = find_open()
        if halls is None:
            response = "Could you try that again? I don't know what dining hall to check."
            return response
        elif len(halls) >= 1:
            response = "Here's what's currently open:\n"
            for value in halls:
                response += value + "\n"
            response = response[0:len(response) - 1]
            return response

        else:
            response = "Looks like no Columbia/Barnard Dining locations are open right now."
            return response

    else:
        dining_hall = args[1]
        if "boba" in dining_hall:
            dining_hall = "Cafe East"
        halls = find_open()
        if halls is None:
            response = "Looks like nothing is open right now."
            return response
        for value in halls:
            if dining_hall.lower() in value.lower():
                response = "Looks like %s is open!" % value
                return response
            else:
                continue
        response = "Unfortunately, %s is closed." % dining_hall
        return response


def dininghallisOpen_msg(result):
    halls = result.parameters['dining_halls']
    msg = isOpen(halls)
    return msg


if __name__ == '__main__':
    isOpen(sys.argv)
