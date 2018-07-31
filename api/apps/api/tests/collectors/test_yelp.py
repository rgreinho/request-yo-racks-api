"""Test the yelp module."""

import json

from faker import Faker
import requests
import pytest

from api.apps.api.collectors.base import BusinessInfo
from api.apps.api.collectors.base import PlaceSearchSummary
from api.apps.api.collectors.yelp import YelpCollector


class TestYelpCollector():
    """Implement tests for the Yelp collector."""
    fake = Faker()

    def test_search_places_00(self, mocker):
        """Ensure the search returns a dictionary."""
        yelp = YelpCollector()

        mocker.patch.object(requests.Response, 'json', return_value=YELP_SEARCH_RESPONSE)
        search_results = yelp.search_places(self.fake.address(), terms=self.fake.pystr())

        assert type(search_results) is dict

    def test_search_places_01(self, mocker):
        """Ensure the search returns a dictionary."""
        yelp = YelpCollector()

        mocker.patch.object(requests.Response, 'json', return_value=YELP_SEARCH_RESPONSE)
        search_results = yelp.search_places(self.fake.address(), terms=self.fake.pystr(), limit=self.fake.pyint())

        assert type(search_results) is dict

    def test_retrieve_place_details_00(self, mocker):
        """Ensure retrieve_place_details returns a dictionary."""
        yelp = YelpCollector()

        mocker.patch.object(requests.Response, 'json', return_value=YELP_DETAILS_RESPONSE)
        details_results = yelp.get_place_details(self.fake.pystr())

        assert type(details_results) is dict

    def test_retrieve_place_details_01(self, mocker):
        """Ensure retrieve_place_details returns a dictionary."""
        yelp = YelpCollector()

        mocker.patch.object(requests.Response, 'json', return_value=YELP_DETAILS_RESPONSE)
        _ = yelp.get_place_details(self.fake.pystr())
        actual = yelp.to_business_info()
        expected = BusinessInfo(
            name='Gary Danko',
            address='800 N Point St San Francisco, CA 94109',
            latitude=37.80587,
            longitude=-122.42058,
            type='American (New)',
            phone='+14152520800',
            email='',
            contact_name='',
            website='',
            parking_info='',
            extra_info='',
            weight=0)

        assert actual == expected

    def test_search_places_nearby_00(self):
        """Ensure the search_nearby fucntion raise `NotImplementedError`."""
        yelp = YelpCollector()
        with pytest.raises(NotImplementedError):
            yelp.search_places_nearby('123.456,789.012')

    def test_to_business_info_00(self):
        """Ensure empty search results return `None`."""
        yelp = YelpCollector()

        actual = yelp.to_business_info()
        expected = None

        assert actual == expected

    def test_retrieve_search_summary_00(self):
        """Ensure empty search results return `None`."""
        yelp = YelpCollector()

        actual = yelp.retrieve_search_summary()
        expected = None

        assert actual == expected

    def test_retrieve_search_summary_01(self):
        """Ensure empty search results return `None`."""
        yelp = YelpCollector()
        yelp.search_results = {'fake_key': 'fake_value'}

        actual = yelp.retrieve_search_summary()
        expected = None

        assert actual == expected

    def test_retrieve_search_summary_02(self):
        """Ensure the first result of the search is returned as a `PlaceSearchSummary`."""
        yelp = YelpCollector()
        yelp.search_results = YELP_SEARCH_RESPONSE
        actual = yelp.retrieve_search_summary()
        expected = PlaceSearchSummary(
            id='four-barrel-coffee-san-francisco',
            name='Four Barrel Coffee',
            address='',
        )

        assert actual == expected


# Yelp Search API Response example.
YELP_SEARCH_RESPONSE_JSON = """
{
  "total": 8228,
  "businesses": [
    {
      "rating": 4,
      "price": "$",
      "phone": "+14152520800",
      "id": "four-barrel-coffee-san-francisco",
      "is_closed": false,
      "categories": [
        {
          "alias": "coffee",
          "title": "Coffee & Tea"
        }
      ],
      "review_count": 1738,
      "name": "Four Barrel Coffee",
      "url": "https://www.yelp.com/biz/four-barrel-coffee-san-francisco",
      "coordinates": {
        "latitude": 37.7670169511878,
        "longitude": -122.42184275
      },
      "image_url": "http://s3-media2.fl.yelpcdn.com/bphoto/MmgtASP3l_t4tPCL1iAsCg/o.jpg",
      "location": {
        "city": "San Francisco",
        "country": "US",
        "address2": "",
        "address3": "",
        "state": "CA",
        "address1": "375 Valencia St",
        "zip_code": "94103"
      },
      "distance": 1604.23,
      "transactions": ["pickup", "delivery"]
    }
  ],
  "region": {
    "center": {
      "latitude": 37.767413217936834,
      "longitude": -122.42820739746094
    }
  }
}
"""
YELP_SEARCH_RESPONSE = json.loads(YELP_SEARCH_RESPONSE_JSON)

# Yelp Business API Response example.
YELP_DETAILS_RESPONSE_JSON = """
{
  "id": "gary-danko-san-francisco",
  "name": "Gary Danko",
  "image_url": "https://s3-media4.fl.yelpcdn.com/bphoto/--8oiPVp0AsjoWHqaY1rDQ/o.jpg",
  "is_claimed": false,
  "is_closed": false,
  "url": "https://www.yelp.com/biz/gary-danko-san-francisco",
  "price": "$$$$",
  "rating": 4.5,
  "review_count": 4521,
  "phone": "+14152520800",
  "photos": [
    "http://s3-media3.fl.yelpcdn.com/bphoto/--8oiPVp0AsjoWHqaY1rDQ/o.jpg",
    "http://s3-media2.fl.yelpcdn.com/bphoto/ybXbObsm7QGw3SGPA1_WXA/o.jpg",
    "http://s3-media3.fl.yelpcdn.com/bphoto/7rZ061Wm4tRZ-iwAhkRSFA/o.jpg"
  ],
  "hours": [
    {
      "hours_type": "REGULAR",
      "open": [
        {
          "is_overnight": false,
          "end": "2200",
          "day": 0,
          "start": "1730"
        },
        {
          "is_overnight": false,
          "end": "2200",
          "day": 1,
          "start": "1730"
        },
        {
          "is_overnight": false,
          "end": "2200",
          "day": 2,
          "start": "1730"
        },
        {
          "is_overnight": false,
          "end": "2200",
          "day": 3,
          "start": "1730"
        },
        {
          "is_overnight": false,
          "end": "2200",
          "day": 4,
          "start": "1730"
        },
        {
          "is_overnight": false,
          "end": "2200",
          "day": 5,
          "start": "1730"
        },
        {
          "is_overnight": false,
          "end": "2200",
          "day": 6,
          "start": "1730"
        }
      ],
      "is_open_now": false
    }
  ],
  "categories": [
    {
      "alias": "newamerican",
      "title": "American (New)"
    }
  ],
  "coordinates": {
    "latitude": 37.80587,
    "longitude": -122.42058
  },

  "location": {
    "address1": "800 N Point St",
    "address2": "",
    "address3": "",
    "city": "San Francisco",
    "state": "CA",
    "zip_code": "94109",
    "country": "US",
    "display_address": [
      "800 N Point St",
      "San Francisco, CA 94109"
    ],
    "cross_streets": "Hyde St & Larkin St"
  },
  "transactions": ["restaurant_reservation"]
}
"""
YELP_DETAILS_RESPONSE = json.loads(YELP_DETAILS_RESPONSE_JSON)
