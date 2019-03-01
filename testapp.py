# request parsing libaries
import json
# system libraries
import os

# database related libraries
import urllib.parse
import uuid
import psycopg2

# flask libraries
from flask import Flask, request, make_response, jsonify

# NLP/context libraries
from api.ai import Agent

# Bot libraries
from fbmq import Template, fbmq

# wellness libaries
from packages.wellness.health import health_resources, health_concern_msg

# dining
from packages.dining.open_hall_finder import dininghallisOpen_msg
# from dining.menu_scraper import dining_hall_menu_msg
from packages.dining.dining import dining_events_msg
from packages.dining.dining import dining_hall_food_request_msg
from packages.dining.dining import dining_hall_menu_msg

# academic
from packages.academic.library_hours import libraries_msg
from packages.academic.academic_calendar import calendar_msg
from packages.academic.printers import printers_msg

# housing
from packages.housing.cutv_channels import tv_network_msg
from packages.housing.laundry import open_machines_msg

# offcampus
from packages.offcampus.broadway import broadway_rush_msg
from packages.offcampus.food_recommendations import offcampus_dining_request_msg
from packages.offcampus.mta import mta_subway_info_msg
from packages.offcampus.food_hours import offcampus_dining_hours_msg

# clubs
from packages.clubs.news import news_msg
from packages.clubs.clubs import clubs_msg

# etc
from packages.etc.memes import get_meme_msg
from packages.etc.wisdomsearch import wisdom_search
from packages.etc.weather import weather_msg

# internal libraries
from packages.internal.postbacks import intro_reply, health_reply
from packages.internal.postbacks import subscriptions_reply
from packages.internal.postbacks import current_features_msg

# density
from packages.density.density import density_msg

MAX_MESSAGE_LENGTH = 160 # Pretty sure that max message length is 160 for dialogflow
app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ['SECRET_KEY']
)

agent = Agent(
    'thecolumbialion',
    os.environ['CLIENT_ACCESS_TOKEN'],
    os.environ['DEVELOPER_ACCESS_TOKEN'],
)

page = fbmq.Page(os.environ['ACCESS_TOKEN'], api_ver="v2.11")
page.greeting(
    "Welcome to LionBot! Click below to learn more about what I can do.")
page.show_starting_button("GET_STARTED")

# Dictionary of all module interface functions.
Msg_Fn_Dict = {
    'clubs': clubs_msg,
    'printers': printers_msg,
    'mta_subway_info': mta_subway_info_msg,
    'campus_news_updates': news_msg,
    'tv_network': tv_network_msg,
    'libraries': libraries_msg,
    'dining_events': dining_events_msg,
    'dininghallisOpen': dininghallisOpen_msg,
    'offcampus_dining_request': offcampus_dining_request_msg,
    'offcampus_dining_hours': offcampus_dining_hours_msg,
    'broadway_rush': broadway_rush_msg,
    'calendar': calendar_msg,
    'dining_hall_menu': dining_hall_menu_msg,
    'dining_hall_food_request': dining_hall_food_request_msg,
    'weather': weather_msg,
    'current_features': current_features_msg,
    'health_concern': health_concern_msg,
    'web.search': wisdom_search,
    'meme': get_meme_msg,
    'laundry': open_machines_msg,
    'density': density_msg
    }

#################


def chunkify(msg):
    """ Break message into chunks that are below
        Dialogflow's max character limit.
        This uses a generator comprehension to be efficient.
    """
    return (msg[0+i:MAX_MESSAGE_LENGTH+i] for i in range(0, len(msg), MAX_MESSAGE_LENGTH))

def get_generic_or_msg(intent, result):
    """ The master method.  This method takes in the
    intent and the result dict structure
    and calls the proper interface method. """
    return Msg_Fn_Dict[intent](result)

def add_string_response(msg, response):
    """
    If the response from the package functions is a string,
    then we want to parse it to make sure that it doesn't 
    exceed the character limit, and then add that to the 
    response message.
    """
    for chunk in chunkify(msg):
        message = { "type": 0, "speech": chunk }
        response['messages'].append(message)

def add_template_list_response(tlist, response):
    """
    If the response from the package function is a Template.List,
    then we want to parse the container and then add its 
    information to the response message.
    """
    for element in tlist.payload['elements']:
        add_generic_element(element, response)

def add_generic_element(element, response):
    """
    A Template.GenericElement is the type that is contained in a 
    Template.List; we want to make sure that we get the info from this
    data structure properly so that we can emulate how Facebook 
    would send a response back to a user.
    """
    message = { "type": 1,
                "title": element.title,
                "subtitle": element.subtitle,
                "imageUrl": element.image_url,
                "itemUrl": element.item_url
            }
    response['messages'].append(message)
    if element.buttons:
        add_buttons(element.buttons, response)

def add_buttons(buttons, response):
    """
    In the typical Facebook response message, it sends back pressable 
    buttons. We don't really care that much about that for the 
    testing(for now). We just want to be sure that we're sending pictures/text 
    properly.
    """

    #Remember that lists in python are passed by reference
    buttons_data = response['data']['facebook']['buttons'] 
    for button in buttons:
        if button.type == 'web_url': 
            # In case there is just a url
            button_object = { "type": button.type,
                              "title": button.title,
                              "url": button.url
                            }
        else: 
            # In case we have a phoneNumber or PostBack
            button_object = { "type": button.type,
                              "title": button.title,
                              "payload": button.payload
                            }
        buttons_data.append(button_object)

def init_dialogflow_response():
    """ Typical dialogflow response template for v1 """
    resp = { "displayText": "",
             "messages" : [],
             "data": { 
                 "facebook": { 
                        "buttons": []
                 } 
             }
           }
    return resp
    
###############################################


urllib.parse.uses_netloc.append("postgres")
url = urllib.parse.urlparse(os.environ['DATABASE_URL'])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
cur = conn.cursor()


@app.route('/webhook', methods=['GET'])
def validate():
    if request.args.get(
        'hub.mode',
        '') == 'subscribe' and request.args.get(
        'hub.verify_token',
            '') == os.environ['VERIFY_TOKEN']:
        print("Validating webhook")
        return request.args.get('hub.challenge', '')
    return "Failed validation. Make sure the validation tokens match."

@app.route('/webhook', methods=['POST'])
def message_handler():
    req = request.get_json(force=True)      # Get the post request, get it in json format
    res = ''                                # Response to the post query
    intentName = ''                         # intent Name
    defaultResponse = ''                    # The default response that we will send back
    result = None                           # Dialogflow's default response to the request
    metadata = None                         # POST metadata 
    response = init_dialogflow_response()   # POST request response (what we will send back to query)


    # Get the intentName from the post request
    # We don't Necessarily need to use get(), but an Attribute Error
    # is more intuitive than a KeyError since we're working 
    # with dict() objects derived from JSON
    try:
        result = req.get('result')
        metadata = result.get('metadata')
        intentName = metadata.get('intentName') 
        defaultResponse = result.get('fulfillment').get('speech')
    except AttributeError:
        return 'json error'

    #Check the intent name
    if intentName in Msg_Fn_Dict:
        webhook_resp = get_generic_or_msg(intentName, result)
        print(type(webhook_resp))
        if isinstance(webhook_resp, Template.List):
            print('We got a template list response!')
            add_template_list_response(webhook_resp, response)
        elif isinstance(webhook_resp, str):
            print('We got a string list response!')
            add_string_response(webhook_resp, response)
        else:
            print("What the hell HAPPENED!")
            print("Type of the returned response %s" % (type(webhook_resp)))
    else:
        message = { "type": 0, 
                    "speech": "Interesting... I don't really know how to respond to that."
                  }
        response['messages'].append(message)

    #Return the value of the response 
    return make_response(jsonify(response))

if __name__ == "__main__":
    app.run()
