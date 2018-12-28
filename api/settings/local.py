"""Define the connexion settings for a local setup."""
import os

from api.settings.common import *  # noqa

DEBUG = True
if os.environ.get('KUBERNETES_PORT'):
    environment_based_spec_dir = '/usr/local/etc/ryr-api'
    BASE_URL = 'http://api.192.168.99.100.nip.io'
else:
    environment_based_spec_dir = 'openapi'
    BASE_URL = f'http://0.0.0.0:{PORT}'
SPECIFICATION_DIR = os.path.join(BASE_DIR, environment_based_spec_dir)
