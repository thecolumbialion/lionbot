import re


def get_networks():
    """
    Reads in channels.txt

    Return:
        dict: a dictionary of current channel listings
    """
    channels_dict = {}
    channels = open('./packages/housing/channels.txt', 'r')
    channel_num = ""
    for index, line in enumerate(channels):
        stripped_line = re.sub('<[^<]+?>', '', line)
        if index % 2 == 0:
            channel_num = stripped_line.rstrip('\n')
        else:
            channel = stripped_line.rstrip('\n')
            channels_dict[channel] = channel_num
    return channels_dict


def find_network(network):
    network = network.lower()
    channels_dict = get_networks()
    results = []
    response = ""
    for channel_listing in channels_dict.keys():
        channel_listing_lower = channel_listing.lower()
        if network in channel_listing_lower:
            channel_num = channels_dict[channel_listing]
            channel_result = channel_listing + ": " + channel_num
            results.append(channel_result)
    if not results:
        msg = "Sorry, I couldn't find any information about that TV channel."
        return msg
    for line in results:
        response += line + "\n"
    response = response.rstrip()
    return response


def tv_network_msg(result):
    channel = result['parameters']['tv_network']
    msg = find_network(channel)
    return msg
