import json
import requests
import os, sys

auth_key = os.environ['DENSITY_API_KEY']


def density_msg(result):
	print(result)

	try:
		location = result['parameters']['density_entities']
	except:
		location = 'Avery'

	return parse_json(location) 

def parse_json(location):
	url = 'http://density.adicu.com/latest?auth_token='+auth_key
	payload = ''
	response = requests.request('GET', url, data = payload)
	json_response  = response.json();
	#return response
	
	building_parameter = 'building_name'
	floor_parameter = 'group_name'
	result_list = [];
	percent_parameter = 'percent_full'

	for place in json_response['data']:
		match = bool(place[building_parameter] in location) or bool(place[floor_parameter] in location) or bool(location in place[floor_parameter])
		if match:
			result_list.append(place[floor_parameter] + ' is ' + str(place[percent_parameter]) + '% full. ')
		
		
	return list_to_str(result_list)

def list_to_str(list_name):
	final_str = ''
	for string in list_name:
		final_str += string + '\n'

	return final_str






