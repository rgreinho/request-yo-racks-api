"""Define the Google Collector."""

import googlemaps

from api.collectors.base import AbstractClientCollector
from api.collectors.base import BusinessInfo
from api.collectors.base import PlaceSearchSummary


class GoogleCollector(AbstractClientCollector):
    """Define the Google Collector."""

    def __init__(self):
        """Initialize the collector."""
        super(GoogleCollector, self).__init__()

        # The Google client.
        self.gmaps = None

    def authenticate(self, api_key):
        """Authenticate against Google."""
        self.gmaps = googlemaps.Client(key=api_key)

    def get_place_details(self, place_id):
        """
        Retrieve the details of a specific place.

        :param str place_id: the ID of a place
        :return: a dictionary containing the place information.
        :rtype: dict
        """
        self.result = self.gmaps.place(place_id)
        return self.result

    def search_places(self, address, terms=None, **kwargs):
        """
        Search for a business based on the provided search criteria.

        No kwargs are used in this implementation.

        :param str address: business address
        :param str terms: search term (e.g. "food", "restaurants") or business names such as "Starbucks"
        :return: A dict representing the places matching the search criteria.
        :rtype: dict
        """
        self.search_results = self.gmaps.find_place(f'{address} {terms}', 'textquery')
        return self.search_results

    def search_places_nearby(self, location, **kwargs):
        """
        Search places near a specific location.

        :param str location: The latitude/longitude value for which you wish to obtain the
            closest, human-readable address. Can be a string, dict, list, or tuple.
        """
        radius = kwargs.get('radius', 250)
        self.search_results = self.gmaps.places_nearby(location=location, radius=radius, **kwargs)
        return self.search_results

    def to_business_info(self):
        """Convert the raw data to a BusinessInfo object."""
        # Ensure we have data to convert.
        if not self.result:
            return None
        if not self.result.get('result'):
            return None

        # Define convenience variables.
        r = self.result.get('result')
        location = r.get('geometry', {}).get('location', {})

        # Populate the business information.
        b = BusinessInfo(weight=self.weight)
        b.name = r.get('name', '')
        b.address = r.get('formatted_address', '')
        b.phone = r.get('formatted_phone_number', '')
        b.website = r.get('website', '')
        b.latitude = location.get('lat', 0.0)
        b.longitude = location.get('lng', 0.0)
        return b

    def retrieve_search_summary(self, index=0):
        """
        Retrieve the search information (ID, name and address) of a specific place.

        :param int index: position of the place to look for in the results.
        :return: the summary information of a specific place.
        :rtype: PlaceSearchSummary
        """
        if not self.search_results:
            return None
        if not self.search_results.get('results'):
            return None
        search_summary = PlaceSearchSummary()
        business = self.search_results.get('results')[index]

        search_summary.place_id = business.get('place_id', '')
        search_summary.name = business.get('name', '')
        search_summary.address = business.get('vicinity', '')

        return search_summary
