"""Define the Celery tasks."""
import os

from celery import chord
from celery.utils.log import get_task_logger

from api.apps.api.collectors.base import BusinessInfo
from api.apps.api.collectors.generic import CollectorClient
from api.celery.worker import app

logger = get_task_logger(__name__)


@app.task(ignore_result=False)
def add(x, y):
    """Add 2 numbers together."""
    logger.info(f'Starting add task with {x},{y}.')
    return int(x + y)


@app.task(ignore_result=False)
def collect_place_details_from_google(place_id):
    """Collect business information from Google."""
    # Prepare client.
    client = CollectorClient('google', api_key=os.environ['RYR_COLLECTOR_GOOGLE_PLACES_API_KEY'])
    client.authenticate()

    # Retrieve detailed results.
    details = client.get_place_details(place_id)
    return details


@app.task(ignore_result=False)
def collect_place_details_from_yelp(name, address):
    """Collect business information from Yelp."""
    # Prepare client.
    client = CollectorClient('yelp', api_key=os.environ['RYR_COLLECTOR_YELP_API_KEY'])
    client.authenticate()

    # Retrieve detailed results.
    client.search_places(address, terms=name, limit=1)
    place_id = client.retrieve_search_summary(0)

    # Extract the place_id.
    details = client.get_place_details(place_id)
    return details


@app.task(ignore_result=False)
def combine_collector_results(collector_results):
    """Combine the results provided by several collectors."""
    # No idea why `collector_results` becomes a list of tuples of `BusinessInfo` !?!?!
    c = BusinessInfo()
    for collector_result in collector_results:
        c = c.merge(collector_result[0])

    return c


def collect_place_details(place_id, name, address):
    """Collect the details of a specific place from all the provider."""
    callback = combine_collector_results.s()
    collect_place_details_from_google.s(place_id)
    header = [collect_place_details_from_yelp.s(name, address)]
    result = chord(header)(callback)
    return result
