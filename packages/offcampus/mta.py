# taken and modified from https://github.com/craigcurtin/mta
import urllib.request
from lxml import etree


class MTA(object):
    '''class to hold data about a NYC MTA line'''

    def __init__(self, name, status, text, date, time):
        '''data attributes are named same as XML attributes'''
        self.name = name
        self.status = status
        self.text = text
        self.date = date
        self.time = time

    def getName(self):
        return self.name

    def getStatus(self):
        return self.status

    def getText(self):
        return self.text

    def getDate(self):
        return self.date

    def getTime(self):
        return self.time

    def getMode(self):
        return self.mode


class Subway(MTA):
    '''class to hold data about a NYC Subway line'''

    def __init__(self, name, status, text, date, time):
        super(Subway, self).__init__(name, status, text, date, time)
        self.Mode = 'subway'


class Bus(MTA):
    '''class to hold data about a NYC Bus line'''

    def __init__(self, name, status, text, date, time):
        '''data attributes are named same as XML attributes'''
        super(Bus, self).__init__(name, status, text, date, time)
        self.Mode = 'bus'


class BT(MTA):
    '''class to hold data about a NYC Bridge and Tunnel line'''

    def __init__(self, name, status, text, date, time):
        '''data attributes are named same as XML attributes'''
        super(BT, self).__init__(name, status, text, date, time)
        self.Mode = 'bt'


class MTAStatus():
    '''Get data from MTA web site
       this mtaData() function returns a dictionary of k,v

        KEY-> value is Subway() instance
       '123' -> Subway('123', 'GOOD ...', 'Text', 'Date', 'Time')
       '456' -> Subway('456', 'GOOD ...', 'Text', 'Date', 'Time')

       NOTE: ... all MTA Subway lines are not availble

       Data is scraped from http://web.mta.info/status/serviceStatus.txt

       Drop above http, in your favorite browser to see the data

    '''

    def __init__(self):
        url = 'http://web.mta.info/status/serviceStatus.txt'
        self.subwayDataAsXML = urllib.request.urlopen(url).read()
        self.root = etree.XML(self.subwayDataAsXML)

        # get MTA metadata
        self.responseCode = self.root.xpath('responsecode')[0].text
        self.timeStamp = self.root.xpath('timestamp')[0].text

    def getReportTime(self):
        return self.timeStamp

    def getSubway(self):
        '''Subway data'''
        self.subwayDict = {}
        # iterate through XML data, only care about Subway data for now
        for count in range(len(self.root.xpath('subway/line/name'))):
            name = self.root.xpath('subway/line/name')[count].text
            status = self.root.xpath('subway/line/status')[count].text
            text = self.root.xpath('subway/line/text')[count].text
            date = self.root.xpath('subway/line/Date')[count].text
            time = self.root.xpath('subway/line/Time')[count].text
            s = Subway(name, status, text, date, time)

            #s = Subway(self.root.xpath('subway'))
            self.subwayDict[s.getName()] = s
        return self.subwayDict

    def getBus(self):
        '''Bus data'''
        self.busDict = {}
        # iterate through XML data, only care about Subway data for now
        for count in range(len(self.root.xpath('bus/line/name'))):
            name = self.root.xpath('bus/line/name')[count].text
            status = self.root.xpath('bus/line/status')[count].text
            text = self.root.xpath('bus/line/text')[count].text
            date = self.root.xpath('bus/line/Date')[count].text
            time = self.root.xpath('bus/line/Time')[count].text
            bus = Bus(name, status, text, date, time)
            # set the SubwayName = Subway() class data
            self.busDict[bus.getName()] = bus
        return self.busDict


def subwaystatus():

    mtaStatus = MTAStatus()
    timeMTA_ReportedData = mtaStatus.getReportTime()

    subwayDictionary = mtaStatus.getSubway()
    # print('as of %s MTA Reported\n') % (timeMTA_ReportedData) # this is
    # provided by MTA
    response = "Here is the current subway info for NYC Transit:\n"
    for name in sorted(subwayDictionary.keys()):
        line = '%s is experiencing: %s' % (
            subwayDictionary[name].getName(),
            subwayDictionary[name].getStatus())
        mta_web_link = "(http://www.mta.info/status/subway/" + \
            subwayDictionary[name].getName() + ")"
        response += line + " " + mta_web_link + "\n"
    response = response[:-1]
    return response


def mta_subway_info_msg(result):
    """Interface function"""
    try:
        msg = subwaystatus()
    except BaseException:
        msg = ("Looks like all MTA lines are reporting good service. "
               "Check http://www.mta.info/status/subway/123 for updates"
               " regarding the 1 train.")
    return msg
