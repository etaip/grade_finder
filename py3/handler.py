import json
from grade_finder import get_restaurant_results, display_results

def get_grade_by_name(event, context):
    #import pdb; pdb.set_trace()
    event_input = json.loads(event) if isinstance(event, str) else event
    restaurant_name = event_input['pathParameters']['name'].lower().strip()
    results = get_restaurant_results(restaurant_name)

    response = {
        "statusCode": 200,
        "body": display_results(results)
    }

    return response
