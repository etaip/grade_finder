import requests
import http
from datetime import datetime
from string import ascii_lowercase
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Index
from documents.restaurant import Restaurant, Address

RESTAURANT_COUNT_URL = 'http://a816-restaurantinspection.nyc.gov/RestaurantInspection/dwr/call/plaincall/' \
                       'RestaurantSpringService.getTotalCountCriteria.dwr'
RESTAURANT_COUNT_DATA = 'callCount=1\n' \
                        'page=/RestaurantInspection/SearchBrowse.do\n' \
                        'httpSessionId=\n' \
                        'scriptSessionId=707\n' \
                        'c0-scriptName=RestaurantSpringService\n' \
                        'c0-methodName=getTotalCountCriteria\n' \
                        'c0-id=0\n' \
                        'c0-param0=string:name%20%3A_{}\n' \
                        'batchId=1\n'
RESTAURANT_COUNT_RESPONSE_PREFIX = '//#DWR-INSERT\r\n' \
                                   '//#DWR-REPLY\r\n' \
                                   'dwr.engine._remoteHandleCallback(\'1\',\'0\','
RESTAURANT_COUNT_RESPONSE_SUFFIX = ');\r\n'
RESTAURANTS_PER_PAGE = 500
RESTAURANT_SEARCH_URL = 'http://a816-restaurantinspection.nyc.gov/RestaurantInspection/dwr/call/plaincall/' \
                        'RestaurantSpringService.getResultsSrchCriteria.dwr'
RESTAURANT_SEARCH_DATA = 'callCount=1\n' \
                         'page=/RestaurantInspection/SearchResults.do\n' \
                         'httpSessionId=\nscriptSessionId=379\n' \
                         'c0-scriptName=RestaurantSpringService\n' \
                         'c0-methodName=getResultsSrchCriteria\n' \
                         'c0-id=0\nc0-param0=string:name%20%3A_{}\n' \
                         'c0-param1=string:displayOrder\n' \
                         'c0-param2=boolean:true\n' \
                         'c0-param3=number:{}\n' \
                         'c0-param4=number:{}\n' \
                         'batchId={}\n'
BOROUGH_MAP = {
    '1' : 'MANHATTAN',
    '2' : 'BRONX',
    '3' : 'BROOKLYN',
    '4' : 'QUEENS',
    '5' : 'STATEN ISLAND'
}
START_SUBSTRING = 's0.brghCode'
LAST_ENTRY_PREFIX = 'dwr.engine._remoteHandleCallback'


connections.create_connection(hosts=['https://4591566ca3ea460f8d529041fd55771e.us-east-1.aws.found.io:9243/'],
                              http_auth=('elastic:xLYRcEDVC7NIZscysN0u0Zwp'))

def parse_restaurant_count_response(resp_text: str):
    if not resp_text.startswith(RESTAURANT_COUNT_RESPONSE_PREFIX) or not \
            resp_text.endswith(RESTAURANT_COUNT_RESPONSE_SUFFIX):
        print('Invalid response text: {}'.format(resp_text))
        return 0

    count = resp_text[len(RESTAURANT_COUNT_RESPONSE_PREFIX):(-len(RESTAURANT_COUNT_RESPONSE_SUFFIX))]
    if not count.isdecimal():
        print('Invalid response text: {}'.format(resp_text))
        return 0

    return int(count)


def get_restaurant_count(letter: str):
    resp = requests.post(RESTAURANT_COUNT_URL, data=RESTAURANT_COUNT_DATA.format(letter))
    if resp.status_code != http.HTTPStatus.OK:
        print('Received {} response!'.format(resp.status_code))
        return 0

    print(resp.text)
    count = parse_restaurant_count_response(resp.text)
    print('Count is {}'.format(count))

    return count


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


def construct_address(restaurant):
    return restaurant['restBuilding'].strip() + ' ' + restaurant['stName'].strip()


def extract_relevant_data(restaurant_results):
    limited_results = []
    for result in restaurant_results:
        restaurant_data = {
            'name': result['restaurantName'],
            'address': construct_address(result),
            'borough': BOROUGH_MAP[result['brghCode']],
            'grade': result['restCurrentGrade'],
            'zip_code': result['restZipCode']
        }
        limited_results.append(restaurant_data)

    return limited_results


def scan_all_restaurants():
    # Delete the existing index
    restaurants = Index('restaurants')
    if restaurants.exists():
         restaurants.delete()

    # Associate the index with the document type
    restaurants.doc_type(Restaurant)

    # Create the index
    restaurants.create()

    id = 1
    print('Starting restaurant scan...')
    for letter in ascii_lowercase + '#':
        print('Getting restaurants starting with "{}"'.format(letter))
        count = get_restaurant_count(letter)
        batches = count // RESTAURANTS_PER_PAGE + (1 if count % RESTAURANTS_PER_PAGE > 0 else 0)

        for i, batch in enumerate(range(batches)):
            print('Getting batch {}'.format(i))
            resp = requests.post(RESTAURANT_SEARCH_URL,
                                 data=RESTAURANT_SEARCH_DATA.format(letter, batch + 1, RESTAURANTS_PER_PAGE, batch))
            if resp.status_code != http.HTTPStatus.OK:
                print('Received {} response!'.format(resp.status_code))
                continue

            results = extract_relevant_data(parse_response(resp.text))
            for result in results:
                address = Address(street=result['address'],
                                  city=result['borough'],
                                  state='NY',
                                  zip_code=result['zip_code'])
                restaurant = Restaurant(name=result['name'],
                                        address=address,
                                        grade=result['grade'],
                                        updated_at=datetime.now(),
                                        meta={'id': id})
                id += 1
                restaurant.save()

    print('Restaurants scanned successfully!')
