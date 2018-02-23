Request-Yo-Racks REST API
=========================

A REST API for Request-Yo-Racks.

Quickstart
----------

Setup the full environment::

  make

This will setup a local virtual environment for this project, as well as build the corresponding docker image.

``make help`` will show you the available targets that will help you work on this project.


Setup the project
-----------------

The `full setup guide`_ provides instructions to help you set up the external services required by the project locally
(postgresql, rabbitmq, redis) and explains how to deploy this project on a local Kubernetes cluster (Minikube).
You can also refer to the ``kubernetes`` folder of the `infra`_ project for more details about the deployment
implementation.

Account and developer keys
""""""""""""""""""""""""""

You will need:

* A `Yelp`_ account
* A `Google`_ account

Then create the developer keys for:

* `Yelp Fusion API`_
* `Google Places API`_
* `Google Geocoding API`_

Environment variables
"""""""""""""""""""""

Once your accounts are setup, store your developer keys in a global environment file. This file should be located in `~/.config/ryr`, which is your configuration directory for the request-yo-racks project::

  RYR_GLOBAL_CONFIG_DIR="${HOME}/.config/ryr"
  mkdir -p "${RYR_GLOBAL_CONFIG_DIR}"
  cat << EOF > "${RYR_GLOBAL_CONFIG_DIR}/ryr-env.sh"
  export RYR_COLLECTOR_YELP_CLIENT_ID=<redacted>
  export RYR_COLLECTOR_YELP_CLIENT_SECRET=<redacted>
  export RYR_COLLECTOR_GOOGLE_PLACES_API_KEY=<redacted>
  export RYR_COLLECTOR_GOOGLE_GEOCODING_API_KEY=<redacted>
  EOF
  chmod 400 "${RYR_GLOBAL_CONFIG_DIR}/ryr-env.sh"

Setup
"""""

Install `docker`_, and `virtualbox`_::

  brew cask install docker virtualbox

Setup a directory to store the RYR projects::

  export RYR_PROJECT_DIR="${HOME}/projects/request-yo-racks"

Clone the projects::

  mkdir -p "${RYR_PROJECT_DIR}"
  cd "${RYR_PROJECT_DIR}"
  for project in api infra; do
    git clone git@github.com:request-yo-racks/${project}.git
  done

Install the services required by the API on minikube::

  cd "${RYR_PROJECT_DIR}/infra/kubernetes"
  make provision configure

Prepare your developement environment::

  eval $(minikube docker-env)
  cd "${RYR_PROJECT_DIR}/api"
  make setup deploy-minikube

Local developement
------------------

The ``make django-debug`` command will start a local instance of this project, and connect it automatically to the
services deployed on minikube.

.. _`docker`: https://docs.docker.com/engine/understanding-docker/
.. _`full setup guide`: https://request-yo-racks.github.io/docs/guides/setup-full-environment/
.. _`infra`: https://github.com/request-yo-racks/infra/tree/master/kubernetes
.. _`virtualbox`: https://www.virtualbox.org/
.. _`Yelp`: https://www.yelp.com/signup
.. _`Google`: https://accounts.google.com/SignUp
.. _`Yelp Fusion API`: https://www.yelp.com/developers/v3/manage_app
.. _`Google Places API`: https://developers.google.com/places/web-service
.. _`Google Geocoding API`: https://developers.google.com/maps/documentation/geocoding/get-api-key
