"""Test the google module."""

import json

import googlemaps
from faker import Faker
import pytest

from api.collectors.base import BusinessInfo
from api.collectors.base import PlaceSearchSummary
from api.collectors.google import GoogleCollector


@pytest.fixture()
def google_collector():
    """
    Return a GoogleCollector.

    A valid API key for the Google Maps client starts with "AIza".
    """
    c = GoogleCollector()
    c.authenticate('AIzaasdf')
    return c


class TestGoogleCollector():
    """Implement tests for the Google collector."""
    fake = Faker()

    def test_search_places_00(self, mocker, google_collector):
        """Ensure the search returns a dictionary."""
        gmaps = google_collector

        mocker.patch.object(googlemaps.Client, 'find_place', return_value=GOOGLE_MAPS_SEARCH_RESPONSE)
        search_results = gmaps.search_places(self.fake.address(), terms=self.fake.pyint())

        assert type(search_results) is dict

    def test_place_details_00(self, mocker, google_collector):
        """Ensure retrieve_place_details returns a dictionary."""
        gmaps = google_collector

        mocker.patch.object(googlemaps.Client, 'place', return_value=GOOGLE_MAPS_DETAILS_RESPONSE)
        details_results = gmaps.get_place_details(self.fake.pystr())

        assert type(details_results) is dict

    def test_place_details_01(self, mocker, google_collector):
        """Ensure retrieve_place_details returns a dictionary."""
        gmaps = google_collector

        mocker.patch.object(googlemaps.Client, 'place', return_value=GOOGLE_MAPS_DETAILS_RESPONSE)
        _ = gmaps.get_place_details(self.fake.pystr())

        actual = gmaps.to_business_info()
        expected = BusinessInfo(
            name='Google',
            address='5, 48 Pirrama Rd, Pyrmont NSW 2009, Australia',
            latitude=-33.866651,
            longitude=151.195827,
            type='',
            phone='(02) 9374 4000',
            email='',
            contact_name='',
            website='https://www.google.com.au/about/careers/locations/sydney/',
            parking_info='',
            extra_info='',
            weight=0)

        assert actual == expected

    def test_to_business_info_00(self, google_collector):
        """Ensure empty search results return `None`."""
        gmaps = google_collector

        actual = gmaps.to_business_info()
        expected = None

        assert actual == expected

    def test_to_business_info_01(self, google_collector):
        """Ensure empty search results return `None`."""
        gmaps = google_collector
        gmaps.result = {'fake_key': 'fake_value'}

        actual = gmaps.to_business_info()
        expected = None

        assert actual == expected

    def test_retrieve_search_summary_00(self, google_collector):
        """Ensure empty search results return `None`."""
        gmaps = google_collector

        actual = gmaps.retrieve_search_summary()
        expected = None

        assert actual == expected

    def test_retrieve_search_summary_01(self, google_collector):
        """Ensure empty search results return `None`."""
        gmaps = google_collector
        gmaps.search_results = {'fake_key': 'fake_value'}

        actual = gmaps.retrieve_search_summary()
        expected = None

        assert actual == expected

    def test_retrieve_search_summary_02(self, google_collector):
        """Ensure the first result of the search is returned as a `PlaceSearchSummary`."""
        gmaps = google_collector
        gmaps.search_results = GOOGLE_MAPS_SEARCH_RESPONSE
        actual = gmaps.retrieve_search_summary()
        expected = PlaceSearchSummary(
            place_id='ChIJyWEHuEmuEmsRm9hTkapTCrk',
            name='Rhythmboat Cruises',
            address='Pyrmont Bay Wharf Darling Dr, Sydney',
        )

        assert actual == expected

    def test_search_places_nearby_00(self, mocker, google_collector):
        """"""
        gmaps = google_collector
        mocker.patch.object(googlemaps.Client, 'places_nearby', return_value=GOOGLE_MAPS_NEARBY_SEARCH_RESPONSE)

        actual = gmaps.search_places_nearby(self.fake.address())
        expected = GOOGLE_MAPS_NEARBY_SEARCH_RESPONSE

        assert actual == expected


# Google Maps Place Search API Response example.
# https://developers.google.com/places/web-service/search#PlaceSearchResponses
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

# Google Maps Place Details API Response example.
# https://developers.google.com/places/web-service/details#PlaceDetailsResponses
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

# Google Maps NearbySearch API Response example.
# https://developers.google.com/places/web-service/search#PlaceSearchRequests
GOOGLE_MAPS_NEARBY_SEARCH_RESPONSE_JSON = r"""
{
  "html_attributions": [],
  "results": [
    {
      "geometry": {
        "location": {
          "lat": -33.8585858,
          "lng": 151.2100415
        },
        "viewport": {
          "northeast": {
            "lat": -33.85723597010728,
            "lng": 151.2113913298927
          },
          "southwest": {
            "lat": -33.85993562989272,
            "lng": 151.2086916701072
          }
        }
      },
      "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/bar-71.png",
      "id": "8e980ad0c819c33cdb1cea31e72d654ca61a7065",
      "name": "Cruise Bar, Restaurant & Events",
      "opening_hours": {
        "open_now": false
      },
      "photos": [
        {
          "height": 1134,
          "html_attributions": [
            "<a href=\"https://maps.google.com/maps/contrib/112582655193348962755/photos\">Cruise Bar, Restaurant &amp; Events</a>"
          ],
          "photo_reference": "CmRaAAAArxGi1pAqcm6zBPnX6Kjp1hy1lNrC-dSlm3w5-_ufK1thWjYRpGCz-jF5YycDLI91wzMPMAWwEyNABou1UuBSkLieewnuY3MzGANUypmfZ40SZaEQ8RXnkrvUGYwrnBAbEhAe2PFhct6sIRnmJh2Id3OMGhQAphJP9xD7Wxeft-379derw7vfkQ",
          "width": 2048
        }
      ],
      "place_id": "ChIJi6C1MxquEmsR9-c-3O48ykI",
      "plus_code": {
        "compound_code": "46R6+H2 The Rocks, New South Wales",
        "global_code": "4RRH46R6+H2"
      },
      "rating": 4,
      "reference": "CmRbAAAAe2tm4tmBBE1M9r6Wu4iN3qUXXReIcMETqNDQba7CWKUrEh2elnPNDsHdIqRvxymwqYOClhirkbR-M_xJ_-LKRIM-TBqAkk9kTMiuuHUOpn8MtCNU7hFsfOJLSG_3lchVEhATdb3OT5BLTw9U_zyiBOyaGhRIXVhuPNhRuvPBeCwYa4cYdmbAPg",
      "scope": "GOOGLE",
      "types": [
        "bar",
        "restaurant",
        "food",
        "point_of_interest",
        "establishment"
      ],
      "vicinity": "Circular Quay W, Sydney"
    },
    {
      "geometry": {
        "location": {
          "lat": -33.867591,
          "lng": 151.201196
        },
        "viewport": {
          "northeast": {
            "lat": -33.86624117010727,
            "lng": 151.2025458298927
          },
          "southwest": {
            "lat": -33.86894082989271,
            "lng": 151.1998461701072
          }
        }
      },
      "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/generic_business-71.png",
      "id": "a97f9fb468bcd26b68a23072a55af82d4b325e0d",
      "name": "Australian Cruise Group",
      "opening_hours": {
        "open_now": false
      },
      "photos": [
        {
          "height": 417,
          "html_attributions": [
            "<a href=\"https://maps.google.com/maps/contrib/110751364053842618118/photos\">Australian Cruise Group</a>"
          ],
          "photo_reference": "CmRaAAAAD_KdpOiGCxGooItucIQkXxzpO1M_n7JQYD2qtrqH0mRnQOzGaqaeehm3V8hT8NMAncc8VInx6eD-UhryUZDOh6thOcRevvteQc3FEiZayqhgDvDqnInFYl7oCyeMfIITEhDxC_dccN9nD1oANsuPxSyhGhQBNMpIp72-p4MEP24nrGpxK8ihaw",
          "width": 1334
        }
      ],
      "place_id": "ChIJrTLr-GyuEmsRBfy61i59si0",
      "plus_code": {
        "compound_code": "46J2+XF Sydney, New South Wales",
        "global_code": "4RRH46J2+XF"
      },
      "rating": 4.6,
      "reference": "CmRbAAAA9iHju4hgzD8x9YBrgRthxsuO9z0sWpxiyXbG8goVJ2n9EDJciluTK29O9_3jJemVFz3wMT3DMwlViOtkJOWlrz1gKZ-nw-yIymXie62BKcKNMjcqbYtqLsmYMtcJnHVyEhDT2Go_a2kIxso43Qyrgku8GhRUhT-Ygamo7LXdH7xO4fePpA3bLA",
      "scope": "GOOGLE",
      "types": [
        "travel_agency",
        "restaurant",
        "food",
        "point_of_interest",
        "establishment"
      ],
      "vicinity": "King Street, Wharf 5, 32 The Promenade, Sydney"
    },
    {
      "geometry": {
        "location": {
          "lat": -33.8686058,
          "lng": 151.2018206
        },
        "viewport": {
          "northeast": {
            "lat": -33.86725597010728,
            "lng": 151.2031704298927
          },
          "southwest": {
            "lat": -33.86995562989272,
            "lng": 151.2004707701072
          }
        }
      },
      "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/generic_business-71.png",
      "id": "21a0b251c9b8392186142c798263e289fe45b4aa",
      "name": "Rhythmboat Cruises",
      "opening_hours": {
        "open_now": false
      },
      "photos": [
        {
          "height": 480,
          "html_attributions": [
            "<a href=\"https://maps.google.com/maps/contrib/104066891898402903288/photos\">Rhythmboat Cruises</a>"
          ],
          "photo_reference": "CmRaAAAA5iUzy16SheBgLthHZ_tW3Y2CLaLHrsAFrvMW-yULhe1OrhbFl3KwcyAWQAS3RhECmTdwRTxNouKTXX5LQSEO3dBB6tnTOMsGjnh_pEIsYD7ZKxKgNFnVqfdr_o2KZdlrEhApm76YIqTLOsz3ARK3uxhPGhTRjgT8MH5yn2okG0KvHElDnNdxvw",
          "width": 640
        }
      ],
      "place_id": "ChIJyWEHuEmuEmsRm9hTkapTCrk",
      "plus_code": {
        "compound_code": "46J2+HP Sydney, New South Wales",
        "global_code": "4RRH46J2+HP"
      },
      "rating": 3.9,
      "reference": "CmRbAAAAG-Os89OKRh4gGtyl0-wBlfBFjdVwIzSqwZ_uqZm0NrGbCgKOxdby-HXEu2V_JqB_NDr8QNCmCPohF-5hU1j0ojdKGVl1a7kBraOmp2UGfRTQxVrjvCZcpkcOWDrupzF_EhDRpawmyNlcsaGt0CFc7EQdGhQgHf-zzet2KTb_f4fmJJ727XTlxQ",
      "scope": "GOOGLE",
      "types": [
        "travel_agency",
        "restaurant",
        "food",
        "point_of_interest",
        "establishment"
      ],
      "vicinity": "King Street Wharf, King St, Sydney"
    },
    {
      "geometry": {
        "location": {
          "lat": -33.8609472,
          "lng": 151.209872
        },
        "viewport": {
          "northeast": {
            "lat": -33.85959737010728,
            "lng": 151.2112218298927
          },
          "southwest": {
            "lat": -33.86229702989272,
            "lng": 151.2085221701072
          }
        }
      },
      "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/generic_business-71.png",
      "id": "9ea7c77cb181b1f33d19c9d76121fcc6d5246ad8",
      "name": "Australian Cruise Group Circular Quay",
      "opening_hours": {
        "open_now": false
      },
      "photos": [
        {
          "height": 1152,
          "html_attributions": [
            "<a href=\"https://maps.google.com/maps/contrib/112378780393544273770/photos\">Australian Cruise Group Circular Quay</a>"
          ],
          "photo_reference": "CmRaAAAABtdvodKa5MFD4M8I1h-qQuPTUO4iFyeJL7IVJLRkexZRcj0F21Pj5PKR18FUQBvzdAX_aS_xnj6XlsojaKfg35ityppRUjhMeEQR-_Yz2TY1nd0moCyiciXYuCQZHkEkEhDlV-2ENNut70BcDL7uS0PPGhSJdHnaIpkAux0GoLu3fYP9Gro10w",
          "width": 2048
        }
      ],
      "place_id": "ChIJpU8KgUKuEmsRKErVGEaa11w",
      "plus_code": {
        "compound_code": "46Q5+JW Sydney, New South Wales",
        "global_code": "4RRH46Q5+JW"
      },
      "rating": 4.3,
      "reference": "CmRbAAAARDlIm_It1-7Ty_P15-ZMvQ_U8Jr9G-Tetj3wjbECRu9R1UT3biXZrassyOXdW3RCRb3qQeXqgLHkvFdivIJ-gP3h04dBlgG1vLiDyQxHV8pf40Zw19qVtq7hlfLyJn77EhCpLdkKAvNxjKWRrZkATbpXGhSquEhYheVYDO2T4Jj2Lc1yBR3FMw",
      "scope": "GOOGLE",
      "types": [
        "travel_agency",
        "restaurant",
        "food",
        "point_of_interest",
        "establishment"
      ],
      "vicinity": "6 Cirular Quay, Sydney"
    },
    {
      "geometry": {
        "location": {
          "lat": -33.871047,
          "lng": 151.189736
        },
        "viewport": {
          "northeast": {
            "lat": -33.86937207010727,
            "lng": 151.1912860798927
          },
          "southwest": {
            "lat": -33.87207172989272,
            "lng": 151.1885864201072
          }
        }
      },
      "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/generic_business-71.png",
      "id": "3458f23c154e574552e0722773a46f384816b241",
      "name": "Vagabond Cruises",
      "opening_hours": {
        "open_now": false
      },
      "photos": [
        {
          "height": 1200,
          "html_attributions": [
            "<a href=\"https://maps.google.com/maps/contrib/101516907347198229066/photos\">Vagabond Cruises</a>"
          ],
          "photo_reference": "CmRaAAAAGF-CcVkuZyc8fNjh57DwMzoXwtvMcIBVZ-_naKaLL45dff6MRODU6cpPvnRPwazEBC5Ly6yweJXD4Kq-80L60_cePao4nFC9TBbJv6n2gVOBdWcuXKuM0FUxYAzQzimOEhA1ZIpHk4kTsuqAEPQn7NDaGhQqjI9eFO4XsDYPA7lyMFKXFyvKWA",
          "width": 1800
        }
      ],
      "place_id": "ChIJLfySpTOuEmsRMFymbMkVkOE",
      "plus_code": {
        "compound_code": "45HQ+HV Pyrmont, New South Wales",
        "global_code": "4RRH45HQ+HV"
      },
      "rating": 3.4,
      "reference": "CmRbAAAAyC4NblpPi4YylOE7excN0dBsN5iRd_SBBLg8JDgvltwLdY4tDOySKg4Ng4j8nKVYDy7FVldiNDSzpbe7WwzehMZLC-78WFRKs9lrN_OqIfx_o7MbLZ767p2aCbtkXPWlEhA117YgRJfqzfR-mHG_59XKGhSaZKNIIKhr87fUiQullkHSYmVS3w",
      "scope": "GOOGLE",
      "types": [
        "travel_agency",
        "restaurant",
        "food",
        "point_of_interest",
        "establishment"
      ],
      "vicinity": "37 Bank St, Pyrmont"
    },
    {
      "geometry": {
        "location": {
          "lat": -33.867591,
          "lng": 151.201196
        },
        "viewport": {
          "northeast": {
            "lat": -33.86624117010727,
            "lng": 151.2025458298927
          },
          "southwest": {
            "lat": -33.86894082989271,
            "lng": 151.1998461701072
          }
        }
      },
      "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/generic_business-71.png",
      "id": "b0277cade7696e575824681aba949d68814f9efe",
      "name": "Sydney New Year's Eve Cruises",
      "opening_hours": {
        "open_now": false
      },
      "photos": [
        {
          "height": 1152,
          "html_attributions": [
            "<a href=\"https://maps.google.com/maps/contrib/107666140764925298472/photos\">Sydney New Year&#39;s Eve Cruises</a>"
          ],
          "photo_reference": "CmRaAAAA2zBa5h8LwLGmCUkqHu4zdNyDmhrX_9s58yjKLjRs2JePWQGvlOVIjkUHZ_tePJJ-9iEhzR5BQft2Cc-0wCj3JJggSdvv5f6UrAUiMWF6cFn02J7hny5R78PW1WkQo3DAEhA7VAkKxWeZYrIrCRm8Of_sGhQ8Ms-A-GSrcX513DgDv28clZrR0g",
          "width": 2048
        }
      ],
      "place_id": "ChIJ__8_hziuEmsR27ucFXECfOg",
      "plus_code": {
        "compound_code": "46J2+XF Sydney, New South Wales",
        "global_code": "4RRH46J2+XF"
      },
      "rating": 5,
      "reference": "CmRbAAAAtdaJcqUg4P6BLGOcDt969X3EC1IDTuvhXNCBIlrMoEkjVQ1VC01PEeAZ3aSwyljCDapgytTGI1KJvmt0hfTUHwDPtX9vrpiQOPGap_aggbS5zhCY2EviF6-TD7C3J3I9EhBYn1IXHO4AufJMXDGh2MFkGhTceqvSUlXYIT6ebaVc2AREm6prVw",
      "scope": "GOOGLE",
      "types": [
        "travel_agency",
        "restaurant",
        "food",
        "point_of_interest",
        "establishment"
      ],
      "vicinity": "32 The Promenade, King Street Wharf 5, Sydney"
    },
    {
      "geometry": {
        "location": {
          "lat": -33.873825,
          "lng": 151.192584
        },
        "viewport": {
          "northeast": {
            "lat": -33.87247632010728,
            "lng": 151.1939354798927
          },
          "southwest": {
            "lat": -33.87517597989272,
            "lng": 151.1912358201073
          }
        }
      },
      "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/generic_business-71.png",
      "id": "48d507d8c878b31eca0b7067698195ab57904c75",
      "name": "Twin Peeks Afloat - Sydney's only luxury adult entertainment cruise",
      "opening_hours": {
        "open_now": false
      },
      "photos": [
        {
          "height": 450,
          "html_attributions": [
            "<a href=\"https://maps.google.com/maps/contrib/112593646930206915862/photos\">Twin Peeks Afloat - Sydney&#39;s only luxury adult entertainment cruise</a>"
          ],
          "photo_reference": "CmRaAAAAMsaCK9LuI163lmGF_-haSBf0USUB51Yz02nx1aA9POdHza4A8BRgGcVUadCbL5rXfNddeg3MDFPCHzu2v-MWBu93JF_iDgDxFqKwTxiijj-cMzcYxDhvOi97fNaYdWYUEhA2OTMMPFDgRyyJBYTgvY8_GhSEMoH9OhIymPGvqv79zwqBs0VCEA",
          "width": 980
        }
      ],
      "place_id": "ChIJD5bUHTKuEmsRhoLAfaJq86U",
      "plus_code": {
        "compound_code": "45GV+F2 Pyrmont, New South Wales",
        "global_code": "4RRH45GV+F2"
      },
      "reference": "CmRbAAAAY3XGuUI0xe49ZGYQXKKgZqkqozix94vn6CtJPf1-YWSrSH42ONt2zouZqnj0yAdJFNkoA2ZHxumxJ_mzPUqZNaMUNnDZqjiXgxdLht7vFG8b1FsjQDEYDbv6-9Bs8NxGEhBmOY2tZD2bFagVFonz4B6OGhSdReLb4cmtB_332eUpE_l5JU9JZg",
      "scope": "GOOGLE",
      "types": [
        "travel_agency",
        "restaurant",
        "food",
        "point_of_interest",
        "establishment"
      ],
      "vicinity": "155/3 Pyrmont Bridge Rd, Pyrmont"
    },
    {
      "geometry": {
        "location": {
          "lat": -33.867594,
          "lng": 151.2012168
        },
        "viewport": {
          "northeast": {
            "lat": -33.86624417010727,
            "lng": 151.2025666298927
          },
          "southwest": {
            "lat": -33.86894382989271,
            "lng": 151.1998669701073
          }
        }
      },
      "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/generic_business-71.png",
      "id": "f1e044040bd03ff06e19de4798b52dd926855281",
      "name": "Sydney Harbour Dinner Cruises",
      "opening_hours": {
        "open_now": false
      },
      "place_id": "ChIJM1mOVTS6EmsRKaDzrTsgids",
      "plus_code": {
        "compound_code": "46J2+XF Belmore, New South Wales",
        "global_code": "4RRH46J2+XF"
      },
      "reference": "CmRbAAAAiXIiuXaxk5YUfg5SkZom5-vCA23WlK7Jf8Mp4g0tTUJ67-WHvmN43HXEMMneQGixIgqz6jnmqNnI_eM61B-zMM-bJqr07F4NG-Vf4BrQM3TABzwbWHQ6WhMqcWfRS5K1EhDXRG4l-eew6mfF48jT45-UGhT3yGlOCXqHwjm3kzs2wqJdpO_oSg",
      "scope": "GOOGLE",
      "types": [
        "travel_agency",
        "restaurant",
        "food",
        "point_of_interest",
        "establishment"
      ],
      "vicinity": "32 The Promenade, Sydney"
    }
  ],
  "status": "OK"
}
"""
GOOGLE_MAPS_NEARBY_SEARCH_RESPONSE = json.loads(GOOGLE_MAPS_NEARBY_SEARCH_RESPONSE_JSON)
