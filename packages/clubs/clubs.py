import os 
import csv

def clubs_msg(result):
	try:
		club = result['parameters']['club']
	except:
		club = "The Lion"
	return find_clubs(club)

def make_club_dict():
	club_dict = {}
	club_file = open('./packages/clubs/clubs.csv')
	for club in club_file:
		club_info = club.split("\t")
		if len(club_info) < 2: 
			continue
		club_dict[club_info[0].strip()] = club_info[1].strip()
	return club_dict

def find_clubs(club):
	club = club.lower()
	clubs_dict = make_club_dict()
	results = []
	response = ""
	for club_name in clubs_dict.keys():
		club_name_lower = club_name.lower()
		if club in club_name_lower:
			club_result = club_name + ": " + clubs_dict[club_name] 
			results.append(club_result)

	if len(results) == 0:
		msg = "Looks like I couldn't find any information about that club."
		return msg

	else:
		for line in results:
			response += line + "\n"
	response = response.rstrip()
	return response

