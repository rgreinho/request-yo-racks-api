"""Test the generic module."""

from faker import Faker
import pytest

from api.apps.api.collectors.base import PlaceSearchSummary
from api.apps.api.collectors.generic import CollectorClient


class TestCollectorClient:
    """Implement Tests for the generic collector client."""
    fake = Faker()

    def test_authenticate_00(self):
        """Ensure an invalid provider raises an error."""
        c = CollectorClient(self.fake.pystr())
        with pytest.raises(ValueError):
            c.authenticate()
        assert True

    def test_authenticate_01(self):
        """Ensure the generic client can authenticate to yelp."""
        c = CollectorClient('yelp', api_key=self.fake.pystr())
        c.authenticate()
        assert True

    def test_authenticate_02(self):
        """Ensure the generic client can authenticate to google."""
        c = CollectorClient('google', api_key=self.fake.pystr())
        with pytest.raises(ValueError):
            c.authenticate()
        assert True

    def test_get_place_details_00(self, mocker):
        """Ensure the collector functions are called."""
        c = CollectorClient(self.fake.pystr())
        c.collector = mocker.Mock()

        c.get_place_details(self.fake.pystr())

        c.collector.get_place_details.assert_called()

    def test_retrieve_search_summary_00(self, mocker):
        """Ensure the collector functions are called."""
        c = CollectorClient(self.fake.pystr())
        c.collector = mocker.Mock()

        c.retrieve_search_summary(self.fake.pystr())

        c.collector.retrieve_search_summary.assert_called()

    def test_retrieve_search_places_00(self, mocker):
        """Ensure the collector functions are called."""
        c = CollectorClient(self.fake.pystr())
        c.collector = mocker.Mock()

        c.search_places(self.fake.pystr())

        c.collector.search_places.assert_called()

    def test_lookup_place_00(self, mocker):
        """Ensure lookup fails when invoked without arguments."""
        c = CollectorClient(self.fake.pystr())
        with pytest.raises(ValueError):
            c.lookup_place()

        assert True

    def test_lookup_place_01(self, mocker):
        """Ensure lookup returns details for a given place_id."""
        fake_place_id = self.fake.pystr()
        c = CollectorClient(self.fake.pystr())
        c.get_place_details = mocker.Mock()

        c.lookup_place(place_id=fake_place_id)

        c.get_place_details.assert_called_with(fake_place_id)

    def test_lookup_place_02(self, mocker):
        """Ensure lookup returns details for a given name/address pair."""
        fake_place_id = self.fake.pystr()
        fake_name = self.fake.pystr()
        fake_address = self.fake.address()
        c = CollectorClient(self.fake.pystr())
        c.search_places = mocker.Mock()
        c.retrieve_search_summary = mocker.Mock(return_value=PlaceSearchSummary(id=fake_place_id))
        c.get_place_details = mocker.Mock()

        c.lookup_place(name=fake_name, address=fake_address)

        c.search_places.assert_called_with(address=fake_address, terms=fake_name, limit=1)
        c.get_place_details.assert_called_with(fake_place_id)

    def test_to_business_info_00(self, mocker):
        """Ensure the collector functions are called."""
        c = CollectorClient(self.fake.pystr())
        c.collector = mocker.Mock()

        c.to_business_info()

        c.collector.to_business_info.assert_called()
