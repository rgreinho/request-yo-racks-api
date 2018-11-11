"""
Define the REST API server.

This was done to help transitionning to `connexion` and may be deleted at some point in the future.
To launch the server locally, use the `make local-api` command instead.
"""

from api.connexion_utils import create_connexion_app

if __name__ == '__main__':
    app = create_connexion_app()
    app.run()
