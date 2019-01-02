import pickle


def clubs_msg(result):
    try:
        club = result['parameters']['club']
    except BaseException:
        club = "The Lion"
    return find_clubs(club)


def make_club_dict():
    """
    Store both club name and its acronym as key, and the
    club info as value into the file club_dict

    """
    club_dict = {}
    club_file = open('./packages/clubs/clubs.csv')
    for club in club_file:
        club_info = club.split("\t")
        if len(club_info) < 2:
            continue
        clubname = club_info[0].strip()
        acronym = "".join(word[0] for word in clubname.split())
        club_dict[clubname] = club_info[1].strip()
        club_dict[acronym] = club_info[1].strip()
    club_file.close()
    output_file = open("./club_dict", "wb")
    pickle.dump(club_dict, output_file)
    output_file.close()


def find_clubs(club):
    """
    Args:
        club (str): a string from the user
    Return:
        results: list of strings, one of which should be
                 what the user is looking for

    If the list is empty: no result is found.
    If the list has multiple entries: any one
    of them might be the club the user is looking for.
    In that case, the bot should handle the logic to
    check with the users which club is the one they want.
    """

    club = club.lower()
    input_file = open("./club_dict", "rb")
    clubs_dict = pickle.load(input_file)
    input_file.close()
    results = []
    response = ""
    for club_name in clubs_dict.keys():
        club_name_lower = club_name.lower()
        if club in club_name_lower:
            club_result = club_name + ": " + clubs_dict[club_name]
            results.append(club_result)
    return results
