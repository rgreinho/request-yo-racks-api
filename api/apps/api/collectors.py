"""Define all the collectors."""

import abc
import urllib.parse

import googlemaps  # pylint: disable=import-error
import requests


class AbstractCollector:
    """Define an abstract class for the collectors."""

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """Initialize the collector."""
        # Business properties.
        self.name = ''
        self.address = ''
        self.phone = ''

    @property
    def business_name(self):
        """Return the business name."""
        return self.name or ''

    @property
    def business_address(self):
        """Return the business address."""
        return self.address or ''

    @property
    def business_phone_number(self):
        """Return the phone number."""
        return self.phone or ''

    @abc.abstractmethod
    def search_place(self, address, terms=None):
        """
        Search for a business based on the provided search criteria.

        :param str address: business address
        :param str terms: Optional. Search term (e.g. "food", "restaurants"). If term isn’t included we
            search everything. The term keyword also accepts business names such as "Starbucks".
        :returns: The ID of the first match.
        :rtype: str
        """
        raise NotImplementedError

    @abc.abstractmethod
    def retrieve_place_details(self, place_id):
        """
        Retrieve the details of a place.

        This function populates the `name`, `address`, and `phone` properties of this instance.

        :param str place_id: the ID of a place
        """
        raise NotImplementedError


class AbstractRestCollector(AbstractCollector):
    """Define an abstract class for the REST-based collectors."""

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """Initialize the Abstract REST Collector."""
        super(AbstractRestCollector, self).__init__()

        # Request headers.
        self.headers = {'cache-control': "no-cache"}

    @abc.abstractmethod
    def authenticate(self, client_id, client_secret):
        """Authenticate against a provider."""
        raise NotImplementedError


class AbstractClientCollector(AbstractCollector):
    """Define an abstract class for the client-based collectors."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def authenticate(self, api_key):
        """Authenticate against a provider."""
        raise NotImplementedError


class YelpCollector(AbstractRestCollector):
    """Define the Yelp Collector."""

    BASE_URL = "https://api.yelp.com/"

    def authenticate(self, client_id, client_secret):
        """
        Authenticate against Yelp.

        :param str client_id: client id for the Yelp app
        :param str client_secret: client secret for the Yelp app
        """
        # Prepare the route.
        AUTHENTICATION_ROUTE = "oauth2/token"
        url = urllib.parse.urljoin(YelpCollector.BASE_URL, AUTHENTICATION_ROUTE)

        # Prepare the headers.
        headers = {'cache-control': "no-cache", 'content-type': "application/x-www-form-urlencoded"}

        # Prepare the payload.
        payload = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials',
        }

        # Query the server.
        response = requests.request("POST", url, data=payload, headers=headers)
        response_json = response.json()

        # Extract the token from the response.
        authentication_token = response_json['access_token']

        # Prepare the header for the future requests.
        self.headers['authorization'] = "Bearer " + authentication_token

    def search_place(self, address, terms=None):
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
            querystring['terms'] = terms

        # Query the server.
        response = requests.get(url, headers=self.headers, params=querystring)
        response_json = response.json()

        return response_json

    def retrieve_place_details(self, place_id):
        """
        Retrieve the details of a place.

        This function populates the `name`, `address`, and `phone` properties of this instance.

        :param str place_id: the ID of a place
        :returns: A dictionnary containing the detailed information of the place matching the `place_id`.
        :rtype: dict
        """
        # Prepare the route.
        DETAILS_ROUTE = 'v3/businesses/{id}'.format(id=place_id)
        url = urllib.parse.urljoin(YelpCollector.BASE_URL, DETAILS_ROUTE)

        # Query the server.
        response = requests.get(url, headers=self.headers)
        response_json = response.json()

        # Populate the properties.
        self.name = response_json.get('name', '')
        self.address = ' '.join(response_json.get('location', {}).get('display_address', ''))
        self.phone = response_json.get('display_phone', '')

        return response_json


class GoogleCollector(AbstractClientCollector):
    """Define the Google Collector."""

    def __init__(self):
        """Initialize the collector."""
        super(GoogleCollector, self).__init__()

        # The Google client.
        self.places_client = None

    def authenticate(self, api_key):
        """Authenticate against Yelp."""
        # Search Business.
        self.places_client = googlemaps.Client(key=api_key)

    def search_place(self, address, terms=None):
        """
        Search for a business based on the provided search criteria.

        :param str address: business address
        :param str terms: Optional. Search term (e.g. "food", "restaurants"). If term isn’t included we
            search everything. The term keyword also accepts business names such as "Starbucks".
        :returns: A dictionnary containing the results of the research.
        :rtype: dict
        """
        results = self.places_client.places_nearby(address, radius=50)
        return results

    def retrieve_place_details(self, place_id):
        """
        Retrieve the details of a place.

        This function populates the `name`, `address`, and `phone` properties of this instance.

        :param str place_id: the ID of a place
        :returns: A dictionnary containing the detailed information of the place matching the `place_id`.
        :rtype: dict
        """
        result = self.places_client.place(place_id)

        # Populate the properties.
        self.name = result.get('result', {}).get('name', '')
        self.address = result.get('result', {}).get('formatted_address', '')
        self.phone = result.get('result', {}).get('phone', '')

        return result


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

    def __init__(self, provider, oauth2=None, api_key=None):
        """Initialize the client."""
        # Authentication properties.
        self.provider = provider
        self.oauth2 = oauth2
        self.api_key = api_key

        # Collector.
        self.collector = None

    def authenticate(self):
        """Authenticate."""
        # Create collector.
        if self.provider.lower() == 'yelp':
            self.collector = YelpCollector()
            self.collector.authenticate(self.oauth2[0], self.oauth2[1])
        elif self.provider.lower() == 'google':
            self.collector = GoogleCollector()
            self.collector.authenticate(self.api_key)
        else:
            raise ValueError('The "{}" provider is not supported.'.format(self.provider))

    def search_place(self, address, terms=None):
        """
        Search for a business based on the provided search criteria.

        :param str address: business address
        :param str terms: Optional. Search term (e.g. "food", "restaurants"). If term isn’t included we
            search everything. The term keyword also accepts business names such as "Starbucks".
        :returns: A dictionnary containing the results of the research.
        :rtype: dict
        """
        return self.collector.search_place(address, terms=terms)

    def retrieve_details(self, place_id):
        """
        Retrieve the details of a place.

        This function retrievesd the `name`, `address`, and `phone` properties of the place matching the
        place_id.

        :param str place_id: the ID of a place
        :returns: A dictionnary containing the detailed information of the place matching the `place_id`.
        :rtype: dict
        """
        details = self.collector.retrieve_place_details(place_id)
        return details

    def retrieve_place_details(self, address, terms=None):
        """Retrieve the details of a place.

        :param str address: business address
        :param str terms: Optional. Search term (e.g. "food", "restaurants"). If term isn’t included we
            search everything. The term keyword also accepts business names such as "Starbucks".

        """
        place_id = self.search_place(address, terms=terms)
        return self.retrieve_details(place_id)
