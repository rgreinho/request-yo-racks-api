Request-Yo-Racks REST API
=========================

.. image:: https://coveralls.io/repos/github/request-yo-racks/api/badge.svg?branch=master
  :target: https://coveralls.io/github/request-yo-racks/api?branch=master

A REST API for Request-Yo-Racks.

.. attention::

  Before starting, please refer to the `full setup guide`_ to ensure that your keys are configured correctly and that
  you have minikube setup properly. Once the external services are running on minikube you can move forward to the next
  steps.

Quickstart
----------

Deploy the latest release in the minikube environment:

.. code-block:: bash

  TAG=$(git describe --abbrev=0) make deploy-minikube-api deploy-minikube-celery-worker

After a few seconds, the latest release of the API server will be available at `<http://api.192.168.99.100.nip.io/>`_.

If you want to build the master branch from source, simply run:

.. code-block:: bash

  eval $(minikube docker-env)
  make build-docker deploy-minikube-api deploy-minikube-celery-worker

``make help`` will show you the available targets that will help you work on this project.

Build the documentation
-----------------------

The ``docs`` target of the ``Makefile`` helps you build the API documentation site easily:

.. code-block:: bash

  make venv
  make docs

Open it with:

.. code-block:: bash

  open docs/build/html/index.html


Setup the project
-----------------

The `full setup guide`_ provides instructions to help you set up the external services required by the project locally
(postgresql, redis) and explains how to deploy this project on a local Kubernetes cluster (Minikube).

You can also refer to the ``kubernetes`` folder of the `infra`_ project for more details about the deployment
implementation.

Required software
"""""""""""""""""

The software required to work on this project can be automatically installed (**OSX only!**) via the following command:

.. code-block:: bash

  bash <(curl -fsSL https://raw.githubusercontent.com/request-yo-racks/api/master/bootstrap/bootstrap-osx.sh)


Local development setup
-----------------------

Virtual environment
"""""""""""""""""""

Start by preparing the virtual environment for this project:

.. code-block:: bash

  cd "${RYR_PROJECT_DIR}/api"
  make venv

Flower
""""""

Flower is optional, but very convenient to monitor the Celery tasks and collect useful information for debugging them.

Deploy Flower on minikube:

.. code-block:: bash

   make deploy-minikube-flower


Once started, flower is available at `<http://flower.192.168.99.100.nip.io>`_.

API server
""""""""""

Open a terminal and start the API server:

.. code-block:: bash

   make local-django-api

This command starts a local instance of the API server, and connects it automatically to the services deployed on
minikube. The API is exposed at `<http://localhost:8000>`_. The API server will pick up your changes automatically by
performing a live reload of your code every time you update a file.


Celery worker
"""""""""""""

Open a terminal and start a celery worker:

.. code-block:: bash

   make local-celery-worker

The Celery worker will **NOT** detect any changes automatically! Therefore you will have to restart it every time you
make a change related to Celery (task, configuration, etc.)

Test your setup
"""""""""""""""

Your terminal windows should be similar to this:

.. image:: images/api+celery-worker_terminals.png


Your Flower interface should resemble this:

.. image:: images/ryr_flower_monitoring.png


Query the local API server to ensure everything works:

.. code-block:: bash

  # Health endpoint.
  curl http://localhost:8000/health

  # Places endpoint.
  curl http://localhost:8000/places/30.318673580117846,-97.72446155548096

  # Place endpoint.
  curl http://localhost:8000/place/ChIJ1XxmFaC1RIYREMC4K9RM3zo/

Test your deployment
--------------------

Once you are done with your changes, you can build a docker image and deploy the project on minikube to further test it:

.. code-block:: bash

  eval $(minikube docker-env)
  cd "${RYR_PROJECT_DIR}/api"
  make build-docker deploy-minikube-api deploy-minikube-celery-worker

.. _`docker`: https://docs.docker.com/engine/understanding-docker/
.. _`full setup guide`: https://request-yo-racks.github.io/docs/guides/setup-full-environment/
.. _`infra`: https://github.com/request-yo-racks/infra/tree/master/kubernetes
.. _`virtualbox`: https://www.virtualbox.org/
.. _`Yelp`: https://www.yelp.com/signup
.. _`Google`: https://accounts.google.com/SignUp
.. _`Yelp Fusion API`: https://www.yelp.com/developers/v3/manage_app
.. _`Google Places API`: https://developers.google.com/places/web-service
.. _`Google Geocoding API`: https://developers.google.com/maps/documentation/geocoding/get-api-key
