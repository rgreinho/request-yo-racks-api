FROM python:3.7.1-slim-stretch as builder
MAINTAINER Rémy Greinhofer <remy.greinhofer@requestyoracks.org>

# Install packages.
RUN apt-get update \
  && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  git \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Switch to the directory containing the code.
WORKDIR /usr/src/app

# Copy the code base.
COPY . .

# Build the packages.
RUN rm -fr dist \
  && python setup.py bdist_wheel

###
# Create the release image.
FROM python:3.7.1-slim-stretch
MAINTAINER Rémy Greinhofer <remy.greinhofer@requestyoracks.org>

# Copy the package and install it.
WORKDIR /usr/src/app
COPY --from=builder /usr/src/app/dist /usr/src/app

RUN apt-get update \
  && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  git \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
  && pip install -U git+https://github.com/celery/celery.git@master#egg=celery \
  # The commands above are part of a hack to install Celery from the master branch in order to be able run it with
  # Python 3.7. Once Celery 4.3 or 5 gets released, they could be safely removed.
  && pip install --no-cache-dir api-*-py3-none-any.whl

# Copy entry point.
COPY docker/docker-entrypoint.sh /

# Set entrypoint.
ENTRYPOINT ["/docker-entrypoint.sh"]
