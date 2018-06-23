"""Define all the collectors."""

import abc
import urllib.parse

from dataclasses import dataclass

import googlemaps  # pylint: disable=import-error
import requests


@dataclass
class BusinessInfo:
    """Define the information identifying a business."""

    name: str = ''
    address: str = ''
    latitude: float = 0.0
    longitude: float = 0.0
    type: str = ''
    phone: str = ''
    email: str = ''
    contact_name: str = ''
    website: str = ''
    parking_info: str = ''
    extra_info: str = ''
    weight: int = 0

    def geolocation(self) -> str:
        """Compute the business geolocation."""
        return f'{self.latitude},{self.longitude}'

    def merge(self, other):
        """
        Merge 2 BusinessInfo object together.

        The lightest BusinessInfo object has priority.

        :other: BusinessInfo to merge into this instance.
        :rtype: A BusinessInfo with de data merged by weight, and a new weight of 0.
        """
        merged = BusinessInfo()
        for key in self.__dict__:
            # Ignore the 'weight' property.
            if key == 'weight':
                continue

            # First merge the key of the current instance if it is not empty, else take the key of other.
            merged.__dict__[key] = self.__dict__[key] if self.__dict__[key] else other.__dict__[key]

            # Do not perform any other action if the weights are equal.
            if self.weight == other.weight:
                continue

            # Otherwise the lightest object has the priority.
            if self.weight < other.weight and self.__dict__[key]:
                merged.__dict__[key] = self.__dict__[key]
            elif self.weight > other.weight and other.__dict__[key]:
                merged.__dict__[key] = other.__dict__[key]

        return merged


class AbstractCollector:
    """Define an abstract class for the collectors."""

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """Initialize the collector."""
        self.result = None

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

        This function returns the raw result of the search and caches it in the `self.result` property.

        :param str place_id: the ID of a place
        :rtype: dict
        """
        raise NotImplementedError

    @abc.abstractmethod
    def to_business_info(self):
        """
        Convert the raw data to a BusinessInfo object.

        :rtype: BusinessInfo object
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

        This function returns the raw result of the search and caches it in the `self.result` property.

        :param str place_id: the ID of a place
        :returns: A dictionnary containing the detailed information of the place matching the `place_id`.
        :rtype: dict
        """
        # Prepare the route.
        DETAILS_ROUTE = 'v3/businesses/{id}'.format(id=place_id)
        url = urllib.parse.urljoin(YelpCollector.BASE_URL, DETAILS_ROUTE)

        # Query the server.
        response = requests.get(url, headers=self.headers)
        self.result = response.json()

        # Populate the properties.

        return self.result

    def to_business_info(self):
        """Convert the raw data to a BusinessInfo object."""
        # Ensure we have data to convert.
        if not self.result:
            return None
        if not self.result.get('result'):
            return None

        # Define convenience variables.
        r = self.result.get('result')
        location = r.get('location', {})

        # Populate the business information.
        b = BusinessInfo()
        b.name = r.get('name', '')
        b.address = ' '.join(location.get('display_address', ''))
        b.phone = r.get('display_phone', '')
        return b


class GoogleCollector(AbstractClientCollector):
    """Define the Google Collector."""

    def __init__(self):
        """Initialize the collector."""
        super(GoogleCollector, self).__init__()

        # The Google client.
        self.places_client = None

    def authenticate(self, api_key):
        """Authenticate against Google."""
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
        self.result = self.places_client.place(place_id)
        return self.result

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
        b = BusinessInfo()
        b.name = r.get('name', '')
        b.address = r.get('formatted_address', '')
        b.phone = r.get('formatted_phone_number', '')
        b.website = r.get('website', '')
        b.latitude = location.get('lat', 0.0)
        b.longitude = location.get('lng', 0.0)
        return b


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
            raise ValueError(f'The "{self.provider}" provider is not supported.')

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

        This function retrieves the `name`, `address`, and `phone` properties of the place matching the
        place_id.

        :param str place_id: the ID of a place
        :returns: A dictionnary containing the detailed information of the place matching the `place_id`.
        :rtype: dict
        """
        _ = self.collector.retrieve_place_details(place_id)
        b = self.collector.to_business_info()
        return self.collector.to_business_info().__dict__ if b else {}
