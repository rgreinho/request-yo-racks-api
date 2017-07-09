import json

import googlemaps
from faker import Faker
import pytest
import requests

from api.apps.api.collectors.collector import CollectorClient
from api.apps.api.collectors.collector import GoogleCollector
from api.apps.api.collectors.collector import YelpCollector


@pytest.fixture()
def google_collector():
    """
    Returns a GoogleCollector.

    A valid API key for the Google Maps client starts with "AIza".
    """
    c = GoogleCollector()
    c.authenticate('AIzaasdf')
    return c


class TestCollectorClient():
    """Tests for the generic collector client."""
    fake = Faker()

    def test_authenticate_00(self):
        """Ensure an invalid provider raises an error."""
        c = CollectorClient(self.fake.pystr())
        with pytest.raises(ValueError):
            c.authenticate()
        assert True

    def test_retrieve_details_00(self, mocker):
        """Ensure an ID is returned."""
        c = CollectorClient(self.fake.pystr())

        # Prepare the expected returned value.
        details = {
            'name': self.fake.company(),
            'address': self.fake.address(),
            'phone': self.fake.phone_number(),
        }

        # Mock the retrieve_details function.
        mock_retrieve_details = mocker.patch.object(CollectorClient, 'retrieve_details', return_value=details)

        assert c.retrieve_details() == details


class TestGoogleCollector():
    """Tests for the Google collector."""
    fake = Faker()

    def test_search_places_00(self, mocker, google_collector):
        """Ensure the search returns a dictionary."""
        gmaps_places = google_collector

        mocker.patch.object(googlemaps.Client, 'places_nearby', return_value=GOOGLE_MAPS_SEARCH_RESPONSE)
        search_results = gmaps_places.search_place(self.fake.address(), terms=self.fake.pyint())

        assert type(search_results) is dict

    def test_retrieve_place_details_00(self, mocker, google_collector):
        """Ensure retrieve_place_details returns a dictionary."""
        gmaps_places = google_collector

        mocker.patch.object(googlemaps.Client, 'place', return_value=GOOGLE_MAPS_DETAILS_RESPONSE)
        details_results = gmaps_places.retrieve_place_details(self.fake.pystr())

        assert type(details_results) is dict


class TestYelpCollector():
    """Tests for the Yelp collector."""
    fake = Faker()

    def test_search_places_00(self, mocker):
        """Ensure the search returns a dictionary."""
        yelp = YelpCollector()

        mocker.patch.object(requests.Response, 'json', return_value=YELP_SEARCH_RESPONSE)
        search_results = yelp.search_place(self.fake.address(), terms=self.fake.pyint())

        assert type(search_results) is dict

    def test_retrieve_place_details_00(self, mocker):
        """Ensure retrieve_place_details returns a dictionary."""
        yelp = YelpCollector()

        mocker.patch.object(requests.Response, 'json', return_value=YELP_DETAILS_RESPONSE_JSON)
        details_results = yelp.retrieve_place_details(self.fake.pystr())

        assert type(details_results) is dict


GOOGLE_MAPS_SEARCH_RESPONSE_JSON = """
{
   "html_attributions" : [],
   "results" : [
      {
         "geometry" : {
            "location" : {
               "lat" : -33.870775,
               "lng" : 151.199025
            }
         },
         "icon" : "http://maps.gstatic.com/mapfiles/place_api/icons/travel_agent-71.png",
         "id" : "21a0b251c9b8392186142c798263e289fe45b4aa",
         "name" : "Rhythmboat Cruises",
         "opening_hours" : {
            "open_now" : true
         },
         "photos" : [
            {
               "height" : 270,
               "html_attributions" : [],
               "photo_reference" : "CnRnAAAAF-LjFR1ZV93eawe1cU_3QNMCNmaGkowY7CnOf-kcNmPhNnPEG9W979jOuJJ1sGr75rhD5hqKzjD8vbMbSsRnq_Ni3ZIGfY6hKWmsOf3qHKJInkm4h55lzvLAXJVc-Rr4kI9O1tmIblblUpg2oqoq8RIQRMQJhFsTr5s9haxQ07EQHxoUO0ICubVFGYfJiMUPor1GnIWb5i8",
               "width" : 519
            }
         ],
         "place_id" : "ChIJyWEHuEmuEmsRm9hTkapTCrk",
         "scope" : "GOOGLE",
         "alt_ids" : [
            {
               "place_id" : "D9iJyWEHuEmuEmsRm9hTkapTCrk",
               "scope" : "APP"
            }
         ],
         "reference" : "CoQBdQAAAFSiijw5-cAV68xdf2O18pKIZ0seJh03u9h9wk_lEdG-cP1dWvp_QGS4SNCBMk_fB06YRsfMrNkINtPez22p5lRIlj5ty_HmcNwcl6GZXbD2RdXsVfLYlQwnZQcnu7ihkjZp_2gk1-fWXql3GQ8-1BEGwgCxG-eaSnIJIBPuIpihEhAY1WYdxPvOWsPnb2-nGb6QGhTipN0lgaLpQTnkcMeAIEvCsSa0Ww",
         "types" : [ "travel_agency", "restaurant", "food", "establishment" ],
         "vicinity" : "Pyrmont Bay Wharf Darling Dr, Sydney"
      },
      {
         "geometry" : {
            "location" : {
               "lat" : -33.866891,
               "lng" : 151.200814
            }
         },
         "icon" : "http://maps.gstatic.com/mapfiles/place_api/icons/restaurant-71.png",
         "id" : "45a27fd8d56c56dc62afc9b49e1d850440d5c403",
         "name" : "Private Charter Sydney Habour Cruise",
         "photos" : [
            {
               "height" : 426,
               "html_attributions" : [],
               "photo_reference" : "CnRnAAAAL3n0Zu3U6fseyPl8URGKD49aGB2Wka7CKDZfamoGX2ZTLMBYgTUshjr-MXc0_O2BbvlUAZWtQTBHUVZ-5Sxb1-P-VX2Fx0sZF87q-9vUt19VDwQQmAX_mjQe7UWmU5lJGCOXSgxp2fu1b5VR_PF31RIQTKZLfqm8TA1eynnN4M1XShoU8adzJCcOWK0er14h8SqOIDZctvU",
               "width" : 640
            }
         ],
         "place_id" : "ChIJqwS6fjiuEmsRJAMiOY9MSms",
         "scope" : "GOOGLE",
         "reference" : "CpQBhgAAAFN27qR_t5oSDKPUzjQIeQa3lrRpFTm5alW3ZYbMFm8k10ETbISfK9S1nwcJVfrP-bjra7NSPuhaRulxoonSPQklDyB-xGvcJncq6qDXIUQ3hlI-bx4AxYckAOX74LkupHq7bcaREgrSBE-U6GbA1C3U7I-HnweO4IPtztSEcgW09y03v1hgHzL8xSDElmkQtRIQzLbyBfj3e0FhJzABXjM2QBoUE2EnL-DzWrzpgmMEulUBLGrtu2Y",
         "types" : [ "restaurant", "food", "establishment" ],
         "vicinity" : "Australia"
      },
      {
         "geometry" : {
            "location" : {
               "lat" : -33.870943,
               "lng" : 151.190311
            }
         },
         "icon" : "http://maps.gstatic.com/mapfiles/place_api/icons/restaurant-71.png",
         "id" : "30bee58f819b6c47bd24151802f25ecf11df8943",
         "name" : "Bucks Party Cruise",
         "opening_hours" : {
            "open_now" : true
         },
         "photos" : [
            {
               "height" : 600,
               "html_attributions" : [],
               "photo_reference" : "CnRnAAAA48AX5MsHIMiuipON_Lgh97hPiYDFkxx_vnaZQMOcvcQwYN92o33t5RwjRpOue5R47AjfMltntoz71hto40zqo7vFyxhDuuqhAChKGRQ5mdO5jv5CKWlzi182PICiOb37PiBtiFt7lSLe1SedoyrD-xIQD8xqSOaejWejYHCN4Ye2XBoUT3q2IXJQpMkmffJiBNftv8QSwF4",
               "width" : 800
            }
         ],
         "place_id" : "ChIJLfySpTOuEmsRsc_JfJtljdc",
         "scope" : "GOOGLE",
         "reference" : "CoQBdQAAANQSThnTekt-UokiTiX3oUFT6YDfdQJIG0ljlQnkLfWefcKmjxax0xmUpWjmpWdOsScl9zSyBNImmrTO9AE9DnWTdQ2hY7n-OOU4UgCfX7U0TE1Vf7jyODRISbK-u86TBJij0b2i7oUWq2bGr0cQSj8CV97U5q8SJR3AFDYi3ogqEhCMXjNLR1k8fiXTkG2BxGJmGhTqwE8C4grdjvJ0w5UsAVoOH7v8HQ",
         "types" : [ "restaurant", "food", "establishment" ],
         "vicinity" : "37 Bank St, Pyrmont"
      },
      {
         "geometry" : {
            "location" : {
               "lat" : -33.867591,
               "lng" : 151.201196
            }
         },
         "icon" : "http://maps.gstatic.com/mapfiles/place_api/icons/travel_agent-71.png",
         "id" : "a97f9fb468bcd26b68a23072a55af82d4b325e0d",
         "name" : "Australian Cruise Group",
         "opening_hours" : {
            "open_now" : true
         },
         "photos" : [
            {
               "height" : 242,
               "html_attributions" : [],
               "photo_reference" : "CnRnAAAABjeoPQ7NUU3pDitV4Vs0BgP1FLhf_iCgStUZUr4ZuNqQnc5k43jbvjKC2hTGM8SrmdJYyOyxRO3D2yutoJwVC4Vp_dzckkjG35L6LfMm5sjrOr6uyOtr2PNCp1xQylx6vhdcpW8yZjBZCvVsjNajLBIQ-z4ttAMIc8EjEZV7LsoFgRoU6OrqxvKCnkJGb9F16W57iIV4LuM",
               "width" : 200
            }
         ],
         "place_id" : "ChIJrTLr-GyuEmsRBfy61i59si0",
         "scope" : "GOOGLE",
         "reference" : "CoQBeQAAAFvf12y8veSQMdIMmAXQmus1zqkgKQ-O2KEX0Kr47rIRTy6HNsyosVl0CjvEBulIu_cujrSOgICdcxNioFDHtAxXBhqeR-8xXtm52Bp0lVwnO3LzLFY3jeo8WrsyIwNE1kQlGuWA4xklpOknHJuRXSQJVheRlYijOHSgsBQ35mOcEhC5IpbpqCMe82yR136087wZGhSziPEbooYkHLn9e5njOTuBprcfVw",
         "types" : [ "travel_agency", "restaurant", "food", "establishment" ],
         "vicinity" : "32 The Promenade, King Street Wharf 5, Sydney"
      }
   ],
   "status" : "OK"
}
"""
GOOGLE_MAPS_SEARCH_RESPONSE = json.loads(GOOGLE_MAPS_SEARCH_RESPONSE_JSON)

GOOGLE_MAPS_DETAILS_RESPONSE_JSON = """
{
   "html_attributions" : [],
   "result" : {
      "address_components" : [
         {
            "long_name" : "5",
            "short_name" : "5",
            "types" : [ "floor" ]
         },
         {
            "long_name" : "48",
            "short_name" : "48",
            "types" : [ "street_number" ]
         },
         {
            "long_name" : "Pirrama Road",
            "short_name" : "Pirrama Rd",
            "types" : [ "route" ]
         },
         {
            "long_name" : "Pyrmont",
            "short_name" : "Pyrmont",
            "types" : [ "locality", "political" ]
         },
         {
            "long_name" : "Council of the City of Sydney",
            "short_name" : "Sydney",
            "types" : [ "administrative_area_level_2", "political" ]
         },
         {
            "long_name" : "New South Wales",
            "short_name" : "NSW",
            "types" : [ "administrative_area_level_1", "political" ]
         },
         {
            "long_name" : "Australia",
            "short_name" : "AU",
            "types" : [ "country", "political" ]
         },
         {
            "long_name" : "2009",
            "short_name" : "2009",
            "types" : [ "postal_code" ]
         }
      ],
      "formatted_address" : "5, 48 Pirrama Rd, Pyrmont NSW 2009, Australia",
      "formatted_phone_number" : "(02) 9374 4000",
      "geometry" : {
         "location" : {
            "lat" : -33.866651,
            "lng" : 151.195827
         },
         "viewport" : {
            "northeast" : {
               "lat" : -33.8653881697085,
               "lng" : 151.1969739802915
            },
            "southwest" : {
               "lat" : -33.86808613029149,
               "lng" : 151.1942760197085
            }
         }
      },
      "icon" : "https://maps.gstatic.com/mapfiles/place_api/icons/generic_business-71.png",
      "id" : "4f89212bf76dde31f092cfc14d7506555d85b5c7",
      "international_phone_number" : "+61 2 9374 4000",
      "name" : "Google",
      "place_id" : "ChIJN1t_tDeuEmsRUsoyG83frY4",
      "rating" : 4.5,
      "reference" : "CmRSAAAAjiEr2_A4yI-DyqGcfsceTv-IBJXHB5-W3ckmGk9QAYk4USgeV8ihBcGBEK5Z1w4ajRZNVAfSbROiKbbuniq0c9rIq_xqkrf_3HpZzX-pFJuJY3cBtG68LSAHzWXB8UzwEhAx04rgN0_WieYLfVp4K0duGhTU58LFaqwcaex73Kcyy0ghYOQTkg",
      "reviews" : [
         {
            "author_name" : "Robert Ardill",
            "author_url" : "https://www.google.com/maps/contrib/106422854611155436041/reviews",
            "language" : "en",
            "profile_photo_url" : "https://lh3.googleusercontent.com/-T47KxWuAoJU/AAAAAAAAAAI/AAAAAAAAAZo/BDmyI12BZAs/s128-c0x00000000-cc-rp-mo-ba1/photo.jpg",
            "rating" : 5,
            "relative_time_description" : "a month ago",
            "text" : "Awesome offices. Great facilities, location and views. Staff are great hosts",
            "time" : 1491144016
         }
      ],
      "scope" : "GOOGLE",
      "types" : [ "point_of_interest", "establishment" ],
      "url" : "https://maps.google.com/?cid=10281119596374313554",
      "utc_offset" : 600,
      "vicinity" : "5, 48 Pirrama Road, Pyrmont",
      "website" : "https://www.google.com.au/about/careers/locations/sydney/"
   },
   "status" : "OK"
}
"""
GOOGLE_MAPS_DETAILS_RESPONSE = json.loads(GOOGLE_MAPS_DETAILS_RESPONSE_JSON)

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
