import json
import requests
import html

url = 'https://events.columbia.edu/feeder/main/eventsFeed.do?f=y&sort=dt'\
    'start.utc:asc&fexpr=(((vpath=%22/public/aliases/Audience/Student%22)))%20an'\
    'd%20(categories.href=%22/public/.bedework/categories/org/UniversityEvents%2'\
    '2)%20and%20(entity_type=%22event%22%7Centity_type=%22todo%22)&skinName=lis'\
    't-json&count=10'

file = requests.get(url)

file_json = file.json()
print(file_json['bwEventList']['events'][0]['summary'])
