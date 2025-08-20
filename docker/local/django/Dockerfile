# ----------------------
# Base Python image with version
ARG PYTHON_VERSION=3.13-slim

FROM python:${PYTHON_VERSION} AS python

# ----------------------
# Build stage
FROM python AS python-build-stage

ARG BUILD_ENVIRONMENT=local

RUN apt-get update && apt-get install --no-install-recommends -y \
   build-essential \
   libpq-dev \
&& rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY ./requirements .

# Create a directory for wheels
RUN pip wheel --wheel-dir /usr/src/app/wheels -r ${BUILD_ENVIRONMENT}.txt

# ----------------------
# Production stage
FROM python AS python-run-stage

ARG BUILD_ENVIRONMENT=local
ARG APP_HOME=/app

# Create app user and set ownership (best practice for security not to run as root)
RUN useradd -m -r appuser \
   && mkdir -p ${APP_HOME} \
   && chown -R appuser:appuser ${APP_HOME}

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    BUILD_ENV=${BUILD_ENVIRONMENT}
# ENV PYTHONPATH="${PYTHONPATH}:/app/apps"

# Install only required runtime packages
RUN apt-get update && apt-get install --no-install-recommends -y \
   libpq-dev \
   gettext \
   && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
   && rm -rf /var/lib/apt/lists/*

WORKDIR ${APP_HOME}

# Copy wheels from build stage
COPY --from=python-build-stage --chown=appuser:appuser /usr/src/app/wheels /wheels/
# Install packages from wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
   && rm -rf /wheels/

RUN mkdir -p /app/staticfiles /app/mediafiles \
    && chown -R appuser:appuser /app/staticfiles /app/mediafiles

# Copy project files
COPY --chown=appuser:appuser . .

# Copy helper scripts
COPY ./docker/local/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh && chmod +x /entrypoint.sh

COPY ./docker/local/django/start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh && chmod +x /start.sh

COPY ./docker/local/celery/worker/start.sh /start-celery-worker.sh
RUN sed -i 's/\r$//g' /start-celery-worker.sh && chmod +x /start-celery-worker.sh

COPY ./docker/local/flower/start.sh /start-flower.sh
RUN sed -i 's/\r$//g' /start-flower.sh && chmod +x /start-flower.sh

USER appuser

EXPOSE 8000

ENTRYPOINT ["/bin/sh", "-c"]