"""Define the Celery tasks."""
import os

from celery import chord
from celery.utils.log import get_task_logger

from api.apps.api.collectors import BusinessInfo
from api.apps.api.collectors import CollectorClient
from api.celery.celery import app

logger = get_task_logger(__name__)


@app.task(ignore_result=False)
def add(x, y):
    """Add 2 numbers together."""
    logger.info(f'Starting add task with {x},{y}.')
    return int(x + y)


@app.task(ignore_result=False)
def collect_place_details_from_google(place_id):
    """Collect business information from Google."""
    # Define data.
    google_places_api_key = os.environ['RYR_COLLECTOR_GOOGLE_PLACES_API_KEY']

    # Prepare client.
    client = CollectorClient('google', api_key=google_places_api_key)
    client.authenticate()

    # Retrieve detailed results.
    details = client.retrieve_details(place_id)
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


def collect_place_details(place_id):
    """Collect the details of a specific place from all the provider."""
    callback = combine_collector_results.s()
    header = [collect_place_details_from_google.s(place_id)]
    result = chord(header)(callback)
    return result
