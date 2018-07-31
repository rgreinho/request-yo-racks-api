"""Define the Celery tasks."""
import os

from celery import chord
from celery.utils.log import get_task_logger

from api.apps.api.collectors.base import BusinessInfo
from api.apps.api.collectors.generic import CollectorClient
from api.celery.celery import app

logger = get_task_logger(__name__)

collectors_settings = {
    'google': {
        'api_key': os.environ['RYR_COLLECTOR_GOOGLE_PLACES_API_KEY']
    },
    'yelp': {
        'api_key': os.environ['RYR_COLLECTOR_YELP_API_KEY']
    }
}


@app.task(ignore_result=False)
def add(x, y):
    """Add 2 numbers together."""
    logger.info(f'Starting add task with {x},{y}.')
    return int(x + y)


@app.task(ignore_result=False)
def collect_place_details_from_google(place_id):
    """Collect business information from Google."""
    # Prepare client.
    client_name = 'google'
    client = CollectorClient(client_name, collectors_settings[client_name]['api_key'])
    client.authenticate()

    # Retrieve detailed results.
    details = client.place_details(place_id)
    return details


@app.task(ignore_result=False)
def collect_place_details_from_yelp(name, address):
    """Collect business information from Yelp."""
    # Prepare client.
    client_name = 'yelp'
    client = CollectorClient(client_name, collectors_settings[client_name]['api_key'])
    client.authenticate()

    # Retrieve detailed results.
    client.search_place(address, terms=name, limit=1)
    place_id = client.retrieve_place_id(0)

    # Extract the place_id.
    details = client.place_details(place_id)
    return details


@app.task(ignore_result=False)
def combine_collector_results(collector_results):
    """Combine the results provided by several collectors."""
    c = BusinessInfo()
    for collector_result in collector_results:
        tmp = BusinessInfo()
        tmp.__dict__ = collector_result
        c = c.merge(tmp)

    return c.__dict__


def collect_place_details(place_id, name, address):
    """Collect the details of a specific place from all the provider."""
    callback = combine_collector_results.s()
    collect_place_details_from_google.s(place_id)
    header = [collect_place_details_from_yelp()]
    result = chord(header)(callback)
    return result
