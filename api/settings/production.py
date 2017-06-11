from .base import *  # noqa
import os

import dj_database_url

# Disable debug modes.
DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# Get tbe production secret from the environment variables.
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# Get tbe production allowed hosts from the environment variables, or limit it to localhost only.
ALLOWED_HOSTS = os.environ['DJANGO_ALLOWED_HOSTS'].split(',')
