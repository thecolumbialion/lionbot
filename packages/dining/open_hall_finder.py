"""Finds all the dining halls that are currently open.
"""

from bs4 import BeautifulSoup
import urllib
import sys
import datetime
import time
import os
import requests

""" Returns a list of the dining halls on Columbia's dining website of all the currently open halls
"""

def find_open():
    file = requests.get('http://dining.columbia.edu/')
    soup = BeautifulSoup(file.content, "html.parser")
    halls = {}
    open_hall = soup.find_all("div", class_="content")
    halls = open_hall[6].find_all("li")
    hall_name_text = []
    for hall in halls:
        hallname = hall.get_text()#.encode('utf-8')
        #print(hallname)
        hall_name_text.append(hallname)
        # print(hall_name_text)

        # adding barnard halls

    now = datetime.datetime.now()
    day = int(now.strftime("%w"))
    hour = int(now.hour)
    # diana

    cond1 = 0 < day < 6 and 9  < hour < 15
    cond2 = 0 < day < 5 and 17 < hour < 20
    cond3 = day < 5 and 20 < hour < 23
    if cond1 or cond2 or cond3:
        hall_name_text.append("Diana")
    # hewitt
    cond4 = day < 6 and 8 < hour < 17
    cond5 = day%6 == 0 and 10 < hour < 15
    cond6 = day < 6 and 17 < hour < 20
    cond7 = day == 6 and 17 < hour < 19
    if cond4 or cond5 or cond6 or cond7:
        hall_name_text.append("Hewitt")
    #print(hall_name_text)
    return hall_name_text

""" Prints the open dining halls to terminal. Gets rid of <li> tags
"""
def printhalls(halls):
    for hall in halls:
        hallname = hall.get_text()#.encode('utf-8')
        print("\n\nDINING HALL: " + hallname)

def isOpen(args):
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
    halls = result['parameters']['dining_halls']
    msg = isOpen(halls)
    return msg

if __name__ == '__main__':
    isOpen(sys.argv)
