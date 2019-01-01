import bs4
import requests


def get_shows():
    # make a dictionary where key is show name and value is a dictionary of
    # show info
    shows = {}
    url = "http://broadwayforbrokepeople.com/"
    get_html = requests.get(url)
    soup = bs4.BeautifulSoup(get_html.text, "html.parser")
    test = soup.find_all('table')
    for row in test[0].find_all("tr"):
        row_start = row.find_all('td')
        # remove any leading or trailing spaces
        show = row_start[1].text.strip()
        theater = row_start[2].text
        close_date = row_start[4].text
        performance_schedule = row_start[5].text
        if(len(row_start) > 6):
            rush_policy = row_start[6].text
            g = row_start[6]
            rush_link_html = g.find_all('a')
            rush_link = list(rush_link_html)
            if len(rush_link) > 0:
                rush_link = make_rush_link(rush_link)
            else:
                rush_link = "%s does not have a rush policy yet." % (show)

        else:
            rush_policy = "TBA"

        # make dictionary of values related to a specifc show and add to
        # dictionary for all shows
        show_dict = make_show_dictionary(
            theater,
            close_date,
            performance_schedule,
            rush_policy,
            rush_link)
        shows[show] = show_dict
    return shows


def make_rush_link(rush_link):
    javascript_line = rush_link[0]['href']
    # javascript_line looks like this: javascript:popupWindow('tgcdetail.html',500,400,100,100,100,100)
    # start will get us to first character of show.html link
    start = javascript_line.index('(') + 2
    # get index of last character of show.html link
    end = javascript_line.index(')') - 25
    show_html = javascript_line[start:end]
    rush_policy_link = "http://broadwayforbrokepeople.com/" + show_html
    return rush_policy_link


def make_show_dictionary(
        theater,
        close_date,
        performance_schedule,
        rush_policy,
        rush_link):
    show_dict = {}
    show_dict['theater'] = theater
    show_dict['close_date'] = close_date
    show_dict['performance_schedule'] = performance_schedule
    show_dict['rush_policy'] = rush_policy + "\n" + rush_link
    show_dict['rush_link'] = rush_policy + "\n" + rush_link
    return show_dict


def search_show(show_name, desired_info=['rush_policy']):
    shows = get_shows()
    # list of shows to check based on show_name given by user (in case they
    # don't give full show title)
    check_shows = []
    statement = ""
    if len(show_name) == 0:
        result = "I'd be happy to help you get some rush tickets. Could you ask me about a specific show though? (ex. 'How do I rush Hamilton?')"
        return result
        #bot.send_text_message(recipient_id, result)
    if len(desired_info) == 0:
        found_shows = []
        try:
            for key in shows.keys():
                if show_name.lower() in key.lower():
                    found_shows.append(key)
            if len(found_shows) == 0:
                message = "Looks like %s is not currently a show on Broadway." % (
                    show_name)
                return message
                #bot.send_text_message(recipient_id, message)
            desired_info = ['rush_policy', 'theater']
            for value in desired_info:
                try:
                    for show in found_shows:
                        result = shows[show][value]
                        statement = show + "\n" + result
                    return statement
                    #bot.send_text_message(recipient_id, statement)
                except BaseException:

                    result = "Looks like I couldn't find out more about %s for you." % (
                        value)
                    #bot.send_text_message(recipient_id, result)
                    return result
        except BaseException:
            message = "What information do you want about the show? I don't know what to check."
            #bot.send_text_message(recipient_id, message)
            return message
    for key in shows.keys():
        #print(show_name.lower() + " " + key.lower())
        #print(show_name.lower() == key.lower())
        if show_name.lower() in key.lower():
            check_shows.append(key)
    if len(check_shows) == 0:
        message = "Looks like %s is not currently a show on Broadway." % (
            show_name)
        # print(message)
        #bot.send_text_message(recipient_id, message)
        return message
    for value in desired_info:
        try:
            for show in check_shows:
                result = shows[show][value]
                statement = show + "\n" + result
                #bot.send_text_message(recipient_id, statement)
                return statement
        except BaseException:
            result = "Looks like I couldn't find out more about %s for you." % (
                value)
            # print(result)
            #bot.send_text_message(recipient_id, result)
            return result
    # else:
        #print("That show does not seem to on Broadway yet.")


def broadway_rush_msg(result):
    """Interface function"""
    try:
        show = result['parameters']['broadway_shows']
        desired_info = result['parameters']['broadway_show_info']
        msg = search_show(show, desired_info)
    except BaseException:
        msg = "Looks like I couldn't find that show's information. Try again?"

    return msg
