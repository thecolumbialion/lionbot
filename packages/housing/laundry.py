from bs4 import BeautifulSoup
import urllib
import sys
import datetime
import time
import os
import re
import requests


def open_machines_msg(args):
    try:
        response = open_machines(args)
        return response
    except:
        response = "Looks like I couldn't find the laundry information requested."
        return response



def get_laundry_dict():
    file = requests.get('http://classic.laundryview.com/columbia')
    soup = BeautifulSoup(file.content, "html.parser")
    laundry = []
    hall = soup.find_all("div", id="campus1")
    rooms =  hall[0].find_all("a", class_="a-room")
    avail = hall[0].find_all("span", class_="user-avail")
    laundry_dict = {}
    for count, room in enumerate(rooms):
        laundry_dict[re.split("\\s\\s+", str(room))[1]] = {"washers": re.findall(r'\d+', avail[count].get_text())[0], "dryers": re.findall(r'\d+', avail[count].get_text())[1]} 
    return laundry_dict

def open_machines(args):    
    laundry_dict = get_laundry_dict()
    #print(args["parameters"]["machine_type"])
    if laundry_dict is None:
        response = "Sorry, either Laundry View is down or Columbia no longer has laundry machines."
    else:
        if args["parameters"]["hall_residence"] == "WATT":
            hall = "WATT "
            watt_floors = ["1ST FLR.", "2ND FLR.", "3RD FLR.", "4TH FLR.", "5TH FLR.", "6TH FLR."]
            watt_floor = args["parameters"]["laundry_watt_floor"]
            machine_type = args["parameters"]["machine_type"]
            if watt_floor == "":
                response = "There are "
                for count, floor in enumerate(watt_floors):
                    if machine_type == "":
                        if count < len(watt_floors) - 1:
                            response += laundry_dict["WATT " + floor]["washers"] + " washers and " +  laundry_dict["WATT " + floor]["dryers"] + " dryers available on floor " + str(count + 1) + ", \n"
                        else:
                            response += "and " + laundry_dict["WATT " + floor]["washers"] + " washers and " +  laundry_dict["WATT " + floor]["dryers"] + " dryers available on floor " + str(count + 1) + "."
                    else:
                        if count < len(watt_floors) - 1:
                            response += laundry_dict["WATT " + floor][machine_type] + " " + machine_type + " available on floor " + str(count + 1) + ", \n"
                        else:
                            response += "and " + laundry_dict["WATT " + floor][machine_type] + " " + machine_type + " available on floor " + str(count + 1) + "."
            elif watt_floor in watt_floors:
                hall += watt_floor
                if machine_type == "":
                    response = "There are " + laundry_dict[hall]["washers"] + " washers and " + laundry_dict[hall]["dryers"] + "dryers available on floor " + str(watt_floors.index(watt_floor)) + "."
                else:
                    response = "There are " + laundry_dict[hall][machine_type] + " " + machine_type + " available on floor " +  str(watt_floors.index(watt_floor)) + "."
        elif args["parameters"]["hall_residence"] not in laundry_dict.keys():
            response = "Sorry, I'm not sure which residence hall to check."
        elif args["parameters"]["machine_type"] == "washers":
            response = "There are " + laundry_dict[args["parameters"]["hall_residence"]]["washers"] + " washers available in " + args["parameters"]["hall_residence"] 
        elif args["parameters"]["machine_type"] == "dryers":
            response = "There are " + laundry_dict[args["parameters"]["hall_residence"]]["dryers"] + " dryers available in " + args["parameters"]["hall_residence"]
        else:
            response = "There are " + laundry_dict[args["parameters"]["hall_residence"]]["washers"] + " washers and " + laundry_dict[args["parameters"]["hall_residence"]]["dryers"] + " dryers available in " + args["parameters"]["hall_residence"]
    return response
    

