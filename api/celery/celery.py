"""Create the Celery app."""
from celery import Celery

# Celery application.
app = Celery()
app.config_from_object('api.celery.celery_settings')
# TODO(remyg): This does not seem to work.
app.autodiscover_tasks(['api.celery'])
