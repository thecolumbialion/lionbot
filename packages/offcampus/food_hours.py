import os, sys
import datetime
from fbmq import Template, QuickReply, ButtonPostBack
import requests
import json

def offcampus_dining_hours_msg(result):
	'''Interface Function'''	
	try: 
		term = result['parameters']['off_campus_restaurant']

	except: 
		return 'Sorry, couldn\'t find that restaurant. Try another?'
	hours = get_hours(term)
	hours_result = term + '\'s ' + hours 
	response = hours_result
	return response

def get_hours(term):
	#set latittude and longitude to CU 
	search_results = query_yelp_search(term, 40.806209, -73.961733, 1)
	biz_id = parse_search(search_results)
	biz_results = query_yelp_lookup(biz_id)
	return get_today_hours(biz_results)

#search for resturant 
def query_yelp_search(term, latitude, longitude, query_limit):
	headers = {'Authorization': 'Bearer ' + 'w5JFtwCUKq05GlSpm8cKo51dBYDQ6r9tyzo-qRsKt4wDyB5_ro6gW5gnG9hS6bvnNHNxOQLHfw7o_9S1e86nkvgcU7DQI_sM6GVt9rqcq_rRYKtagQrexuH0zsU0WXYx'}
	params = { 
		'term': term,
		'latitude': latitude,
		'longitude': longitude, 
		'locale': 'en_US',
		'limit': query_limit,
		'open_now': 'True' 
	}
	query = requests.get('https://api.yelp.com/v3/businesses/search', headers=headers, params=params)
	return query.json()

#get id from search results 
def parse_search(results):
	if 'businesses' not in results: 
		print('error - resturant not found')
		return 
	biz_id = results['businesses'][0]['id']
	return biz_id

#lookup resturant using id 
def query_yelp_lookup(biz_id):
	headers = {'Authorization': 'Bearer ' + 'w5JFtwCUKq05GlSpm8cKo51dBYDQ6r9tyzo-qRsKt4wDyB5_ro6gW5gnG9hS6bvnNHNxOQLHfw7o_9S1e86nkvgcU7DQI_sM6GVt9rqcq_rRYKtagQrexuH0zsU0WXYx'}
	url = 'https://api.yelp.com/v3/businesses/' + biz_id
	query = requests.get(url, headers=headers)
	return query.json()

#get hours for today for lookup results 
def get_today_hours(results):
	day = datetime.datetime.today().weekday()

	open_time = results['hours'][0]['open'][day]['start']
	close_time = results['hours'][0]['open'][day]['end']
	
	parsed_open = parse_time(open_time)
	parsed_close = parse_time(close_time)

	hours_msg = "hours for today are " + parsed_open + " to " + parsed_close
	return hours_msg

#get hours for other days, day is int corresponding to weekday() 
def get_other_hours(results, day):
	open_time = results['hours'][0]['open'][day]['start']
	close_time = results['hours'][0]['open'][day]['end']
	
	parsed_open = parse_time(open_time)
	parsed_close = parse_time(close_time)

	hours_msg = "hours are " + parsed_open + " to " + parsed_close
	return hours_msg

def parse_time(time_string):
	#figure out if am or pm and convert from 24 hour time 
	time_modifier = 'p.m.'
	hour = time_string[0:2]
	if int(hour) < 12:
		time_modifier = 'a.m.'
	elif int(hour) > 12:
		hour = int(hour) - 12 
	
	#fix midnight  
	if int(hour) == 0: 
		hour = 12
	parsed_time = str(hour) + ":" + time_string[2:4] + " " + time_modifier
	return parsed_time
