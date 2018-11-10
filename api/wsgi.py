"""Define the WSGI app."""

from api.connexion_utils import create_connexion_app

app = create_connexion_app()
application = app.app
