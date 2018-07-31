import json
import os

from api.apps.api.collectors.generic import CollectorClient
from api.apps.api.collectors.google import GoogleCollector
from api.apps.api.collectors.base import PlaceSearchSummary


def integration_test_yelp_search_place():
    client_api_key = os.environ['RYR_COLLECTOR_YELP_API_KEY']

    client = CollectorClient('yelp', api_key=client_api_key)
    client.authenticate()
    search_result = client.search_places('221 West North Loop Boulevard, Austin', terms='Epoch Coffee', limit=1)

    print(json.dumps(search_result))


def integration_test_yelp_place_details():
    client_api_key = os.environ['RYR_COLLECTOR_YELP_API_KEY']

    client = CollectorClient('yelp', api_key=client_api_key)
    client.authenticate()
    place_details = client.place_details('krzzyozIVGC7pX1lfVO40w')
    print(json.dumps(place_details))


def integration_test_yelp_retrieve_place_details():
    client_api_key = os.environ['RYR_COLLECTOR_YELP_API_KEY']

    client = CollectorClient('yelp', api_key=client_api_key)
    client.authenticate()
    epoch_search_summary = PlaceSearchSummary(
        'krzzyozIVGC7pX1lfVO40w',
        'Epoch Coffee',
        '221 West North Loop Boulevard, Austin',
    )
    place_details = client.retrieve_place_details(
        epoch_search_summary.id,
        epoch_search_summary.name,
        epoch_search_summary.address,
    )

    print(json.dumps(place_details))


def integration_test_google_search_place():
    """
    Use jq to parse the json output:

        cat google_collector_search_epoch_coffee.json | jq '.results[] | {name: .name, vicinity: .vicinity, place_id: .place_id}'
    """

    places_api_key = os.environ['RYR_COLLECTOR_GOOGLE_PLACES_API_KEY']

    epoch_latlong = (30.3186037, -97.72454019999999)
    gmaps_places = GoogleCollector()
    gmaps_places.authenticate(api_key=places_api_key)
    search_results = gmaps_places.search_places(epoch_latlong)
    print(json.dumps(search_results, indent=2))


def integration_test_google_place_details():
    """
    Use jq to parse the json output:

        cat google_collector_details_epoch_coffee.json | jq '.result | {name: .name, address: .formatted_address, phone: .formatted_phone_number, website: .website}'
    """
    places_api_key = os.environ['RYR_COLLECTOR_GOOGLE_PLACES_API_KEY']
    gmaps_places = GoogleCollector()
    gmaps_places.authenticate(api_key=places_api_key)
    details = gmaps_places.place_details('ChIJG-gJw2vKRIYROWi2uwOp8QE')
    print(json.dumps(details, indent=2))


def integration_test_full_google_yelp_workflow():
    """"""
    places_api_key = os.environ['RYR_COLLECTOR_GOOGLE_PLACES_API_KEY']
    yelp_api_key = os.environ['RYR_COLLECTOR_YELP_API_KEY']

    epoch_latlong = (30.3186037, -97.72454019999999)

    gmaps_places = GoogleCollector()
    gmaps_places.authenticate(api_key=places_api_key)
    s = gmaps_places.search_places(epoch_latlong)

    epoch_search_summary = gmaps_places.retrieve_search_summary(1)

    yelp = CollectorClient('yelp', api_key=yelp_api_key)
    yelp.authenticate()
    place_details = yelp.retrieve_place_details(
        epoch_search_summary.id,
        epoch_search_summary.name,
        epoch_search_summary.address,
    )
    print(json.dumps(place_details))


def integration_test_full_google_yelp_workflow_with_generic():
    """"""
    places_api_key = os.environ['RYR_COLLECTOR_GOOGLE_PLACES_API_KEY']
    yelp_api_key = os.environ['RYR_COLLECTOR_YELP_API_KEY']

    # Simulate a click Epoch Coffee Shop - Northloop on the map.
    epoch_latlong = (30.3186037, -97.72454019999999)

    # Retrieve the places nearby the location clicked on the map.
    gmap = GoogleCollector()
    gmap.authenticate(api_key=places_api_key)
    places_nearby = gmap.search_places_nearby(epoch_latlong)

    # Act like a user chose Epoch Coffee Shop - Northloop in the result list.
    epoch_search_summary = gmap.retrieve_search_summary(1)
    print(epoch_search_summary)

    # Lookup the place on Google Maps.
    google = CollectorClient('google', api_key=places_api_key)
    google.authenticate()
    google_place_details = google.lookup_place(epoch_search_summary.id)
    gb = google.to_business_info()
    print('*** Google:')
    print(gb)

    # Lookup the place on Yelp.
    yelp = CollectorClient('yelp', api_key=yelp_api_key, weight=10)
    yelp.authenticate()
    yelp_place_details = yelp.lookup_place(None, epoch_search_summary.name, epoch_search_summary.address)
    yb = yelp.to_business_info()
    print('*** Yelp:')
    print(yb)

    # Merge the results.
    print('*** Merged:')
    print(gb.merge(yb))


if __name__ == '__main__':
    # integration_test_google_search_place()
    # integration_test_google_place_details()
    # integration_test_yelp_search_place()
    # integration_test_yelp_place_details()
    # integration_test_yelp_retrieve_place_details()
    # integration_test_full_google_yelp_workflow()
    integration_test_full_google_yelp_workflow_with_generic()
