from bs4 import BeautifulSoup
import requests
import feedparser
from fbmq import Template


def news_msg(result):
    """ Interface Function for news intent """
    campus_publication = ""
    news_result = []
    try:
        campus_publication = result['parameters']['club']
        campus_publication = campus_publication.lower()
    except BaseException:
        campus_publication = ""
        return "I couldn't get any news from the publication requested."

    if "bwog" in campus_publication:
        news_result = make_bwog_feed()
    elif "spectator" in campus_publication:
        news_result = make_spec_feed()
    else:
        news_result = make_lion_feed()
    # if no results returned
    if news_result == []:
        news_result = ("I couldn't get any news "
                       "updates from the publication requested.")
    response = Template.List(elements=news_result, top_element_style='large')
    return response


def make_lion_feed():
    """ Gets recent lion articles """
    news_articles = []
    thelion = feedparser.parse('http://www.columbialion.com/rss')
    lion_counter = 1
    for feed in thelion['entries']:
        if lion_counter > 4:
            break
        else:
            image = ("http://columbialion.com/wp-content/uploads/2015/08/"
                     "4468318_10157368552385198_1896799578837951965_o.png")
            news_item = Template.GenericElement(
                title=feed['title'],
                subtitle=feed['description'],
                item_url=feed['link'],
                image_url=image,
                buttons=[
                    {
                        'type': 'web_url',
                        'title': 'Read More',
                        'value': feed['link']}])

            news_articles.append(news_item)
            lion_counter += 1
    return news_articles


def make_bwog_feed():
    """ Gets recent bwog articles """
    news_articles = []
    bwog = feedparser.parse('http://www.bwog.com/rss')
    bwog_counter = 1
    for feed in bwog['entries']:
        if bwog_counter > 4:
            break
        else:
            image = "https://i.vimeocdn.com/portrait/7168298_300x300"
            text = "Read more at bwog.com"
            news_item = Template.GenericElement(
                title=feed['title'],
                subtitle=text,
                item_url=feed['link'],
                image_url=image,
                buttons=[
                    {
                        'type': 'web_url',
                        'title': 'Read More',
                        'value': feed['link']}])
            news_articles.append(news_item)
            bwog_counter += 1
    return news_articles


def make_spec_feed():
    student_life = requests.get(
        "http://columbiaspectator.com/News/Student-Life/")
    soup = BeautifulSoup(student_life.text, "html.parser")
    test = soup.findAll("div", {"class": "stories"})
    test_names = test[0].findAll("div", {"class": "article-info"})
    image_links = test_names = test[0].findAll("div", {"class": "row"})
    articles = []
    for line, article in enumerate(test_names, 0):
        one_article = {}
        article_names = test_names[line].findAll(
            "div", {"class": "story-title"})
        article_image = image_links[line].findAll(
            "div",
            {"class": "col-xs-12 col-md-4"})[0].findAll("div",
                                                        {"class":
                                                        "image-container"})[0]
        image_link = article_image.findAll('img', src=True)[0]
        actual_image = image_link['src']
        article_link = article_names[0].findAll('a', href=True)
        article_bylines = test_names[line].findAll("div", {"class": "bylines"})
        article_summary = test_names[line].findAll(
            "div", {"class": "story-summary"})
        title = ""
        link = ""
        byline = ""
        summary = ""
        for title in article_names:
            title = title.text
        for link in article_link:
            link = "http://www.columbiaspectator.com" + link['href']
        for byline in article_bylines:
            byline = byline.text
        for summary in article_summary:
            summary = summary.text
        news_item = Template.GenericElement(
            title=title,
            subtitle=byline,
            item_url=link,
            image_url=actual_image,
            buttons=[
                {
                    'type': 'web_url',
                    'title': 'Read More',
                    'value': link}])

        articles.append(news_item)

    return articles[0:4]
