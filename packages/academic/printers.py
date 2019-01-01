# from printer_list import printers
import itertools

printers = ['Avery 200', 'Broadway 100', 'Broadway 304',
            'Burke 100', 'Burke 300', 'Butler 209',
            'Butler 300', 'Butler 304', 'Butler 304COLOR ',
            'Butler 310 ', 'Butler 401', 'Butler 403',
            'Butler 501', 'Butler 606', 'Campbell 505',
            'Carlton Arms Lobby', 'Carman 112',
            'Claremont 1st Floor', 'Dodge Arts 412',
            'Dodge Arts 5th Floor', 'Dodge Arts 6th Floor',
            'Dodge Music 701', 'EC 1st Floor', 'EC 10', 'EC 18',
            '251 Engineering Terrace', '252 Engineering Terrace',
            'Fairholm Bsmnt', 'Furnald 107', 'Harmony 100',
            'Hartley 100 ', 'Hartley 111', 'IAB 215', 'IAB 310',
            'IAB 323', 'IAB 323 COLOR', 'IAB 509', 'John Jay 100',
            'Kent 200 ', 'Kent 300', 'Lerner 200', 'Lerner 300',
            'Lerner 500 ', 'Lewisohn 300', 'Math 303', 'McBain 100',
            'NWCB 400 ', 'NWCB 600 ', 'Ruggles 1st Floor',
            'River Bsmnt', 'Russell 1st Floor (TC)', 'Schapiro 100 ',
            'Schapiro 108', 'Schermerhorn 558', 'Schermerhorn 601',
            'SIC House Bsmnt', '600 W 113th 1st Floor', 'Statistics 902',
            'Uris 130', 'Wallach 100', 'Wein 100', 'Wien 211',
            'Woodbridge 100', 'Brooks Lab/Classroom (Quad B) ',
            'Diana 307 COLOR', 'Elliott 1st Floor', 'Library',
            'Plimpton 1st Floor', '616 1st Floor',
            'Sulzberger Lounge (Quad Lab A)']


def printers_msg(result):
    msg = "These are the printers available"

    buildings = []
    is_color = False

    if 'campus_buildings' in result['parameters']:
        buildings = result['parameters']['campus_buildings']

    if len(result['parameters']['color_printer']) > 0:
        is_color = True

    printer_list = []
    for i, j in itertools.product(range(len(printers)), range(len(buildings))):
        if buildings[j].upper() in printers[i].upper():
            printer_list.append(printers[i])

    if is_color:
        printer_list = [x for x in printer_list if 'COLOR' in x]

    # if len(printer_list) == 0:
    if not printer_list:
        return "Looks I couldn't find any printers in that area."

    return "These are the printers available:\n" + "\n".join(printer_list)


"""if __name__ == "__main__":
    result = {
        "parameters": {
            "campus_buildings": ["Wallach", "Diana"]
            #"color_printer": "color"
        }
    }
    print(printers_msg(result))"""
