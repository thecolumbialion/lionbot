import sys
import datetime
import requests
import ast
import html
import json
from bs4 import BeautifulSoup
import itertools


def campus_events_msg(result):
    return current_events()


#takes in output from current_events function
def event_finder():
    return


#returns a dictionary mapping dates to events
def current_events():

    url = 'https://events.columbia.edu/feeder/main/eventsFeed.do?f=y&sort=dtstart.\
    utc:asc&fexpr=(categories.href!=%22/public/.bedework/categories/sys/Ongoing%22)%\
    20and%20(categories.href=%22/public/.bedework/categories/org/UniversityEvents%22)\
    %20and%20(entity_type=%22event%22%7Centity_type=%22todo%22)&skinName=list-json&count=10'\

    file = requests.get(url)
    file_json = file.json()


    eventdict = {}
    event_list = file_json['bwEventList']['events']
    events = [li['summary'] for li in event_list]
    start_times = [li['start'] for li in event_list]
    end_times = [li['end'] for li in event_list]

    event_msg = "Here are some 10 events going on today or in the near future, \n \n"

    for (event, start, end) in zip(events, start_times, end_times):
     event_msg += 'Name: ' + event + '\n'+ 'Start Date: ' + start['shortdate'] + " " + start['time'] + ' End Date: ' + end['shortdate'] + " " + end['time'] + '\n\n'


    return(event_msg)





if __name__ == '__main__':
    current_events()

"""
next time add onto this feature

accomodate for dates and times maybe

allow them to ask for a specific event
"""
