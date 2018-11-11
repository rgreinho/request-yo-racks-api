"""Test the Celery tasks."""
import dataclasses
import os
from unittest.mock import Mock

from celery import chord
from celery import group
from faker import Faker
import googlemaps
import pytest
import requests
import responses

from api.celery import tasks
from api.collectors.base import BusinessInfo
from api.collectors.base import PlaceSearchSummary
from api.collectors.generic import CollectorClient
from api.collectors.yelp import YelpCollector
from tests.collectors.test_google import GOOGLE_MAPS_DETAILS_RESPONSE
from tests.collectors.test_yelp import YELP_DETAILS_RESPONSE
from tests.collectors.test_yelp import YELP_SEARCH_RESPONSE


class TestCeleryTasks:
    """Test the Celery tasks."""
    fake = Faker()

    def test_add(self, mocker):
        """Ensure add works."""

        task = tasks.add.s(1, 1).apply()
        assert task.successful()
        assert task.result == 2

    def test_collect_place_details_from_google_00(self, mocker):
        """Ensure data are retrieved from Google."""
        google_info = {
            'name': 'Google',
            'address': '5, 48 Pirrama Rd, Pyrmont NSW 2009, Australia',
            'latitude': -33.866651,
            'longitude': 151.195827,
            'type': '',
            'phone': '(02) 9374 4000',
            'email': '',
            'contact_name': '',
            'website': 'https://www.google.com.au/about/careers/locations/sydney/',
            'parking_info': '',
            'extra_info': '',
            'weight': 0
        }
        mocker.patch.dict(
            'os.environ',
            {
                'RYR_COLLECTOR_GOOGLE_PLACES_API_KEY': 'AIza' + self.fake.pystr(),
            },
        )
        mocker.patch.object(
            googlemaps.Client,
            'place',
            return_value=GOOGLE_MAPS_DETAILS_RESPONSE,
        )
        task = tasks.collect_place_details_from_google.s(self.fake.pystr()).apply()
        assert task.successful()
        assert dataclasses.asdict(task.result) == google_info

    @responses.activate
    def test_collect_place_details_from_yelp_00(self, mocker):
        """Ensure data are retrieved from Yelp."""
        yelp_info = {
            'name': 'Gary Danko',
            'address': '800 N Point St San Francisco, CA 94109',
            'latitude': 37.80587,
            'longitude': -122.42058,
            'type': 'American (New)',
            'phone': '+14152520800',
            'email': '',
            'contact_name': '',
            'website': '',
            'parking_info': '',
            'extra_info': '',
            'weight': 0
        }
        mocker.patch.dict(
            'os.environ',
            {
                'RYR_COLLECTOR_YELP_API_KEY': self.fake.pystr(),
            },
        )
        responses.add(
            responses.GET,
            'https://api.yelp.com/v3/businesses/search',
            json=YELP_SEARCH_RESPONSE,
            status=200,
        )
        responses.add(
            responses.GET,
            'https://api.yelp.com/v3/businesses/four-barrel-coffee-san-francisco',
            json=YELP_DETAILS_RESPONSE,
            status=200,
        )
        task = tasks.collect_place_details_from_yelp.s(
            self.fake.pystr(),
            self.fake.pystr(),
        ).apply()
        assert task.successful()
        assert dataclasses.asdict(task.result) == yelp_info

    def test_combine_collector_results_00(self):
        """Ensure results are combined correctly."""
        b0 = BusinessInfo(name='name1')
        b1 = BusinessInfo(address='address2')
        b2 = BusinessInfo(name='name1', address='address2')
        task = tasks.combine_collector_results.s([b0, b1]).apply()
        assert task.successful()
        assert task.result == b2

    @pytest.mark.skip()
    def test_collect_place_details_00(self, mocker):
        """
        Ensure data are collected from multiple collectors then combined.

        Test with "Epoch Coffee Shop - Northloop, Austin, TX."
        """
        kwargs = {
            'place_id': 'ChIJG-gJw2vKRIYROWi2uwOp8QE',
            'name': 'Epoch Coffee - North Loop',
            'address': '221 West North Loop Boulevard, Austin',
        }
        bi_google = BusinessInfo(
            name='Epoch Coffee - North Loop',
            address='221 W N Loop Blvd, Austin, TX 78751, USA',
            latitude=30.31865599999999,
            longitude=-97.72445499999999,
            type='',
            phone='(512) 454-3762',
            email='',
            contact_name='',
            website='http://www.epochcoffee.com/',
            parking_info='',
            extra_info='',
            weight=0)
        bi_yelp = BusinessInfo(
            name='Epoch Coffee',
            address='221 W North Loop Blvd Austin, TX 78751',
            latitude=30.3186,
            longitude=-97.72457,
            type='Coffee & Tea, Cafes',
            phone='+15124543762',
            email='',
            contact_name='',
            website='',
            parking_info='',
            extra_info='',
            weight=10)
        bi_combined = BusinessInfo(
            name='Epoch Coffee - North Loop',
            address='221 W N Loop Blvd, Austin, TX 78751, USA',
            latitude=30.31865599999999,
            longitude=-97.72445499999999,
            type='Coffee & Tea, Cafes',
            phone='(512) 454-3762',
            email='',
            contact_name='',
            website='http://www.epochcoffee.com/',
            parking_info='',
            extra_info='',
            weight=0)
        mocker.patch('api.celery.tasks.collect_place_details_from_google', return_value=bi_google)
        mocker.patch('api.celery.tasks.collect_place_details_from_yelp', return_value=bi_yelp)
        # task = tasks.collect_place_details(**kwargs)
        task = chord([tasks.collect_place_details_from_yelp.s(kwargs['name'], kwargs['address'])])(
            tasks.combine_collector_results.s()).apply()
