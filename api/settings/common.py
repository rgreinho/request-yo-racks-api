"""Define the connexion settings common to all setup."""
import os

# PATH vars
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SPECIFICATION_DIR = os.path.join(BASE_DIR, 'openapi')
SPECIFICATION_FILE = 'openapi.yaml'

# Server parameters.
PORT = 8000
IMPORT_NAME = 'ryr'

# Resolver parameters.
RESOLVER_MODULE_NAME = 'api.controller'
