from urllib.parse import urlencode, quote_plus


def make_link(text):
    # link_start = "http://lmgtfy.com/?"
    link_start = "https://www.google.com/#"
    search_query = {'q': text}
    params = urlencode(search_query, quote_via=quote_plus)
    link = link_start + params
    return link


def wisdom_search(result):
    try:
        question = result['parameters']['q']
    except BaseException:
        msg = "I'm not sure what that is. Try again?"
    columbiafy_question = question
    google_link = make_link(columbiafy_question)
    msg = "I don't think I have a great answer for that (yet). In the meantime, let me refer you to a close friend for help: " + google_link
    return msg


class BotSearch:
    def __init__(self, base_link):
        self.base_link = base_link

    def make_link(self, text):
        search_query = {'q': text}
        params = urlencode(search_query, quote_via=quote_plus)
        link = self.base_link + params
        return link

    def search(self, question, intent):
        if intent == "wisdom_search":
            columbiafy_question = question + "columbia university"
            google_link = make_link(columbiafy_question)
            msg = "I don't think I have a great answer for that (yet). In the meantime, let me refer you to a close friend for help: " + google_link
            return msg
        google_link = make_link(question)
        msg = "I don't think I have a great answer for that (yet). In the meantime, let me refer you to a close friend for help: " + google_link
        # bot.send_text_message(recipient_id, msg)
        return msg
