"""Define the connexion settings for a local setup."""
import os

from api.settings.common import *  # noqa

DEBUG = True
environment_based_spec_dir = '/usr/local/etc/ryr-api' if os.environ.get('KUBERNETES_PORT') else 'openapi'
SPECIFICATION_DIR = os.path.join(BASE_DIR, environment_based_spec_dir)
