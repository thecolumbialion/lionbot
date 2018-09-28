import json
import requests


auth_key = 'vsHAK7tggAjSQo7f0F7jfzKeEHeUOlgOa1_3v_rqhQgkSIWxkbNOopdJnRvXrti0'


def density_msg(result):
	print(result)
	
	try:
		location = result['parameters'][density_entities]
	except:
		location = 'Butler'

	return parse_json(location) 

def parse_json(location):
	url = 'http://density.adicu.com/latest/'
	payload = ''
	response = requests.request('GET', url, data = payload)
	json_response  = response.json();
	building_parameter = 'building_name'
	floor_parameter = 'group_name'
	result_list = [];
	percent_parameter = 'percent_full'

	for place in json_response['data']:
		match = bool(place[building_parameter] in location) or bool(place[floor_parameter] in location) 
		if match:
			result_list.append(place[floor_parameter] + ' is ' + place[percent_parameter] + ' full. ')
		
		
	return list_to_str(result_list)

def list_to_str(list_name):
	final_str = ''
	for string in list_name:
		final_str += string + '\n'

	return final_str






