"""Define the Celery tasks."""
from celery import chain
from celery.schedules import crontab
from celery.utils.log import get_task_logger

from api.celery.celery import app

logger = get_task_logger(__name__)


@app.task
def add(x, y):
    return x + y
