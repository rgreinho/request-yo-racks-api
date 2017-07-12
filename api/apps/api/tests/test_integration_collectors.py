import json
import os

from api.apps.api.collectors.collector import CollectorClient
# from collectors.collector import CollectorClient
from api.apps.api.collectors.collector import GoogleCollector


def integration_test_yelp():
    client_id = os.environ['RYR_COLLECTOR_YELP_CLIENT_ID']
    client_secret = os.environ['RYR_COLLECTOR_YELP_CLIENT_SECRET']

    client = CollectorClient('yelp', oauth2=(client_id, client_secret))
    client.authenticate()
    details = client.retrieve_place_details('221 W North Loop Blvd, Austin, TX 78751', terms='Epoch coffee')
    print(details)


def integration_test_google_00():
    geocoding_api_key = os.environ['RYR_COLLECTOR_GOOGLE_GEOCODING_API_KEY']
    places_api_key = os.environ['RYR_COLLECTOR_GOOGLE_PLACES_API_KEY']

    # geocode = googlemaps.Client(key=geocoding_api_key)
    # geocode_result = geocode.geocode('221 W N Loop Blvd, Austin, TX 78751')

    epoch_latlong = (30.3186037, -97.72454019999999)
    client = CollectorClient('google', api_key=places_api_key)
    client.authenticate()
    details = client.retrieve_place_details(epoch_latlong)
    print(details)


def integration_test_google_search_00():
    """
    Use jq to parse the json output:

        cat google_collector_search_epoch_coffee.json | jq '.results[] | {name: .name, place_id: .place_id}'
    """

    geocoding_api_key = os.environ['RYR_COLLECTOR_GOOGLE_GEOCODING_API_KEY']
    places_api_key = os.environ['RYR_COLLECTOR_GOOGLE_PLACES_API_KEY']

    # geocode = googlemaps.Client(key=geocoding_api_key)
    # geocode_result = geocode.geocode('221 W N Loop Blvd, Austin, TX 78751')

    epoch_latlong = (30.3186037, -97.72454019999999)
    gmaps_places = GoogleCollector()
    gmaps_places.authenticate(api_key=places_api_key)
    search_results = gmaps_places.search_place(epoch_latlong)
    print(json.dumps(search_results, indent=2))


def integration_test_google_place_details_00():
    """
    Use jq to parse the json output:

        cat google_collector_details_epoch_coffee.json | jq '.result | {name: .name, address: .formatted_address, phone: .formatted_phone_number, website: .website}'
    """
    places_api_key = os.environ['RYR_COLLECTOR_GOOGLE_PLACES_API_KEY']
    gmaps_places = GoogleCollector()
    gmaps_places.authenticate(api_key=places_api_key)
    details = gmaps_places.retrieve_place_details('ChIJG-gJw2vKRIYROWi2uwOp8QE')
    print(json.dumps(details, indent=2))


if __name__ == '__main__':
    integration_test_google_place_details_00()
