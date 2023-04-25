#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 12:51:12 2023
@author: Nick, Samson, Masu (Team: Cold Brew)
"""

import json
import requests

# call_api(name)
# Parameters: name - basic animal name string such as Lynx, Tiger, or Panda
# Returns: Python list formatted json array document provided by api-ninja
# Description: call api-ninja's animal api with an animal name from parameter
#              If http status code is not 200, print it with error message
def call_api(name):
    # Call API
    api_url = 'https://api.api-ninjas.com/v1/animals?name={}'.format(name)
    response = requests.get(api_url, headers={'X-Api-Key': 'ztezdcjp1SeG6H1Qy/jMsA==6ZC7V50Q45XOpgnu'})

    # Return json document formatted by json.loads method
    if response.status_code == requests.codes.ok:
        return json.loads(response.text)
    else:
        print("API Call Error:", response.status_code, response.text)

# wording(animal_dict)
# Parameters: animal_dict - a dict object selected from api response in main routine
# Returns: display formatted string value
# Description: convert json to string with easy to understand formatting
def wording(animal_dict):
    # wording string value
    explanation = ''

    # Name
    explanation += '# Name' + '\n'
    explanation += '    ' +animal_dict.get('name') +'\n'

    # Taxonomy
    explanation += '# Taxonomy' + '\n'
    for k, v in animal_dict.get('taxonomy').items():
        explanation += '    ' + k + ': ' + v + '\n'

    # Location
    explanation += '# Location' + '\n'
    location_list = animal_dict.get('locations')
    for location in location_list:
        explanation += '    ' + location +'\n'

    # Characteristics
    explanation += '# Characteristics' + '\n'
    for k, v in animal_dict.get('characteristics').items():
        explanation += '    ' + k + ': ' + v + '\n'

    return explanation


# for debug purpose only
def main():
    response = call_api('Lynx')
    print(len(response))
    print(response[0])
    animal_dict = dict(response[0])
    print(wording(animal_dict))

if __name__ == '__main__':
    main()
