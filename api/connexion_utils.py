"""Define utilities to create and configure a connexion app."""

import os

import connexion
from connexion.resolver import RestyResolver
from flask_cors import CORS
from werkzeug.utils import import_string

from api.connexion_redoc import add_redoc_route


def from_object(obj):
    """
    Update the values from the given object.

    An object can be of one of the following two types:
    -   a string: in this case the object with that name will be imported
    -   an actual object reference: that object is used directly
    Objects are usually either modules or classes. :meth:`from_object`
    loads only the uppercase attributes of the module/class. A ``dict``
    object will not work with :meth:`from_object` because the keys of a
    ``dict`` are not attributes of the ``dict`` class.
    Example of module-based configuration::
        app.config.from_object('yourapplication.default_config')
        from yourapplication import default_config
        app.config.from_object(default_config)
    You should not use this function to load the actual configuration but
    rather configuration defaults.  The actual config should be loaded
    with :meth:`from_pyfile` and ideally from a location not within the
    package because the package might be installed system wide.
    See :ref:`config-dev-prod` for an example of class-based configuration
    using :meth:`from_object`.
    :param obj: an import name or object
    """
    obj = import_string(obj)
    d = {key: getattr(obj, key) for key in dir(obj) if key.isupper()}
    return d


def create_connexion_app():
    """Create and configure a connexion app."""
    settings_module = os.environ['CONNEXION_SETTINGS_MODULE']
    settings = from_object(settings_module)

    app_options = {
        'import_name': __name__,
        'port': settings['PORT'],
        'specification_dir': settings['SPECIFICATION_DIR'],
        'debug': settings['DEBUG']
    }
    app = connexion.FlaskApp(**app_options)

    # Add the specification file.
    app.add_api(settings['SPECIFICATION_FILE'], resolver=RestyResolver(settings['RESOLVER_MODULE_NAME']))

    # Add an extra route to for redoc.
    openapi_json_url = "http://0.0.0.0:8000/1.0/openapi.json"
    add_redoc_route(app, openapi_json_url)

    # Add CORS support.
    CORS(app.app)

    return app
