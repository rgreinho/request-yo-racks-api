# Project configuration.
PROJECT_NAME = api

# Makefile parameters.
RUN ?= local
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

# Chart.
CHART_REPO = ${RYR_PROJECT_DIR}/charts/charts
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

default: setup

help: # Display help
	@awk -F ':|##' \
		'/^[^\t].+?:.*?##/ {\
			printf "\033[36m%-30s\033[0m %s\n", $$1, $$NF \
		}' $(MAKEFILE_LIST) | sort

.PHONY: build-docker
build-docker: ## Build the docker image
	@docker build -t $(DOCKER_IMG) -f $(DOCKERFILE) .

.PHONY: ci
ci: ci-format ci-linters ci-tests ci-docs ## Run all CI targets at once

.PHONY: ci-docs
ci-docs: ## Ensure the documentation builds
	$(RUN_CMD) tox -e docs

.PHONY: ci-format
ci-format: ## Check the code formatting using YAPF
	$(RUN_CMD) tox -e format-check

.PHONY: ci-linters
ci-linters: ## Run the static analyzers
	$(RUN_CMD) tox -e flake8,pydocstyle,pylint

.PHONY: ci-tests
ci-tests: ## Run the unit tests
	$(RUN_CMD) tox

.PHONY: clean
clean: clean-repo clean-minikube clean-docker  ## Clean everything (!DESTRUCTIVE!)

.PHONY: clean-docker
clean-docker: ## Remove all docker artifacts for this project (!DESTRUCTIVE!)
	@docker image rm -f $(shell docker image ls --filter reference='$(DOCKER_REPO)' -q) || true

.PHONY: clean-minikube
clean-minikube: ## Remove all the Kubernetes objects associated to this project (!DESTRUCTIVE!)
	@helm --kube-context minikube delete --purge $(PROJECT_NAME) || true

.PHONY: clean-repo
clean-repo: ## Remove unwanted files in project (!DESTRUCTIVE!)
	@cd $(TOPDIR) && git clean -ffdx && git reset --hard

.PHONY: deploy-minikube-api
deploy-minikube-api: ## Deploy the API on Minikube
	cd charts \
	&& helm upgrade $(PROJECT_NAME) $(CHART_NAME) \
		--kube-context minikube \
	  --install \
		-f values.common.yaml \
		-f values.minikube.yaml \
	  --set image.tag=$(TAG)

.PHONY: deploy-minikube-celery-worker
deploy-minikube-celery-worker: ## Deploy the API on Minikube
	cd charts/celery-worker \
	&& helm upgrade celery-worker $(CHART_REPO)/celery-worker \
		--kube-context minikube \
	  --install \
		-f values.common.yaml \
		-f values.minikube.yaml \
	  --set image.tag=$(TAG)

.PHONY: deploy-minikube-flower
deploy-minikube-flower: ## Deploy Flower on Minikiube
	helm upgrade flower ryr/flower \
		--kube-context minikube \
		--install \
		--version 0.1.0

.PHONY: deploy-prod-api
deploy-prod-api: ## Deploy the API in production
	cd charts \
	&& helm upgrade $(PROJECT_NAME) $(CHART_NAME) \
		--kube-context gke_request-yo-racks-1499134244211_us-central1-a_ryr-prod \
	  --install \
		--version 0.2.5 \
		-f values.common.yaml \
		-f values.prod.yaml \
	  --set image.tag=$(TAG)

.PHONY: dist
dist: wheel ## Package the application

.PHONY: docs
docs: ## Build documentation
	$(RUN_CMD) tox -e docs

.PHONY: format
format: ## Format the codebase using YAPF
	$(RUN_CMD) tox -e format

.PHONY: local-envvars
local-envvars: ## Setup Django environment variables for this project
	@bash tools/kubernetes-local-env-vars.sh

.PHONY: local-celery-worker
local-celery-worker: ## Start a local celery worker
	source $(HOME)/.config/ryr/ryr-env.sh \
		&& export RYR_LOG_LEVEL=info \
		&& eval $$(tools/kubernetes-local-env-vars.sh) \
		&& $(LOCAL_RUN_CMD) docker/docker-entrypoint.sh celery worker

.PHONY: local-api
local-api: ## Run connexion locally
	source $(HOME)/.config/ryr/ryr-env.sh \
		&& export CONNEXION_SETTINGS_MODULE=api.settings.local \
		&& export RYR_API_API_OPTS="--reload --timeout 1800" \
		&& export RYR_LOG_LEVEL=info \
		&& eval $$(tools/kubernetes-local-env-vars.sh) \
		&& $(LOCAL_RUN_CMD) docker/docker-entrypoint.sh api

.PHONY: setup
setup: venv build-docker ## Setup the full environment (default)

venv: venv/bin/activate ## Setup local venv

venv/bin/activate: requirements.txt
	test -d venv || python3 -m venv venv || virtualenv --no-setuptools --no-wheel -p python3 venv
	. venv/bin/activate \
		&& pip install --upgrade pip setuptools \
		&& pip install -U -r requirements.txt \
		&& pip install -r requirements-dev.txt \
		&& pip install -e .

.PHONY: wheel
wheel: ## Build a wheel package
	$(RUN_CMD) tox -e wheel
