# Project configuration.
PROJECT_NAME = api

# Makefile parameters.
RUN ?= docker
SUFFIX ?= .dev
TAG ?= $(shell git describe)$(SUFFIX)

# General.
SHELL = /bin/bash
TOPDIR = $(shell git rev-parse --show-toplevel)

# Docker.
DOCKER_ORG = requestyoracks
REPOSITORY = $(DOCKER_ORG)/$(PROJECT_NAME)
DOCKER_IMG = $(REPOSITORY):$(TAG)
DOCKERFILE = Dockerfile$(SUFFIX)
DOCKER_IMAGE_COALA = coala/base:0.11

# Chart.
CHART_REPO = ryr
CHART_NAME = $(CHART_REPO)/$(PROJECT_NAME)

# Docker run command.
DOCKER_RUN_CMD = docker run -t -v=$$(pwd):/code --rm $(DOCKER_IMG)

# Determine whether running the command in a container or locally.
ifeq ($(RUN),docker)
  RUN_CMD = $(DOCKER_RUN_CMD)
else
  RUN_CMD = source venv/bin/activate &&
endif

# Docker compose run generic parameters.
# DOCKER_COMPOSE_RUN_CMD = docker-compose run
# DOCKER_COMPOSE_RUN_OPTS = --no-deps --rm
# DOCKER_COMPOSE_RUN_SVC = ryr-api-django
# DOCKER_COMPOSE_RUN_FULL = $(DOCKER_COMPOSE_RUN_CMD) $(DOCKER_COMPOSE_RUN_OPTS) $(DOCKER_COMPOSE_RUN_SVC)
# DOCKER_DB_CONTAINER = ryr-api-db

# Docker compose run Django parameters.
# DOCKER_COMPOSE_RUN_DJANGO_MANAGE_CMD = python manage.py
# DOCKER_COMPOSE_RUN_DJANGO_FULL = $(DOCKER_COMPOSE_RUN_CMD) $(DOCKER_COMPOSE_RUN_DJANGO_OPTS) $(DOCKER_COMPOSE_RUN_SVC) $(DOCKER_COMPOSE_RUN_DJANGO_MANAGE_CMD)

default: setup

help: # Display help
	@awk -F ':|##' \
		'/^[^\t].+?:.*?##/ {\
			printf "\033[36m%-30s\033[0m %s\n", $$1, $$NF \
		}' $(MAKEFILE_LIST) | sort

ci-all: ci-linters ci-tests ci-docs ## Run all CI targets at once

ci-linters: ## Run the static analyzers
	@docker pull $(DOCKER_IMAGE_COALA)
	@docker run --rm -t -v=$$(pwd):/app --workdir=/app $(DOCKER_IMAGE_COALA) coala --ci

ci-docs: ## Ensure the documentation builds
	$(RUN_CMD) tox -e docs

ci-tests: ## Run the unit tests
	$(RUN_CMD) tox

clean: ## Remove unwanted files in project (!DESTRUCTIVE!)
	@cd $(TOPDIR) && git clean -ffdx && git reset --hard

clean-all: clean clean-docker clean-minikube ## Clean everything (!DESTRUCTIVE!)

clean-docker: ## Remove all docker artifacts for this project (!DESTRUCTIVE!)
	@docker image rm -f $(shell docker image ls --filter reference='$(REPOSITORY)' -q)

clean-minikube: ## Remove all the Kubernetes objects associated to this project
	@helm delete --purge $(PROJECT_NAME)

django-dbup: # Ensure Django DB is up and runnig
	@docker-compose up -d $(DOCKER_DB_CONTAINER);
	$(DOCKER_COMPOSE_RUN_CMD) $(DOCKER_COMPOSE_RUN_DJANGO_OPTS) $(DOCKER_DB_CONTAINER) bash -c "until psql -h \"$(DOCKER_DB_CONTAINER)\" -U \"postgres\" -c '\l' >/dev/null 2>&1; do sleep 1; done"

django-debug: django-dbup ## Run Django in a way allowing the use of PDB
	$(DOCKER_COMPOSE_RUN_CMD) --rm --service-ports $(DOCKER_COMPOSE_RUN_SVC)

django-migrate: django-dbup ## Run the Django migrations
	$(DOCKER_COMPOSE_RUN_DJANGO_FULL) migrate

django-make-migrations: django-dbup ## Prepare the Django migrations
	$(DOCKER_COMPOSE_RUN_DJANGO_FULL) makemigrations

django-shell: django-dbup ## Run the Django Shell
	$(DOCKER_COMPOSE_RUN_DJANGO_FULL) shell

django-superuser: django-dbup ## Create the Django super user
	$(DOCKER_COMPOSE_RUN_DJANGO_FULL) createsuperuser

deploy-minikube:
	cd charts \
	&& helm upgrade $(PROJECT_NAME) $(CHART_NAME) \
	  --install \
		-f values.minikube.yaml \
	  --set image.tag=$(TAG) \
		--set persistence.hostPath.path=$(PWD)

dist: wheel ## Package the application

docker-build: ## Build the docker image
	@docker build -t $(DOCKER_IMG) -f $(DOCKERFILE) .

docs: ## Build documentation
	$(RUN_CMD) tox -e docs

format: ## Format the codebase using YAPF
	$(RUN_CMD) tox -e format

format-check: ## Check the code formatting using YAPF
	$(RUN_CMD) tox -e format-check

setup: docker-build ## Setup the full environment (default)

venv: venv/bin/activate ## Setup local venv

venv/bin/activate: requirements.txt
	test -d venv || virtualenv --no-setuptools --no-wheel -p python3 venv || python3 -m venv venv
	. venv/bin/activate \
		&& pip install -U pip==9.0.1 setuptools==38.4.0 \
		&& pip install -e .[docs,local,testing]

wheel: ## Build a wheel package
	$(RUN_CMD) tox -e wheel

.PHONY: ci-all ci-docs ci-tests ci-linters clean-all clean clean-docker clean-minikube dist django-migrate django-make-migrations django-shell django-superuser docker-build docs format format-check setup wheel
