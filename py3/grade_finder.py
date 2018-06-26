#!/usr/bin/env python

import requests
import http

SEARCH_URL = 'http://a816-restaurantinspection.nyc.gov/RestaurantInspection/dwr/call/plaincall/' \
             'RestaurantSpringService.getResultsSrchCriteria.dwr'
SEARCH_PREFIX = 'callCount=1\n' \
                'page=/RestaurantInspection/SearchResults.do\n' \
                'httpSessionId=\n' \
                'scriptSessionId=${scriptSessionId}485\n' \
                'c0-scriptName=RestaurantSpringService\n' \
                'c0-methodName=getResultsSrchCriteria\n' \
                'c0-id=0\n' \
                'c0-param0=string:name%20%3A'
SEARCH_SUFFIX = '\nc0-param1=string:\n' \
                'c0-param2=boolean:true\n' \
                'c0-param3=number:1\n' \
                'c0-param4=number:20\n' \
                'batchId=0'
BOROUGH_MAP = {
    '1' : 'MANHATTAN',
    '2' : 'BRONX',
    '3' : 'BROOKLYN',
    '4' : 'QUEENS',
    '5' : 'STATEN ISLAND'
}
DISPLAY_MAP = {
    'brghCode' : 'Borough',
    'cuisineType' : 'Cuisine Type',
    'lastInspectedDate' : 'Last Inspected Date',
    'restCurrentGrade' : 'Grade',
    'restZipCode' : 'ZIP Code',
    'scoreViolations' : 'Score Violations',
    'telephone' : 'Telephone'
}
START_SUBSTRING = 's0.brghCode'
LAST_ENTRY_PREFIX = 'dwr.engine._remoteHandleCallback'


def construct_address(restaurant):
    return restaurant['restBuilding'].strip() + ' ' + restaurant['stName'].strip()


def parse_response(resp):
    results = []
    start = resp.find(START_SUBSTRING)
    if start == -1:
        return results

    unparsed_results = resp[start:].split('\n')
    for restaurant in unparsed_results:
        if restaurant.startswith(LAST_ENTRY_PREFIX):
            return results

        restaurant_info = restaurant.split(';')
        restaurant_dict = {}
        for field in restaurant_info:
            try:
                key, val = field.split('=')
            except ValueError:
                continue

            key = key.split('.')[1]
            restaurant_dict[key] = val.replace('"', '')

        results.append(restaurant_dict)

    # Should have returned already, but just in case the LAST_ENTRY_PREFIX wasn't found
    return results


def display_results(results):
    formatted_results = ''
    for result in results:
        formatted_results += 'Restaurant Name: {}\n'.format(result['restaurantName'])
        formatted_results += 'Address: {}\n'.format(construct_address(result))
        for key in result:
            if key in DISPLAY_MAP:
                if key == 'brghCode':
                    val = BOROUGH_MAP[result[key]]
                else:
                    val = result[key]
                formatted_results += DISPLAY_MAP[key] + ': ' + val + '\n'
        formatted_results += '=' * 100 + '\n'
    return formatted_results


def extract_relevant_data(restaurant_results):
    limited_results = []
    for result in restaurant_results:
        restaurant_data = {
            'name': result['restaurantName'],
            'address': construct_address(result),
            'borough': BOROUGH_MAP[result['brghCode']],
            'grade': result['restCurrentGrade']
        }
        limited_results.append(restaurant_data)

    return limited_results


def get_restaurant_results(restaurant_name):
    print('Getting restaurant results for {}'.format(restaurant_name))
    resp = requests.post(SEARCH_URL, data=SEARCH_PREFIX + restaurant_name + SEARCH_SUFFIX)
    if resp.status_code != http.HTTPStatus.OK:
        print('Received {} response!'.format(resp.status_code))
        return []
    else:
        results = parse_response(resp.text)

        return extract_relevant_data(results)


def main():
    restaurant_name = input('Enter a restaurant in New York City: ').strip()
    results = get_restaurant_results(restaurant_name)
    print(display_results(results))


if __name__ == '__main__':
    main()