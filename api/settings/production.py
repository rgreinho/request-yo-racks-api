import os

from .base import *  # noqa

# Disable debug modes.
DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# Get tbe production secret from the environment variables.
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"].strip()

# Get tbe production allowed hosts from the environment variables.
ALLOWED_HOSTS = os.environ['DJANGO_ALLOWED_HOSTS'].strip().split(',')

# CORS settings.
# https://github.com/ottoyiu/django-cors-headers#cors_origin_whitelist
CORS_ORIGIN_WHITELIST = os.environ['DJANGO_CORS_ORIGIN_WHITELIST'].strip().split(',')
