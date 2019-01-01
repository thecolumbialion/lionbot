from bs4 import BeautifulSoup
import requests


def find_open():
    """
    Returns a list of all the current open libraries
    """
    file = requests.get("https://hours.library.columbia.edu")
    soup = BeautifulSoup(file.content, "html.parser")

    libraries = []

    # lst_mid = soup.findAll("p", class_="clearfix")
    # lst_mid = soup.findAll("ul", class_="lib-list")
    lst_mid = soup.findAll("li", class_="location-item")
    # print((lst_mid))
    for x in lst_mid:
        element = x.find("a")
        print(element.text)  # MOMO CHANGED THIS prints name
        closing = ""
        ele = x.findAll("span", class_="closes-at pull-right")
        # print(ele)
        # ele = x.findAll("small", class_="closes_at_note pull-right")
        for val in ele:
            closing = val.text
            print(closing)
            print("-------------")
            library = element.get_text()
            if closing:
                lib_and_hours = library + " | " + closing
                libraries.append(lib_and_hours)
    return libraries


def libraries_msg(result):
    try:
        open_lib = find_open()
    except:
        open_lib = []
    if len(open_lib) < 1:
        msg = "There are no libraries currently open"
        return msg
    msg = "Here's what libraries are open:\n"
    for library in open_lib:
        msg += library + "\n"
    msg = msg[:len(msg)-1]
    return msg


if __name__ == '__main__':
    find_open()
