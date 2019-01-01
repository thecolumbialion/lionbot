import requests
from bs4 import BeautifulSoup

"""THIS FILE IS CURRENTLY NOT IN USE"""


def main():
    site = requests.get("http://density.adicu.com")
    soup = BeautifulSoup(site.text, "lxml")
    locations = soup.findAll("li", {"class": "list-group-item"})
    print(locations[0].findAll("h4"))
    for place in locations:
        location = place.findAll("h4")[0].text
        print(location)
        # print(' '.join(place.text.split()))
        progress = place.findAll("div", {"class": "progress"})
        progress_percentage = progress[0].text
        progress_percentage = ' '.join(progress_percentage.split())
        print(progress_percentage)
        print("----------------")


main()
