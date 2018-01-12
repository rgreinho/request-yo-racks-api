# General.
SHELL = /bin/bash
TOPDIR = $(shell git rev-parse --show-toplevel)
TAG ?= $(shell git describe)

# Docker.
DOCKER_NETWORK = ryr
DOCKER_ORG = requestyoracks
DOCKER_SVC = api
DOCKER_IMAGE_COALA = coala/base:0.11

# Docker compose run generic parameters.
DOCKER_COMPOSE_RUN_CMD = docker-compose run
DOCKER_COMPOSE_RUN_OPTS = --no-deps --rm
DOCKER_COMPOSE_RUN_SVC = ryr-api-django
DOCKER_COMPOSE_RUN_FULL = $(DOCKER_COMPOSE_RUN_CMD) $(DOCKER_COMPOSE_RUN_OPTS) $(DOCKER_COMPOSE_RUN_SVC)
DOCKER_DB_CONTAINER = ryr-api-db

# Docker compose run Django parameters.
DOCKER_COMPOSE_RUN_DJANGO_MANAGE_CMD = python manage.py
DOCKER_COMPOSE_RUN_DJANGO_FULL = $(DOCKER_COMPOSE_RUN_CMD) $(DOCKER_COMPOSE_RUN_DJANGO_OPTS) $(DOCKER_COMPOSE_RUN_SVC) $(DOCKER_COMPOSE_RUN_DJANGO_MANAGE_CMD)

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
	$(DOCKER_COMPOSE_RUN_FULL) tox -e docs

ci-tests: ## Run the unit tests
	$(DOCKER_COMPOSE_RUN_FULL) tox

clean: ## Remove unwanted files in project (!DESTRUCTIVE!)
	cd $(TOPDIR) && git clean -ffdx

clean-minikube: ## Remove minikube deployment (!DESTRUCTIVE!)
	helm delete --purge api

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
	&& helm upgrade api ryr/api \
	  --install \
		-f values.minikube.yaml \
	  --set image.tag=$(TAG) \
		--set persistence.hostPath.path=$(PWD)

dist: ## Package the application
	@echo "Not implemented yet."

docker-build: ## Build the docker image
	@docker build -t $(DOCKER_ORG)/$(DOCKER_SVC):$(TAG) -f Dockerfile.dev .

docker-clean: ## Stop and remove containers, volumes, networks and images for this project (!DESTRUCTIVE!)
	@docker-compose down --rmi local -v
	@docker network prune -f

docker-network: ## Create a Loannister bridge network
	FOUND=$$(docker network ls -f name=^$(DOCKER_NETWORK)$$ -q); \
	if [ -z "$$FOUND" ]; then \
		docker network create --driver bridge $(DOCKER_NETWORK); \
	fi

docs: ## Build documentation
	$(DOCKER_COMPOSE_RUN_FULL) sphinx-build -b html -d docs/build/doctrees docs/source/ docs/build/html

format: ## Format the codebase using YAPF
	$(DOCKER_COMPOSE_RUN_FULL) yapf -r -i .

format-check: ## Check the code formatting using YAPF
	$(DOCKER_COMPOSE_RUN_FULL) exit `yapf -d -r . | wc -l | tr -s ' '

setup: docker-network ## Setup the full environment (default)
	@docker-compose build
	@docker-compose pull

venv: venv/bin/activate ## Setup local venv

venv/bin/activate: requirements.txt
	test -d venv || python3 -m venv venv
	. venv/bin/activate && pip install -U pip==9.0.1 setuptools==38.4.0 && pip install -e .[docs,local,testing]

wheel: ## Build a wheel package
	$(DOCKER_COMPOSE_RUN_FULL) python setup.py bdist_wheel

.PHONY: ci-coala ci-docs ci-tests clean django-migrate django-make-migrations django-shell django-superuser docker-clean docker-network docs format format-check setup wheel
