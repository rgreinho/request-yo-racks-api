"""Defines a generic client for the collectors."""

from api.apps.api.collectors.google import GoogleCollector
from api.apps.api.collectors.yelp import YelpCollector


class CollectorClient:
    """
    Defines a generic client for the collectors.

    :param str provider: name of the provider to use

        The following providers are supported:
            * yelp
            * google

    :param tuple(str,str) oauth2: tuple containing 2 strings:
        0. the client id
        1. the client secret

    :param str api_key: API key

    If a client can take several types of authentication parameters, they are used in the following order.
        1. OAuth2
        2. API key

    Once one is found, the rest is ignored.
    """

    def __init__(self, provider, oauth2=None, api_key=None, weight=0):
        """Initialize the client."""
        # Authentication properties.
        self.provider = provider
        self.oauth2 = oauth2
        self.api_key = api_key

        # Collector.
        self.collector = None
        self.weight = weight

    def authenticate(self):
        """Authenticate."""
        # Create collector.
        if self.provider.lower() == 'yelp':
            self.collector = YelpCollector()
            self.collector.authenticate(self.api_key)
        elif self.provider.lower() == 'google':
            self.collector = GoogleCollector()
            self.collector.authenticate(self.api_key)
        else:
            raise ValueError(f'The "{self.provider}" provider is not supported.')

        self.collector.weight = self.weight

    def get_place_details(self, place_id):
        """
        Retrieve the details of a place.

        :param str place_id: the ID of a place
        :returns: A dictionnary containing the detailed information of the place matching the `place_id`.
        :rtype: dict
        """
        self.collector.get_place_details(place_id)
        b = self.collector.to_business_info()
        return b

    def retrieve_search_summary(self, index=0):
        """
        Retrieve the search information (ID, name and address) of a specific place.

        :param int index: position of the place to look for in the results.
        :return: the summary information of a specific place.
        :rtype: PlaceSearchSummary
        """
        return self.collector.retrieve_search_summary(index)

    def search_places(self, address, terms=None, **kwargs):
        """
        Search for a business based on the provided search criteria.

        The kwargs arguments are specific to the implementation of the collector.

        :param str address: business address
        :param str terms: search term (e.g. "food", "restaurants") or business names such as "Starbucks"
        :return: A dict representing the places matching the search criteria.
        :rtype: dict
        """
        return self.collector.search_places(address, terms=terms, **kwargs)

    def lookup_place(self, place_id=None, name=None, address=None):
        """
        Look up for a place.

        :param str place_id: ID of the place to look for. Dependent of the collector used to perform the lookup.
        :param str name: name of the place
        :param str address: adress of the place
        :return: A dictionary containing the business information.
        :rtype: dict
        """
        if not place_id:
            if not (name and address):
                raise ValueError('A name and a address must be provided.')
            self.search_places(
                address=address,
                terms=name,
                limit=1,
            )
            search_summary = self.retrieve_search_summary(0)
            lookup_id = search_summary.id
        else:
            lookup_id = place_id
        place_details = self.get_place_details(lookup_id)
        return place_details

    def to_business_info(self):
        """
        Convert the raw data to a BusinessInfo object.

        :rtype: BusinessInfo object
        """
        return self.collector.to_business_info()
