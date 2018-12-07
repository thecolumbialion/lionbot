#flask libraries
from flask import Flask, request, redirect, render_template, request, abort, Response, flash, send_file
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from flask import session as sess
from werkzeug.security import generate_password_hash, check_password_hash

#NLP/context libraries
from api.ai import Agent

#Bot libraries
from fbmq import Attachment, Template, QuickReply, NotificationType, fbmq

#system libraries
import os

#database related libraries
import psycopg2
import urllib.parse
import uuid
import ast
import requests

#wellness libaries
from packages.wellness.health import health_resources, health_concern_msg

#dining
from packages.dining.open_hall_finder import dininghallisOpen_msg
#from dining.menu_scraper import dining_hall_menu_msg
from packages.dining.dining import dining_events_msg, dining_hall_food_request_msg, dining_hall_menu_msg

#academic
from packages.academic.library_hours import libraries_msg
from packages.academic.academic_calendar import calendar_msg
from packages.academic.printers import printers_msg

#housing
from packages.housing.cutv_channels import tv_network_msg
from packages.housing.laundry import open_machines_msg

#offcampus
from packages.offcampus.broadway import broadway_rush_msg
from packages.offcampus.food_recommendations import offcampus_dining_request_msg, get_yelp_info
from packages.offcampus.mta import mta_subway_info_msg
from packages.offcampus.food_hours import offcampus_dining_hours_msg

#clubs
from packages.clubs.news import news_msg
from packages.clubs.clubs import clubs_msg

#etc
from packages.etc.memes import get_meme_msg
from packages.etc.wisdomsearch import wisdom_search
from packages.etc.weather import weather_msg

#internal libraries
from packages.internal.postbacks import intro_reply, health_reply, bot_menu, subscriptions_reply, current_features_msg


MAX_MESSAGE_LENGTH = 640
app = Flask(__name__)
app.config.update(
    SECRET_KEY= os.environ['SECRET_KEY']
)

agent = Agent(
     'thecolumbialion',
     os.environ['CLIENT_ACCESS_TOKEN'],
     os.environ['DEVELOPER_ACCESS_TOKEN'],
)

page = fbmq.Page(os.environ['ACCESS_TOKEN'],api_ver="v2.11")
page.greeting("Welcome to LionBot! Click below to learn more about what I can do.")
page.show_starting_button("GET_STARTED")
#THE DICT
""" Dictionary of all module interface functions."""
Msg_Fn_Dict = {
        'clubs' : clubs_msg,
        'printers':printers_msg,
        'mta_subway_info':mta_subway_info_msg,
        'campus_news_updates': news_msg,
        'tv_network': tv_network_msg,
        'libraries' : libraries_msg,
        'dining_events' : dining_events_msg,
        'dininghallisOpen' : dininghallisOpen_msg,
        'offcampus_dining_request' : offcampus_dining_request_msg,
        'offcampus_dining_hours' : offcampus_dining_hours_msg,
        'broadway_rush' : broadway_rush_msg,
        'calendar' : calendar_msg,
        'dining_hall_menu' : dining_hall_menu_msg,
        'dining_hall_food_request' : dining_hall_food_request_msg,
        'weather': weather_msg,
        'current_features': current_features_msg,
        'health_concern': health_concern_msg,
        'web.search': wisdom_search,
        'meme' : get_meme_msg,
        'laundry': open_machines_msg}

#################

def chunkify(msg):
    """ Break message into chunks that are below Facebook's max character limit"""
    try:
        maxline = MAX_MESSAGE_LENGTH
        lines = msg.split("\n")
        chunk = ""
        chunks = []
        for line in lines:
            if len(chunk) + len(line) <= maxline:
                chunk += line + "\n"
            else:
                chunks.append(chunk)
                chunk = line
        chunks.append(chunk)
        return chunks
    except:
        return ""


def get_generic_or_msg(intent,result):
    """ The master method.  This method takes in the intent and the result dict structure
    and calls the proper interface method."""
    #print("in get_generic_or_msg")
    return Msg_Fn_Dict[intent](result)
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

def submitTip(event):

    print("Entered submitTip")

    catDict = {'1':'classes','2':'questions', '3':'student'}

    recipient_id = event.sender_id
    message = event.message.get("text")
    #message = "uni: ddd123, question: Is this a test question?, tip: Test questions are good, categories: [2,3]"
    

    #get request ready
    """
    try:
        base_url = 'https://api.api.ai/v1'
        request_session = requests.Session()
        self.request_session.headers.update({
                 'Authorization': 'Bearer %s' % os.environ['DEVELOPER_ACCESS_TOKEN'],
                 'ocp-apim-subscription-key': self.sub_key,
        })
    except Exception as e:
        print(e)
        """

    uni = ""
    question = ""
    tip = ""
    categories = []
    try:
        message = message[message.index('tip submit data content:')+len('tip submit data content:'):]
        tokens = message.strip().split(',')
        uni = tokens[0].strip()
        question = tokens[1].strip()
        tip = tokens[2].strip()
        cat = 3
        while cat < len(tokens):
            categories.append(catDict[tokens[cat].strip()])
            cat += 1
     
        print('tip parsing worked!')
    except Exception as e:
        print('Student submitted wrongly formatted tip', str(e))
        page.send(recipient_id, 'Wrong format! try again')

    print("tip: ",  tip)
    print("question: ", question)
    print("uni: ", uni)
    print("categories: ", categories)
    page.send(recipient_id, 'Parsing worked! Checking your tip ...')

    # todo tip_number  = get fromDB
    try:
        q = 'SELECT MAX(tip_no) FROM tip_submission;'
        cur.execute(q)
        x = cur.fetchone()
        tip_number = x[0] + 1
        print("tip number: %d" % tip_number)
        response = agent.query(question)
        result = {'action': ''}
        print("asked agent about question")
    except Exception as e:
        print("this is the exception - ", e)
    try:
        result = response['result']
        intent = result['metadata'].get('intentName', None)

        print("checking intent of question. Intent is: " + intent)
        if intent == 'tip_filter':
            print("Went to if")
            page.send(recipient_id, "oops...your tip got rejected!")
            return

        if intent == 'Default Fallback Intent':
            print("Went to 2nd if")
            #POST add new intent adding tip as a default response
            try:
                #print(agent.intents.all())
                response = [{"resetContexts": False, "affectedContexts": [], "parameters": [], "messages": [{"type": 0, "lang": "en", "speech": tip}], "defaultResponsePlatforms": {}, "speech": []}]
                print(agent.intents.create(name = 'TIP#' + str(tip_number),contexts = [], templates= [question], responses = response))
                """
                body = {
                        "fallbackIntent": False,
                        "name": 'TIP#' + str(tip_number),
                        "priority": 500000,
                        "responses": [tip],
                        "templates": [question]
                        }

                print(request_session.post(base_url + "/intents?v=20150910", body).json())
                """

            except Exception as e:
                print("crashed creating intent", e)
            print("tip submitted")
            page.send(recipient_id, "Tip submitted")
            return

        else:
            print("Went to else")
            defaultResponse = result['fulfillment']['speech']
            tipID = result['metadata']['intentId']
            if 'TIP' in intent:
                # get question for follow up questions
                matchingIntent = request_session.get(base_url + "/intents?%sv=20150910"%tipID)



                # open up another webview that asks if they want to
                # add the tip to existing intent or create a new intent with their
                # question.

                # take response and respond accordingly

                # if they want to update
                # POST adding a default answer to intent
                # page.send("Tip submitted")

                body = {
                        "fallbackIntent": false,
                        "name": intent,
                        "priority": 500000,
                        "responses": [defaultResponse + '\n' + tip],
                        "templates": matchingIntent['templates']
                        }

                request_session.post(base_url + "/intents?v=20150910", body).json()
                page.send("Tip added to existing question")
                print("Adding to existing quesion worked!")

                #if user wants new question
                #page.send("Tip added to new question")
            else:
                print("Tip matched with another intent")
                agent.intents.create('TIP#' + tip_number,None,[question],tip)
                page.send("Sorry, ADI already handles that question")

        # todo enter into database the tip number, question, tip, categories
        q = "INSERT INTO tip_submission VALUES (%s, '%s', '%s',ARRAY[%s], '%s');" % (tip_number, tip, question,categories, uni)
        cur.execute(q)
        conn.commit()
    except:
        page.send("uh-oh something went wrong!")

@app.route('/webhook', methods=['GET'])
def validate():
    if request.args.get('hub.mode', '') == 'subscribe' and \
                    request.args.get('hub.verify_token', '') == os.environ['VERIFY_TOKEN']:
        print("Validating webhook")
        return request.args.get('hub.challenge', '')
    else:
        return "Failed validation. Make sure the validation tokens match."


def show_persistent_menu():
    page.show_persistent_menu([Template.ButtonPostBack('Subscriptions', 'MENU_PAYLOAD/subscriptions'),
                               Template.ButtonPostBack('Current Features', 'MENU_PAYLOAD/GET_STARTED'),
                               Template.ButtonPostBack('Health and Wellness', 'MENU_PAYLOAD/health')])
    return "Done with persistent menu section"

@page.callback(['MENU_PAYLOAD/(.+)'])
def click_persistent_menu(payload, event):
    click_menu = payload.split('/')[1]
    recipient_id = event.sender_id
    if click_menu == 'GET_STARTED':
        page.send(recipient_id, intro_reply)
        return "done with get started"
    elif click_menu == 'health':
        print(page.send(recipient_id, "What are you currently concerned about?", quick_replies=health_reply))
        return "done with health"
    elif click_menu == 'subscriptions':
        print(page.send(recipient_id, """Welcome to Subscriptions, a new feature that allows you to get direct updates from campus clubs. To check which topics you're subscribed to, just ask 'What topics am I currently subscribed to?'"""))
        print(page.send(recipient_id, "What topics do you want to subscribe to?", quick_replies=subscriptions_reply))
        return "done with subscriptions intro"
    else:
        print("CLICK MENU WAS " + click_menu + " and it failed to find the right payload")
        return "done"

    return "done with persistent menu click"

#TO-DO: add db query to insert userid to topic's column.
@page.callback(['Subscriptions/(.+)'])
def handle_subscriptons(payload, event):
    click_menu = payload.split('/')[1]
    recipient_id = event.sender_id
    print(page.send(recipient_id, "You are now subscribed to " + click_menu))
    page.typing_off(recipient_id)

    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cursor()
    try:
        subscription_query = "UPDATE subscription SET messenger_id_list = array_append(messenger_id_list, '%s') WHERE category = '%s'" % (recipient_id, click_menu)
        print(subscription_query)
        cur.execute(subscription_query)
        conn.commit()
    except:
        print("ERROR: Updating database (subscription) failed.")

    return "Done with handling subscription request"

@app.route('/webhook', methods=['POST'])
def webhook():
    page.handle_webhook(request.get_data(as_text=True))
    return "finished"

@page.handle_postback
def received_postback(event):
    show_persistent_menu()
    recipient_id = event.sender_id
    time_of_postback = event.timestamp
    payload = event.postback.payload
    try:
        payload = payload.split('/')[1]
    except:
        payload = payload
    if payload == 'GET_STARTED':
        try:
            user_profile = page.get_user_profile(recipient_id)
            first_name = str(user_profile["first_name"])
        except:
            first_name = ""
        print(page.send(recipient_id, "Hi, %s. Welcome to LionBot! Here's some of the things I can do." % (first_name)))
        print(page.send(recipient_id, intro_reply))

    elif payload == 'health':
        return "health done"
    elif payload == 'subscriptions':

        return "subscriptions done"
    else:
        return "ERROR: Menu not found"
    return "postback done"

@page.handle_message
def message_handler(event):
    recipient_id = event.sender_id
    message = event.message
    user_profile = page.get_user_profile(event.sender_id)
    response = agent.query(message.get("text"))
    page.typing_on(recipient_id)
    result = {'action': ''}
    defaultResponse = ""
    try:
        first_name = str(user_profile["first_name"])
        last_name = str(user_profile["last_name"])
        unique_id = uuid.uuid4().hex
        user_id = str(recipient_id)
        result = response['result']
        print("this is the result")
        print("")
        print(result)
        intent = result['metadata'].get('intentName', None)

        if intent == 'tip submit':
            print("caught the intent tip submit")
            submitTip(event)
            return "tip submission will be handled elsewhere"
        else:
            print("Did not match")
        defaultResponse = result['fulfillment']['speech']
    except:
        first_name, last_name, intent = ("", "", "")

    try:
        q = "INSERT INTO All_user_messages VALUES (%s,%s,%s,%s,%s,%s)" % (unique_id, user_id, last_name, first_name, intent, message)
        cur.execute(q)
        conn.commit()
    except:
        print("ERROR: Inserting into database failed.")

    message_text = message.get("text")
    message_attachments = message.get("attachments")
    quick_reply = message.get("quick_reply")
    if quick_reply:
        quick_reply_payload = quick_reply.get('payload')
        return "Quick reply will be handled elsewhere"
    if message_attachments:
        attachment_type = message_attachments[0]['type']
        if attachment_type == "location":
            latitude = message_attachments[0]['payload']['coordinates']['lat']
            longitude = message_attachments[0]['payload']['coordinates']['long']
            response = offcampus_dining_request_msg(result, latitude, longitude)
            print(page.send(recipient_id, response))
        else:
            print(page.send(recipient_id, "Here's a handpicked meme by Rafael Ortiz of Columbia buy/sell memes fame."))
            meme = get_meme_msg(result)
            print(page.send(recipient_id, meme))
        return "Done handling attachments"

    if intent in Msg_Fn_Dict:
        msg = get_generic_or_msg(intent,result)
        print(type(msg))
        if type(msg) is list:
            print('sending as list')
            print(page.send(recipient_id, msg))
        if type(msg) is str:
            print('sending as str')
            try:
                chunks = chunkify(msg)
                for chunk in chunks:
                    print(page.send(recipient_id, chunk))
            except:
                return ""
        else:
            print('sending as other')
            print(msg)
            print(page.send(recipient_id, msg))

    elif "smalltalk" in result['action']:
        speech = result['fulfillment']['speech']
        if len(speech) == 0:
            msg = "Interesting... I don't really know how to respond to that."
            print(page.send(recipient_id, msg))
        else:
            print(page.send(recipient_id, speech))

    elif defaultResponse != '':
        print('sending default response')
        print(page.send(recipient_id, defaultResponse))

    else:
        error = "I didn't catch that. Ask me again?"
        page.send(recipient_id, error)
    cur.close()
    conn.close()
    page.typing_off(recipient_id)

@page.handle_read
def received_message_read(event):
    watermark = event.read.get("watermark")
    seq = event.read.get("seq")
    return "received message read"


@page.handle_delivery
def received_delivery_confirmation(event):
    delivery = event.delivery
    message_ids = delivery.get("mids")
    watermark = delivery.get("watermark")

    if message_ids:
        for message_id in message_ids:
            pass
    return "delivery confirmed"

@page.handle_echo
def received_echo(event):
    message = event.message
    message_id = message.get("mid")
    app_id = message.get("app_id")
    metadata = message.get("metadata")
    return "Echo received done"

@page.after_send
def after_send(payload, response):
    return "after send done"


@page.callback(['stress', 'alcohol', 'wellness', 'depression', 'LGBT', 'eating-disorders', 'suicide', 'sleep', 'sexual-assault'])
def callback_clicked_button(payload, event):
    recipient_id = event.sender_id
    page.send(recipient_id, health_resources(payload))
    return "health/welness callback done"

if __name__ == "__main__":
    app.run()
