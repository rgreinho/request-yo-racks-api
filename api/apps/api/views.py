"""Define the API views."""
import logging
import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.apps.api.collectors.google import GoogleCollector
from api.celery.tasks import collect_place_details

logger = logging.getLogger(__name__)


class Health(APIView):
    """Health check endpoint."""

    # pylint: disable=redefined-builtin,unused-argument
    def get(self, request):
        """Return the status of the application."""
        content = {'status': 'ok'}
        return Response(content, status=status.HTTP_200_OK)


class PlaceList(APIView):
    """
    View to list all places in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    # authentication_classes = (authentication.TokenAuthentication, )
    # permission_classes = (permissions.IsAdminUser, )

    # pylint: disable=redefined-builtin,unused-argument
    def get(self, request, latlong, format=None):
        """Return a list of all places nearby our coordinates."""
        # Define data.
        places_api_key = os.environ['RYR_COLLECTOR_GOOGLE_PLACES_API_KEY']

        # Prepare client.
        gmap = GoogleCollector()
        gmap.authenticate(api_key=places_api_key)

        # Retrieve nearby places.
        places_nearby = gmap.search_places_nearby(latlong)
        return Response(places_nearby)


class PlaceDetails(APIView):
    """View to provide detailed information about a specific place."""

    # pylint: disable=redefined-builtin,unused-argument
    def get(self, request, pid, format=None):
        """Return the detailed information about a specific place."""
        place_id, name, address = pid.split(',')
        result = collect_place_details(place_id, name, address)
        return Response(result.get())
