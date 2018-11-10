"""Define the endpoint for the health resource."""
from connexion.lifecycle import ConnexionResponse


def search():
    """Provide server status information."""
    content = {'status': 'ok'}
    return ConnexionResponse(body=content)
