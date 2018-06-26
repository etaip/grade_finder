import json
from grade_finder import get_restaurant_results

def get_grade_by_name(event, context):
    print('Received event: {}'.format(event))
    event_input = json.loads(event) if isinstance(event, str) else event
    restaurant_name = event_input['pathParameters']['name'].lower().strip()
    results = get_restaurant_results(restaurant_name)

    response = {
        "statusCode": 200,
        "body": json.dumps(results)
    }

    print('Response to be returned is: {}'.format(response))
    return response
