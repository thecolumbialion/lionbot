import os
import heapq
import requests

auth_key = os.environ['DENSITY_API_KEY']
types_of_places = {
    'eat': [
        "JJ's Place",
        "John Jay Dining Hall",
        "John Jay"],
    'study': [
        "Avery",
        "Butler",
        "Lehman Library",
        "Lerner",
        "Northwest Corner Building",
        "East Asian Library",
        "Uris"]}


def density_msg(result):
    try:
        location = result['parameters']['density_entities']
    except BaseException:
        location = 'NoCo'

    url = 'http://density.adicu.com/latest?auth_token=' + auth_key
    payload = ''
    response = requests.request('GET', url, data=payload)

    return parse_json(response, location)


def parse_json(response, location):
    """
    Returns a list of locations based on what the user is asking for
    :param response: (String) Density API call result
    :param location: (String) String representation of the location
                              the user is asking about.
    :return: (String) Formatted results showing % full for location
    """
    json_response = response.json()
    building_parameter = 'building_name'
    floor_parameter = 'group_name'
    result_list = []
    percent_parameter = 'percent_full'
    match_threshold = 0.8
    buildings_comparison_number = 5
    m_heap = []

    if location in ('study', 'eat'):
        for place in json_response['data']:
            if place[building_parameter] in types_of_places[location]:
                heapq.heappush(
                    m_heap, (place[percent_parameter], place[floor_parameter]))

        result_list.append(
            'These are the least crowded places to ' +
            str(location) +
            ' on campus right now:')

        for i in range(min(buildings_comparison_number, len(m_heap))):
            item = heapq.heappop(m_heap)
            result_list.append(
                '\t' + item[1] + ' is ' + str(item[0]) + '% full')
    else:
        for place in json_response['data']:
            temp_match = match_percentage(
                place, building_parameter, floor_parameter, location)
            if temp_match > match_threshold:
                result_list.append(
                    place[floor_parameter] + ' is ' + str(place[percent_parameter]) + '% full.')
    return list_to_str(result_list)


def list_to_str(list_name):
    """
    Formats a list into a string.
    :param list_name: (List of String) List to be formatted
    :return: (String) String representation of list
    """
    final_str = ''
    for string in list_name:
        final_str += string + '\n'

    return final_str


def match_percentage(place, building_parameter, floor_parameter, location):
    ratio = max(
        dice_coefficient(
            place[building_parameter],
            location),
        dice_coefficient(
            place[floor_parameter],
            location))
    return ratio


def dice_coefficient(a, b):
    """
    Creates a coefficient that shows how similar
        two strings are based on bigrams
    :param a: (String) String 1
    :param b: (String) String 2
    :return: (float) percentage match
    """
    if not len(a) or not len(b):
        return 0.0
    # quick case for true duplicates
    if a == b:
        return 1.0
    # if a != b, and a or b are single chars, then they can't possibly match
    if len(a) == 1 or len(b) == 1:
        return 0.0

    # use python list comprehension, preferred over list.append()
    a_bigram_list = [a[i:i + 2] for i in range(len(a) - 1)]
    b_bigram_list = [b[i:i + 2] for i in range(len(b) - 1)]

    a_bigram_list.sort()
    b_bigram_list.sort()

    # assignments to save function calls
    lena = len(a_bigram_list)
    lenb = len(b_bigram_list)
    # initialize match counters
    matches = i = j = 0
    while (i < lena and j < lenb):
        if a_bigram_list[i] == b_bigram_list[j]:
            matches += 2
            i += 1
            j += 1
        elif a_bigram_list[i] < b_bigram_list[j]:
            i += 1
        else:
            j += 1

    score = float(matches) / float(lena + lenb)
    return score
