"""Define the Yelp Collector."""
import urllib.parse

import requests

from api.collectors.base import AbstractRestCollector
from api.collectors.base import BusinessInfo
from api.collectors.base import PlaceSearchSummary


class YelpCollector(AbstractRestCollector):
    """Define the Yelp Collector."""

    BASE_URL = "https://api.yelp.com/"

    def authenticate(self, api_key):
        """
        Authenticate against Yelp.

        Since Yelp uses only an API key to authenticate the requests (starting March 1, 2018), this function simply
        generates the correct headers.

        :param str api_key: Yelp API key
        """
        # Prepare the header for the future requests.
        self.headers['Authorization'] = f'Bearer {api_key}'

    def get_place_details(self, place_id):
        """
        Retrieve the details of a place.

        This function returns the raw result of the search and caches it in the `self.result` property.

        :param str place_id: the ID of a place
        :returns: A dictionnary containing the detailed information of the place matching the `place_id`.
        :rtype: dict
        """
        # Prepare the route.
        DETAILS_ROUTE = f'v3/businesses/{place_id}'
        url = urllib.parse.urljoin(YelpCollector.BASE_URL, DETAILS_ROUTE)

        # Query the server.
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            response.raise_for_status()
        self.result = response.json()

        return self.result

    def search_places(self, address, terms=None, **kwargs):
        """
        Search for a business based on the provided search criteria.

        :param str address: business address
        :param str terms: Optional. Search term (e.g. "food", "restaurants"). If term isn’t included we
            search everything. The term keyword also accepts business names such as "Starbucks".
        :returns: A dictionnary containing the results of the research.
        :rtype: dict
        """
        # Prepare the route.
        SEARCH_ROUTE = 'v3/businesses/search'
        url = urllib.parse.urljoin(YelpCollector.BASE_URL, SEARCH_ROUTE)

        # Prepare the quesrystring.
        querystring = {'location': address}
        if terms:
            sanitized_terms = terms.split(' - ')[0]
            querystring['term'] = sanitized_terms
        if kwargs.get('limit'):
            querystring['limit'] = kwargs.get('limit')

        # Query the server.
        response = requests.get(url, headers=self.headers, params=querystring)
        self.search_results = response.json()

        return self.search_results

    def search_places_nearby(self, location, **kwargs):
        """
        Search places nearby.

        This collector does not support this search method.
        """
        raise NotImplementedError

    def to_business_info(self):
        """Convert the raw data to a BusinessInfo object."""
        # Ensure we have data to convert.
        if not self.result:
            return None

        # Define convenience variables.
        r = self.result
        location = r.get('location', {})
        coordinates = r.get('coordinates', {})

        # Populate the business information.
        b = BusinessInfo(weight=self.weight)
        b.name = r.get('name', '')
        b.address = ' '.join(location.get('display_address', ''))
        b.phone = r.get('phone', '')
        b.latitude = coordinates.get('latitude', 0.0)
        b.longitude = coordinates.get('longitude', 0.0)
        b.type = ', '.join([d['title'] for d in r['categories']])
        return b

    def retrieve_search_summary(self, index=0):
        """Retrieve the ID of a specific place."""
        if not self.search_results:
            return None
        if not self.search_results.get('businesses'):
            return None

        search_summary = PlaceSearchSummary()
        business = self.search_results.get('businesses')[index]

        search_summary.place_id = business.get('id', '')
        search_summary.name = business.get('name', '')
        search_summary.address = ' '.join(business.get('location', {}).get('display_address', ''))

        return search_summary
