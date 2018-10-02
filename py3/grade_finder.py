#!/usr/bin/env python

from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Match
from elasticsearch import Elasticsearch

client = Elasticsearch(hosts=['https://4591566ca3ea460f8d529041fd55771e.us-east-1.aws.found.io:9243/'],
                       http_auth=('elastic:xLYRcEDVC7NIZscysN0u0Zwp'))


def get_restaurant_results(restaurant_name):
    print('Getting restaurant results for {}'.format(restaurant_name))

    s = Search(using=client)
    s.query = Match(name={'query': restaurant_name,
                          'fuzziness': 'AUTO',
                          'operator': 'and'})

    results = []
    for result in s:
        print('result is {}'.format(result))
        results.append({
            'name': result['name'],
            'address': result['address']['street'],
            'borough': result['address']['city'],
            'grade': result['grade']
        })

    return results


def main():
    restaurant_name = input('Enter a restaurant in New York City: ').strip()
    return get_restaurant_results(restaurant_name)


if __name__ == '__main__':
    main()