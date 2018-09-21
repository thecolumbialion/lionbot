from fbmq import Template, QuickReply, ButtonPostBack

intro_reply = Template.List(elements=[
    Template.GenericElement("Columbia and Barnard Dining",
                          subtitle="I know dining halls menus and even special Dining events",
                          image_url="http://columbialion.com/wp-content/uploads/2017/04/diningbot.jpg"),
    Template.GenericElement("Campus News",
                          subtitle="News updates direct from The Lion, Bwog, and Spec",
                          image_url="http://columbialion.com/wp-content/uploads/2017/04/newsbot.png"),
    Template.GenericElement("Recommend places to eat",
                          subtitle="I can get you the perfect off-campus meal",
                          image_url="http://columbialion.com/wp-content/uploads/2017/04/offcampusdiningbot.jpg"),
    Template.GenericElement("Broadway Rush Policies",
                          subtitle="Want to find cheap Hamilton tickets? I have tips for that",
                          image_url="http://columbialion.com/wp-content/uploads/2017/04/broadwaybot.png")
], top_element_style='large', buttons=[])


mental_health_resources = Template.List(elements=[
    Template.GenericElement("Columbia Health Resources",
                          subtitle="Here are helpful resources for counseling at Columbia",
                          image_url="http://columbialion.com/wp-content/uploads/2017/04/wellnessbot.png"),
    Template.GenericElement("Counseling and Psychological Services",
                          subtitle="CPS offers counseling, consulation, and crisis intervention ",
                          item_url="https://health.columbia.edu/counseling-and-psychological-services",
                          image_url="https://mundaylab.umd.edu/wp-content/uploads/logo-columbia.png"),
    Template.GenericElement("Furman Counseling",
                          subtitle="Barnard's counseling center for its students",
                          item_url="https://barnard.edu/counsel",
                          image_url="https://barnard.edu/sites/default/files/styles/top_news_view__325x240_/public/barnard-b-blue-square-01.png?itok=tjdz2rnb")
], top_element_style='large', buttons=[])



"""intro_reply = Template.Generic([
    Template.GenericElement("Recommend places to eat",
                          subtitle="Want some A+ restaurant recommendations? Just ask 'Where can I eat off-campus?'",
                          image_url="http://columbialion.com/wp-content/uploads/2017/04/offcampusdiningbot.jpg"),
    Template.GenericElement("Columbia and Barnard Dining",
                          subtitle="I know dining halls menus and even special Dining events.",
                          image_url="http://columbialion.com/wp-content/uploads/2017/04/diningbot.jpg"),
    Template.GenericElement("Health and Wellness",
                          subtitle="I can provide links and phone numbers for mental health and wellness.",
                          image_url="http://columbialion.com/wp-content/uploads/2017/04/wellnessbot.png"),
    Template.GenericElement("Academic Calendar",
                          subtitle="I can help when it comes to remembering all the important academic dates.",
                          image_url="http://columbialion.com/wp-content/uploads/2017/04/academiccalendarbot.png"),
    Template.GenericElement("Campus News",
                          subtitle="I can keep you updated on campus news with from The Lion, Bwog and Spec.",
                          image_url="http://columbialion.com/wp-content/uploads/2017/04/newsbot.png"),
    Template.GenericElement("CUTV Channels",
                          subtitle="Trying to figure out what channel CNN is? I can help with that.",
                          image_url="http://columbialion.com/wp-content/uploads/2017/04/channelsbot.png"),
    Template.GenericElement("Broadway Rush Policies",
                          subtitle="Want to find cheap Hamilton tickets? I have tips for that.",
                          image_url="http://columbialion.com/wp-content/uploads/2017/04/broadwaybot.png"),
    Template.GenericElement("Campus Libraries",
                          subtitle="Just ask and I can let you know which libraries are open.",
                          image_url="http://columbialion.com/wp-content/uploads/2017/04/librariesbot.jpg"),

])"""

health_reply = [ 
QuickReply(title="Stress/Anxiety", payload="stress"),
QuickReply(title="Alcohol and Drugs", payload="alcohol"),
QuickReply(title="Depression", payload="depression"),
QuickReply(title="LGBT", payload="LGBT"),
QuickReply(title="Eating Disorders", payload="eating-disorders"),
QuickReply(title="Suicide", payload="suicide"),
QuickReply(title="Sleep", payload="sleep"),
QuickReply(title="Sexual Assault", payload="sexual-assault"),
QuickReply(title="Other", payload="other")]

#for future deployment with subscriptions feature
"""bot_menu = [Template.ButtonPostBack('Subscriptions', 'MENU_PAYLOAD/Subscriptions'),
Template.ButtonPostBack('Current Features', 'MENU_PAYLOAD/GET_STARTED'),
Template.ButtonPostBack('Health and Wellness', 'MENU_PAYLOAD/health')]"""

bot_menu = [Template.ButtonPostBack('Current Features', 'MENU_PAYLOAD/GET_STARTED'),
Template.ButtonPostBack('Health and Wellness', 'MENU_PAYLOAD/health')]

subscriptions_welcome = "Welcome to Subscriptions. A new feature that allows you to get direct updates from campus clubs."
subscriptions_reply = [ QuickReply(title="Media & Publications", payload="Subscriptions/media&publications"),
QuickReply(title="Technology & Engineering", payload="Subscriptions/technology&engineering"),
QuickReply(title="Political", payload="Subscriptions/political"),
QuickReply(title="Environmental", payload="Subscriptions/environmental"),
QuickReply(title="Medicine", payload="Subscriptions/medicine"),
QuickReply(title="Music & Dance", payload="Subscriptions/music&dance"),
QuickReply(title="Science", payload="Subscriptions/science"),
QuickReply(title="Service", payload="Subscriptions/service")]

def current_features_msg(result):
  return intro_reply
