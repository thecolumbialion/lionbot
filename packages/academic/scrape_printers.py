import sys
import requests
from bs4 import BeautifulSoup

CUIT_PRINTERS_URL = "https://cuit.columbia.edu/printer-locations"


def get_printers():
    try:
        r = requests.get(CUIT_PRINTERS_URL)
    except requests.exception.RequestException as e:
        print(e)
        sys.exit(1)

    soup = BeautifulSoup(r.content)
    locations = soup.find("div", id="text-3151").text + soup.find("div", id="text-3153").text
    locations = locations.replace("\xa0", "").split("\n")
    locations = [x for x in locations if x != '' and x.find("PawPrint") == -1]

    return locations


if __name__ == "__main__":
    f = open('printer_list.py', 'w')
    f.write("printers = " + str(get_printers()))
    f.close()
