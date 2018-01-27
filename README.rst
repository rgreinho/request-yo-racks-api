Request-Yo-Racks REST API
=========================

A REST API for Request-Yo-Racks.

Quickstart
----------

Install `docker`_.

Setup the full environment::

  make

This will setup a local virtual environment for this project, as well as build the corresponding docker image.

``make help`` will show you the available targets that will help you work on this project.

The `full setup guide`_ provides instructions to help you set up the external services required by the project locally
(postgresql, rabbitmq, redis) and explains how to deploy this project on a local Kubernetes cluster (Minikube).
You can also refer to the ``kubernetes`` folder of the `infra`_ project for more details about the implementation.

The ``make django-debug`` command will start a local instance of this project, connecting automatically to the external
services deployed on minikube.

.. _`docker`: https://docs.docker.com/engine/understanding-docker/
.. _`full setup guide`: https://request-yo-racks.github.io/docs/guides/setup-full-environment/
.. _`infra`: https://github.com/request-yo-racks/infra/tree/master/kubernetes
