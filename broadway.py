#############################
# Feature to return on what days a desired meal will occur next
#
#
#
#
############################

from bs4 import BeautifulSoup
import requests


def get_shows():
    request = requests.get("https://www.broadway.org/shows")
    soup = BeautifulSoup(request.content, "html.parser")
    # shows = soup.findAll("ul", class_="list-group")
    shows = soup.findAll(class_="color-white bold")


def get_shows_message():
    try:
        shows = get_shows()
    except:
        shows = "No shows available. Try again later"
