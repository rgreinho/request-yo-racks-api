"""Define the endpoint for the place resource."""
import dataclasses

from connexion.lifecycle import ConnexionResponse

from api.celery.tasks import collect_place_details


def post(body):
    """Provide detailed information about a specific place."""
    result = collect_place_details(
        body['place_id'],
        body['name'],
        body['address'],
    )
    return ConnexionResponse(body=dataclasses.asdict(result))
