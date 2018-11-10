"""Define utilities to create and configure a connexion app."""

import os
import sys

import connexion
from connexion.resolver import RestyResolver


def import_string(import_name):
    """
    Import an object based on a string.

    This is useful if you want to
    use import paths as endpoints or something similar.  An import path can
    be specified either in dotted notation (``xml.sax.saxutils.escape``)
    or with a colon as object delimiter (``xml.sax.saxutils:escape``).
    If `silent` is True the return value will be `None` if the import fails.
    :param import_name: the dotted name for the object to import.
    :param silent: if set to `True` import errors are ignored and
        `None` is returned instead.
    :return: imported object
    """
    # force the import name to automatically convert to strings
    # __import__ is not able to handle unicode strings in the fromlist
    # if the module is a package
    import_name = str(import_name).replace(':', '.')
    try:
        try:
            __import__(import_name)
        except ImportError:
            if '.' not in import_name:
                raise
        else:
            return sys.modules[import_name]

        module_name, obj_name = import_name.rsplit('.', 1)
        try:
            module = __import__(module_name, None, None, [obj_name])
        except ImportError:
            # support importing modules not yet set up by the parent module
            # (or package for that matter)
            module = import_string(module_name)

        try:
            return getattr(module, obj_name)
        except AttributeError as e:
            raise ImportError(e)

    except ImportError as e:
        raise e


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
    d = {}
    if isinstance(obj, str):
        obj = import_string(obj)
    for key in dir(obj):
        if key.isupper():
            d[key] = getattr(obj, key)

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

    app.add_api(settings['SPECIFICATION_FILE'], resolver=RestyResolver(settings['RESOLVER_MODULE_NAME']))
    return app
