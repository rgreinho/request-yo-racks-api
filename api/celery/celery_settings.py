"""Configure Celery."""
import os

from celery.utils.log import get_task_logger
from json_tricks.nonp import dumps
from json_tricks.nonp import loads
from kombu.serialization import register

logger = get_task_logger(__name__)

# Register json-tricks as json encoder
register(
    'json_tricks.nonp',
    lambda obj: dumps(obj, conv_str_byte=True),
    lambda obj: loads(obj, conv_str_byte=True),
    content_type='application/x-json-tricks',
    content_encoding='utf-8',
)

# Global configuration.
accept_content = ['application/x-json-tricks', 'application/json']
imports = ('api.celery.tasks', )
timezone = 'America/Chicago'

# Beat configuration.
beat_max_loop_interval = 5

# Broker configuration.
broker_url = os.environ.get('CELERY_BROKER_URL', 'rpc://')

# Result configuration.
result_backend = os.environ.get('CELERY_RESULT_BACKEND', 'redis://')
result_serializer = 'json_tricks.nonp'

# Task configuration.
task_serializer = 'json_tricks.nonp'

# Worker condiguration.
worker_concurrency = 1
