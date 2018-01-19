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
DOCKERFILE = Dockerfile$(SUFFIX)
DOCKER_ORG = requestyoracks
DOCKER_REPO = $(DOCKER_ORG)/$(PROJECT_NAME)
DOCKER_IMG = $(DOCKER_REPO):$(TAG)
DOCKER_IMG_COALA = coala/base:0.11

# Chart.
CHART_REPO = ryr
CHART_NAME = $(CHART_REPO)/$(PROJECT_NAME)

# Docker run command.
DOCKER_RUN_CMD = docker run --rm -t -v=$$(pwd):/code $(DOCKER_IMG)

# Determine whether running the command in a container or locally.
ifeq ($(RUN),docker)
  RUN_CMD = $(DOCKER_RUN_CMD)
else
  RUN_CMD = source venv/bin/activate &&
endif

# Docker run Django parameters.
RUN_DJANGO_MANAGE_CMD = $(RUN_CMD) python manage.py

default: setup

help: # Display help
	@awk -F ':|##' \
		'/^[^\t].+?:.*?##/ {\
			printf "\033[36m%-30s\033[0m %s\n", $$1, $$NF \
		}' $(MAKEFILE_LIST) | sort

build-docker: ## Build the docker image
	@docker build -t $(DOCKER_IMG) -f $(DOCKERFILE) .

ci: ci-linters ci-tests ci-docs ## Run all CI targets at once

ci-docs: ## Ensure the documentation builds
	$(RUN_CMD) tox -e docs

ci-format: ## Check the code formatting using YAPF
	$(RUN_CMD) tox -e format-check

ci-linters: ## Run the static analyzers
	@docker pull $(DOCKER_IMG_COALA)
	@docker run --rm -t -v=$$(pwd):/app --workdir=/app $(DOCKER_IMG_COALA) coala --ci

ci-tests: ## Run the unit tests
	$(RUN_CMD) tox

clean: clean-repo clean-minikube clean-docker  ## Clean everything (!DESTRUCTIVE!)

clean-docker: ## Remove all docker artifacts for this project (!DESTRUCTIVE!)
	@docker image rm -f $(shell docker image ls --filter reference='$(DOCKER_REPO)' -q)

clean-minikube: ## Remove all the Kubernetes objects associated to this project (!DESTRUCTIVE!)
	@helm delete --purge $(PROJECT_NAME)

clean-repo: ## Remove unwanted files in project (!DESTRUCTIVE!)
	@cd $(TOPDIR) && git clean -ffdx && git reset --hard

django-debug: ## Run Django in a way allowing the use of PDB
	@echo "Needs to be reimplemented."
	# $(RUN_DJANGO_MANAGE_CMD) --rm --service-ports $(DOCKER_COMPOSE_RUN_SVC)

django-migrate: ## Run the Django migrations
	@echo "Needs to be reimplemented."
	# $(RUN_DJANGO_MANAGE_CMD) migrate

django-make-migrations: ## Prepare the Django migrations
	$(RUN_DJANGO_MANAGE_CMD) makemigrations

django-shell: ## Run the Django Shell
	$(RUN_DJANGO_MANAGE_CMD) shell

django-superuser: ## Create the Django super user
	@echo "Needs to be reimplemented."
	# $(RUN_DJANGO_MANAGE_CMD) createsuperuser

deploy-minikube:
	cd charts \
	&& helm upgrade $(PROJECT_NAME) $(CHART_NAME) \
	  --install \
		-f values.minikube.yaml \
	  --set image.tag=$(TAG) \
		--set persistence.hostPath.path=$(PWD)

dist: wheel ## Package the application

docs: ## Build documentation
	$(RUN_CMD) tox -e docs

format: ## Format the codebase using YAPF
	$(RUN_CMD) tox -e format

setup: docker-build ## Setup the full environment (default)

venv: venv/bin/activate ## Setup local venv

venv/bin/activate: requirements.txt
	test -d venv || virtualenv --no-setuptools --no-wheel -p python3 venv || python3 -m venv venv
	. venv/bin/activate \
		&& pip install -U pip==9.0.1 setuptools==38.4.0 \
		&& pip install -e .[docs,local,testing]

wheel: # Build a wheel package
	$(RUN_CMD) tox -e wheel

.PHONY: ci ci-format ci-linters ci-docs ci-tests clean clean-docker clean-minikube clean-repo dist django-migrate django-make-migrations django-shell django-superuser docker-build docs format setup wheel
