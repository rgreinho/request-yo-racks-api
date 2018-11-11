"""Test the base module."""
from faker import Faker
import pytest

from api.collectors.base import AbstractCollector
from api.collectors.base import BusinessInfo
from api.collectors.base import PlaceSearchSummary


class TestBusinessInfo:
    """Implement tests for BusinessInfo."""

    # Merge scenario list.
    # The first tuple contains:
    #   0. first BusinessInfo object
    #   1. second BusinessInfo object
    #   2. expected result
    # The second tuple is a description of the scenario.
    merge_scenarios = [
        ((
            BusinessInfo(name='name1'),
            BusinessInfo(address='address2'),
            BusinessInfo(name='name1', address='address2'),
        ), 'Ensure different properties are merged for same weight objects.'),
        ((
            BusinessInfo(name='name1'),
            BusinessInfo(name='name2'),
            BusinessInfo(name='name1'),
        ), 'Ensure no property is overwritten for same weight objects.'),
        ((
            BusinessInfo(name='name1', weight=1),
            BusinessInfo(name='name2', weight=5),
            BusinessInfo(name='name1'),
        ), 'Ensure objects with the less weight overwrites properties.'),
        ((
            BusinessInfo(name='name1', weight=3),
            BusinessInfo(name='name2', weight=2),
            BusinessInfo(name='name2'),
        ), 'Ensure objects with the less weight overwrites properties.'),
        ((
            BusinessInfo(name='name1', weight=3),
            BusinessInfo(address='address2', weight=2),
            BusinessInfo(name='name1', address='address2'),
        ), 'Ensure objects with the less weight overwrites properties.'),
        ((
            BusinessInfo(name='name1', weight=3),
            PlaceSearchSummary(),
            BusinessInfo(name='name1', weight=3),
        ), 'Ensure objects of different types don\'t merge'),
    ]

    def scenario_inputs(scenarios):
        """Parse the scenarios and feed the data to the test function."""
        return [test_input[0] for test_input in scenarios]

    def scenario_ids(scenarios):
        """Parse the scenarios and feed the IDs to the test function."""
        return [test_input[1] for test_input in scenarios]

    def test_geolocation_00(self):
        """Ensure geolocation is computed properly for default objects."""
        b1 = BusinessInfo()
        assert b1.geolocation() == '0.0,0.0'

    def test_geolocation_01(self):
        """Ensure geolocation is computed properly."""
        b1 = BusinessInfo(latitude=1.0, longitude=2.0)
        assert b1.geolocation() == '1.0,2.0'

    @pytest.mark.parametrize("test_input", scenario_inputs(merge_scenarios), ids=scenario_ids(merge_scenarios))
    def test_merge(self, test_input):
        """Ensure objects are merge correctly."""
        actual = test_input[0].merge(test_input[1])
        expected = test_input[2]
        assert actual == expected

    def test_to_json_00(self):
        """Ensure the object serializes to JSON correctly."""
        b = BusinessInfo(name='name1', address='address2')
        actual = b.to_json(indent=None)
        expected = '{"__instance_type__": ["api.collectors.base", "BusinessInfo"], "attributes": {"address": "address2", "contact_name": "", "email": "", "extra_info": "", "latitude": 0.0, "longitude": 0.0, "name": "name1", "parking_info": "", "phone": "", "type": "", "website": "", "weight": 0}}'
        assert actual == expected

    def test_from_json_00(self):
        """Ensure the object get deserialized from JSON correctly."""
        json_object = '{"__instance_type__": ["api.collectors.base", "BusinessInfo"], "attributes": {"address": "address2", "contact_name": "", "email": "", "extra_info": "", "latitude": 0.0, "longitude": 0.0, "name": "name1", "parking_info": "", "phone": "", "type": "", "website": "", "weight": 0}}'
        actual = BusinessInfo.from_json(json_object)
        expected = BusinessInfo(name='name1', address='address2')
        assert actual == expected


class TestAbstractCollector:
    """Implement tests for AbstractCollector."""
    fake = Faker()

    def test_no_abstract_function_is_implemented(self):
        """Ensure that abstract functions raise NotImplementedError."""
        a = AbstractCollector()
        with pytest.raises(NotImplementedError):
            a.authenticate(self.fake.pystr())
        with pytest.raises(NotImplementedError):
            a.get_place_details(self.fake.pystr())
        with pytest.raises(NotImplementedError):
            a.search_places(self.fake.pystr())
        with pytest.raises(NotImplementedError):
            a.search_places_nearby(self.fake.pystr())
        with pytest.raises(NotImplementedError):
            a.to_business_info()

        assert True
