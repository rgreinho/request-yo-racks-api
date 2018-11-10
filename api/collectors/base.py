"""Define the base classes/function for the collectors."""

import abc
from dataclasses import dataclass

import json_tricks as json


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

        :other: BusinessInfo to merge with this instance
        :return: A BusinessInfo with de data merged by weight, and a new weight of 0.
        :rtype: BusinessInfo
        """
        # Do not try to merge objects of different types.
        if not isinstance(other, BusinessInfo):
            return self

        # Merge attribute per attribute.
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

    def to_json(self, indent=2):
        """
        Serialize this instance to JSON.

        :param int indent: Number of spaces to use to indent the JSON representation
        :return: a string representing an instance of this object.
        """
        return json.dumps(self, sort_keys=True, indent=indent)

    @classmethod
    def from_json(cls, json_obj):
        """
        Create an instance of this object from a JSON string.

        :param string json_obj: a JSON string containing the value to create an instance of this object
        :return: a `BusinessInfo` instance.
        """
        return json.loads(json_obj)


@dataclass
class PlaceSearchSummary:
    """Define Place Search Summary information."""

    place_id: str = ''
    name: str = ''
    address: str = ''


class AbstractCollector:
    """Define an abstract class for the collectors."""

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """Initialize the collector."""
        self.search_results = None
        self.result = None
        self.weight = 0

    @abc.abstractmethod
    def authenticate(self, api_key):
        """
        Authenticate against a provider.

        :param str api_key: Collector's API key.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_place_details(self, place_id):
        """
        Retrieve the details of a specific place.

        :param str place_id: the ID of a place
        :return: a dictionary containing the place information.
        :rtype: dict
        """
        raise NotImplementedError

    @abc.abstractmethod
    def search_places(self, address, terms=None, **kwargs):
        """
        Search for businesses using an address and keywords.

        The kwargs arguments are specific to the implementation of the collector.

        :param str address: business address
        :param str terms: search term (e.g. "food", "restaurants") or business names such as "Starbucks"
        :return: A dict representing the places matching the search criteria.
        :rtype: dict
        """
        raise NotImplementedError

    def search_places_nearby(self, location, **kwargs):
        """
        Search places near a specific location.

        The kwargs arguments are specific to the implementation of the collector.

        :param str location: The latitude/longitude value for which you wish to obtain the
            closest, human-readable address. Can be a string, dict, list, or tuple.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def to_business_info(self):
        """
        Convert the raw data to a BusinessInfo object.

        :return: A BusinessInfo object representing this instance.
        :rtype: BusinessInfo object
        """
        raise NotImplementedError


# Pylint does not recognize classes which do not raise NotImplementedError as abstract even though they inherit from
# an abstract class. Ref: https://stackoverflow.com/q/23768767
# pylint: disable=W0223
class AbstractRestCollector(AbstractCollector):
    """Define an abstract class for the REST-based collectors."""

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """Initialize the Abstract REST Collector."""
        super(AbstractRestCollector, self).__init__()

        # Request headers.
        self.headers = {'cache-control': "no-cache"}


# Pylint does not recognize classes which do not raise NotImplementedError as abstract even though they inherit from
# an abstract class. Ref: https://stackoverflow.com/q/23768767
# pylint: disable=W0223
class AbstractClientCollector(AbstractCollector):
    """Define an abstract class for the client-based collectors."""

    __metaclass__ = abc.ABCMeta
