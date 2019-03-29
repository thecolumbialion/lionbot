import os
import requests
from fbmq import Template

"""
Returns a Template.List which is essentially just a wrapper for a 
python list of Template.Elements.
The list is the 'elements' field of the payload paramter (which is a
dictionary)
"""
def offcampus_dining_request_msg(
        result,
        latitude=40.806209,
        longitude=-73.961733):
    """Interface function"""
    try:
        term = result.parameters['off_campus_food']
    except BaseException:
        term = "boba"
    food_recs = get_recommendation_type(term, latitude, longitude)
    response = Template.List(elements=food_recs, top_element_style='large')
    return response


# we have a different procedure depending on how the user phrased the request
def get_recommendation_type(term, latitude=40.806209, longitude=-73.961733):
    result = get_yelp_info(term, latitude, longitude)
    return result

# set default coordinates to campus in case we do not get a user location

# Returns a list of Tempate.GenericElement objects 
def get_yelp_info(term="", latitude=40.806209, longitude=-73.961733):
    recommendations_list = []
    business_link_base = "https://www.yelp.com/biz/"
    query_limit = 4
    i = 0
    results = query_yelp(term, latitude, longitude, query_limit)
    # if no results, return info for JJ's Place
    if 'businesses' not in results:
        element = Template.GenericElement(
            title="JJ's Place",
            subtitle="A Columbia late night classic",
            item_url="bit.ly/2shtorh",
            image_url="bit.ly/2shtorh",
            buttons=[
                {
                    'type': 'web_url',
                    'title': 'Learn More',
                    'value': "bit.ly/2rcSpAB"}])
        recommendations_list.append(element)
        return recommendations_list
    query_limit = len(results['businesses']) if len(
        results['businesses']) < 4 else query_limit
    for i in range(query_limit):
        business_name = results['businesses'][i]['name']
        business_image = results['businesses'][i]['image_url']
        business_address = results['businesses'][i]['location']['address1']
        yelp_link = business_link_base + results['businesses'][i]['id']
        business_subtitle = "Located at " + business_address + "."
        element = Template.GenericElement(
            title=business_name,
            subtitle=business_subtitle,
            item_url=yelp_link,
            image_url=business_image,
            buttons=[
                {
                    'type': 'web_url',
                    'title': 'Learn More',
                    'value': yelp_link}])
        recommendations_list.append(element)
    return recommendations_list


# Returns a JSON response
def query_yelp(term, latitude, longitude, query_limit):
    headers = {'Authorization': 'Bearer ' + os.environ['YELP_API_KEY']}
    params = {
        'term': term,
        'latitude': latitude,
        'longitude': longitude,
        'locale': 'en_US',
        'limit': query_limit,
        'open_now': 'True'
    }
    query = requests.get(
        'https://api.yelp.com/v3/businesses/search',
        headers=headers,
        params=params)
    return query.json()
