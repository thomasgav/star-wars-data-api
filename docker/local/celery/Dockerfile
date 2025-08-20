# ----------------------
# Base Python image
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

# Build Python wheels
RUN pip wheel --wheel-dir /usr/src/app/wheels -r ${BUILD_ENVIRONMENT}.txt

# ----------------------
# Runtime stage
FROM python AS python-run-stage

ARG BUILD_ENVIRONMENT=local
ARG APP_HOME=/app

RUN useradd -m -r appuser \
   && mkdir -p ${APP_HOME} \
   && chown -R appuser:appuser ${APP_HOME}

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    BUILD_ENV=${BUILD_ENVIRONMENT}

RUN apt-get update && apt-get install --no-install-recommends -y \
   libpq-dev \
   gettext \
   && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
   && rm -rf /var/lib/apt/lists/*

WORKDIR ${APP_HOME}

# Install built wheels
COPY --from=python-build-stage --chown=appuser:appuser /usr/src/app/wheels /wheels/
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
   && rm -rf /wheels/

RUN mkdir -p /app/staticfiles /app/mediafiles \
    && chown -R appuser:appuser /app/staticfiles /app/mediafiles

# Copy project files (Celery still needs Django settings)
COPY --chown=appuser:appuser . .

# Copy Celery entrypoint
COPY ./docker/local/celery/worker/start.sh /start-celery-worker.sh
RUN sed -i 's/\r$//g' /start-celery-worker.sh && chmod +x /start-celery-worker.sh

# COPY ./docker/local/celery/beat/start.sh /start-celery-beat.sh
# RUN sed -i 's/\r$//g' /start-celery-beat.sh && chmod +x /start-celery-beat.sh

USER appuser

ENTRYPOINT ["/bin/sh", "-c"]
