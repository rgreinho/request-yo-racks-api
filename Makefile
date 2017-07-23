# Project configuration.
PROJECT_NAME = api

# Makefile parameters.
RUN ?= docker
SUFFIX ?=
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

# Run commands.
DOCKER_RUN_CMD = docker run --rm -t -v=$$(pwd):/code $(DOCKER_IMG)
LOCAL_RUN_CMD = source venv/bin/activate &&

# Determine whether running the command in a container or locally.
ifeq ($(RUN),docker)
  RUN_CMD = $(DOCKER_RUN_CMD)
else
  RUN_CMD = $(LOCAL_RUN_CMD)
endif

# Docker run Django parameters.
DJANGO_MANAGE_CMD = python manage.py
RUN_DJANGO_MANAGE_CMD = $(RUN_CMD) $(DJANGO_MANAGE_CMD)

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

django-debug: django-envvars ## Run Django in a way allowing the use of PDB
	source $(HOME)/.config/ryr/ryr-env.sh \
		&& export DJANGO_SETTINGS_MODULE=api.settings.local \
		&& $(LOCAL_RUN_CMD) $(DJANGO_MANAGE_CMD) runserver 0.0.0.0:8000

django-envvars: ## Setup Django environment variables for this project
	@bash tools/kubernetes-django-env-vars.sh

django-migrate: ## Run the Django migrations
	@bash tools/kubernetes-django-manage.sh migrate

django-make-migrations: ## Prepare the Django migrations
	@bash tools/kubernetes-django-manage.sh makemigrations

django-shell: ## Run the Django Shell
	@bash tools/kubernetes-django-manage.sh shell

django-superuser: ## Create the Django super user
	@bash tools/kubernetes-django-manage.sh createsuperuser \
		--username admin\
		--email admin@requestyoracks.com

deploy-minikube: ## Deploy the API on Minikube
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

setup: venv build-docker ## Setup the full environment (default)

venv: venv/bin/activate ## Setup local venv

venv/bin/activate: requirements.txt
	test -d venv || virtualenv --no-setuptools --no-wheel -p python3 venv || python3 -m venv venv
	. venv/bin/activate \
		&& pip install -U pip==9.0.1 setuptools==38.4.0 \
		&& pip install -e .[docs,local,testing]

wheel: # Build a wheel package
	$(RUN_CMD) tox -e wheel

.PHONY: build-docker ci ci-format ci-linters ci-docs ci-tests clean clean-docker clean-minikube clean-repo dist django-migrate django-make-migrations django-shell django-superuser docs format setup wheel
