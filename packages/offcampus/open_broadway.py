import os,sys
from bs4 import BeautifulSoup
import requests
import datetime


def open_broadway_shows():
        r = requests.get("https://www.broadway.org/shows");
        soup = BeautifulSoup(r.content, "html.parser")
        shows = soup.findAll(class_="color-white bold")
        response = ""
        for show in shows:
            response += show.text + ", "
        return response


def open_broadway_shows_msg(result):
    """Interface function"""
    msg = ""
    try:
        show = result['parameters']['open_broadway_shows']
        desired_info = result['parameters']['currently_open_shows']
        msg = open_broadway_shows()

        if msg == "":
            msg = "Cannot find open shows. Try again later"

    except:
        msg = "Cannot find open shows. Try again later"

    return msg

if __name__ == '__main__':
    open_shows()
