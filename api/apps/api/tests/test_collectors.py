from faker import Faker
import pytest

from api.apps.api.collectors.collector import CollectorClient


@pytest.fixture()
def fake_collector_client():
    pass


class TestCollectorClient():
    """Empty test"""

    def test_authenticate_00(self):
        """Ensure an invalid provider raises an error."""
        fake = Faker()
        c = CollectorClient(fake.pystr())
        with pytest.raises(ValueError):
            c.authenticate()
        assert True

    def test_retrieve_details_00(self, mocker):
        """Ensure an ID is returned."""
        fake = Faker()
        c = CollectorClient(fake.pystr())

        # Prepare the expected returned value.
        details = {
            'name': fake.company(),
            'address': fake.address(),
            'phone': fake.phone_number(),
        }

        # Mock the retrieve_details function.
        mock_retrieve_details = mocker.patch.object(CollectorClient, 'retrieve_details', return_value=details)

        assert c.retrieve_details() == details
