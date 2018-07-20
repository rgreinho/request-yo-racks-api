"""Define the django settings for a testing setup."""
from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'CHANGE THIS!!!'

# Allow all host headers
# SECURITY WARNING: don't run with this setting in production!
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['api.192.168.99.100.nip.io']

# CORS settings.
# https://github.com/ottoyiu/django-cors-headers#cors_origin_allow_all
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = ['www.192.168.99.100.nip.io']
