"""Define the endpoint for the places resource."""
import os

from connexion.lifecycle import ConnexionResponse

from api.collectors.google import GoogleCollector


def search(location):
    """Return a list of all places nearby our coordinates."""
    # Define data.
    places_api_key = os.environ['RYR_COLLECTOR_GOOGLE_PLACES_API_KEY']

    # Prepare client.
    gmap = GoogleCollector()
    gmap.authenticate(api_key=places_api_key)

    # Retrieve nearby places.
    places_nearby = gmap.search_places_nearby(location)
    return ConnexionResponse(body=places_nearby)
