from bs4 import BeautifulSoup
import requests

# request_example = {
#     "source": "agent",
#     "resolvedQuery": "what time does butler close",
#     "action": "",
#     "actionIncomplete": False,
#     "parameters": {
#       "libraries": [
#         "Butler Library"
#       ]
#       }
# }

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
        #print(element.text)  # MOMO CHANGED THIS prints name
        closing = ""
        ele = x.findAll("span", class_="closes-at pull-right")

        # print(ele)
        # ele = x.findAll("small", class_="closes_at_note pull-right")
        for val in ele:
            closing = val.text
            #print(closing)
            #print("-------------")
            library = element.get_text()
            if closing:
                lib_and_hours = library + " | " + closing
                libraries.append(lib_and_hours)
    return libraries


def libraries_msg(result):

    #opens list of libraries and hours
    try:
        open_lib = find_open()
    except BaseException:
        open_lib = []
    #accesses the library name you want to specifically select
    specific_lib_name = result['parameters']['libraries'][0]

    #if their input isn't a specific library then it'll display all library info
    if specific_lib_name == 'library' or specific_lib_name == 'None':

        if len(open_lib) < 1:
            msg = "There are no libraries currently open"
            return msg
        msg = "Here's what libraries are open:\n"
        for library in open_lib:
            msg += library + "\n"
        msg = msg[:len(msg) - 1]
        return msg


    else:
        #loops through list of libraries until it finds the specific one
        for library in open_lib:
                lib_name = library.split('| \n', 1)[0]

                #prints out nice message about only that library and its hours
                if specific_lib_name == lib_name or specific_lib_name in lib_name:
                    msg = specific_lib_name + "'s hours for today are " + library.split('| \n', 1)[1].strip().replace('- ','to')
                    return msg
                    #print(msg)


if __name__ == '__main__':
    #print(libraries_msg(request_example))
