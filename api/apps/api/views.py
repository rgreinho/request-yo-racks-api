"""Define the API views."""
import os

from rest_framework.response import Response
from rest_framework.views import APIView

from api.apps.api.collectors import CollectorClient


class PlaceList(APIView):
    """
    View to list all places in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    # authentication_classes = (authentication.TokenAuthentication, )
    # permission_classes = (permissions.IsAdminUser, )

    def get(self):
        """Return a list of all places nearby our coordinates."""
        # Define data.
        places_api_key = os.environ['RYR_COLLECTOR_GOOGLE_PLACES_API_KEY']
        epoch_latlong = (30.3186037, -97.72454019999999)

        # Prepare client.
        client = CollectorClient('google', api_key=places_api_key)
        client.authenticate()

        # Retrieve search results.
        search_results = client.search_place(epoch_latlong)
        return Response(search_results)


class PlaceDetails(APIView):
    """View to provide detailed information about a specific place."""

    def get(self, pid):
        """Return the detailed information about a specific place."""
        # Define data.
        places_api_key = os.environ['RYR_COLLECTOR_GOOGLE_PLACES_API_KEY']

        # Prepare client.
        client = CollectorClient('google', api_key=places_api_key)
        client.authenticate()

        # Retrieve detailed results.
        details = client.retrieve_details(pid)
        return Response(details)
