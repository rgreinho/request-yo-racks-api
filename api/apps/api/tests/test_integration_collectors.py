import os

from api.apps.api.collectors.collector import CollectorClient


def integration_test_yelp():
    client_id = os.environ['RYR_COLLECTOR_YELP_CLIENT_ID']
    client_secret = os.environ['RYR_COLLECTOR_YELP_CLIENT_SECRET']

    client = CollectorClient('yelp', oauth2=(client_id, client_secret))
    client.authenticate()
    details = client.retrieve_place_details('221 W North Loop Blvd, Austin, TX 78751', terms='Epoch coffee')
    print(details)


def integration_test_google():
    geocoding_api_key = os.environ['RYR_COLLECTOR_GOOGLE_GEOCODING_API_KEY']
    places_api_key = os.environ['RYR_COLLECTOR_GOOGLE_PLACES_API_KEY']

    # geocode = googlemaps.Client(key=geocoding_api_key)
    # geocode_result = geocode.geocode('221 W N Loop Blvd, Austin, TX 78751')

    epoch_latlong = (30.3186037, -97.72454019999999)
    client = CollectorClient('google', api_key=places_api_key)
    client.authenticate()
    details = client.retrieve_place_details(epoch_latlong)
    print(details)


if __name__ == '__main__':
    test_google()
