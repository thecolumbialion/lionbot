""" Find dining halls that are open in the future. - built by Momo Arbeit """
import re
import requests
from bs4 import BeautifulSoup

# https://barnard.edu/dining/locations/diana-center-cafe
# https://barnard.edu/dining/locations/hewitt-dining-hall
# https://barnard.edu/dining/locations/lizs-place


def get_soup(url):
    file = requests.get(url)
    # file = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(file.content, "html.parser")
    return soup


def find_hall_hours(url):
    # file = requests.get("https://barnard.edu/dining/locations/hewitt-dining-hall")
    # soup = BeautifulSoup(file.content, "html.parser")

    soup = get_soup(url)
    temp = soup.select('div[class="field-item even"]')
    open_hours = str(temp).rsplit('</em></p>', 1)[1]

    i = 0
    while i <= len(open_hours):

        if 'h4' in open_hours.splitlines()[i]:
            if i > 1:
                print("-------------")

        open_hours = open_hours.replace("<br>", "")
        print(re.sub("<.*?>", "", open_hours.splitlines()[i]))
        i += 1

    return open_hours


if __name__ == '__main__':
    find_hall_hours()
