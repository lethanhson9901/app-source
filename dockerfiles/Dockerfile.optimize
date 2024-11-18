# Stage 1: Builder/Compiler
FROM python:3.11-slim-bullseye as builder

# Set build-time arguments and environment variables
ARG POETRY_VERSION=1.7.0
ARG POETRY_HOME="/opt/poetry"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=${POETRY_VERSION} \
    POETRY_HOME=${POETRY_HOME} \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="${POETRY_HOME}/bin:$PATH" \
    PYTHONPATH="/app"

# Install system dependencies and Poetry in a single layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        build-essential \
        libpq-dev && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apt-get purge -y --auto-remove build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app

# Copy only dependency files first
COPY --chown=root:root pyproject.toml poetry.lock ./

# Install dependencies with explicit version pinning
RUN poetry install --only main --no-root \
    && find /usr/local -type d -name __pycache__ -exec rm -rf {} + \
    && rm -rf ~/.cache/pip ~/.cache/poetry

# Copy source code
COPY --chown=root:root src/ src/

# Stage 2: Runtime
FROM python:3.11-slim-bullseye

# Set runtime arguments and environment variables
ARG PORT=8080
ARG APP_USER=appuser
ARG APP_GROUP=appgroup
ARG UID=1001
ARG GID=1001

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="/app" \
    PORT=${PORT} \
    PATH="/usr/local/bin:$PATH"

# Install runtime dependencies and create user in a single layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq5 \
        curl \
        tini && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    groupadd -r -g ${GID} ${APP_GROUP} && \
    useradd -r -g ${APP_GROUP} -u ${UID} ${APP_USER} && \
    mkdir -p /app/logs && \
    chown -R ${APP_USER}:${APP_GROUP} /app

WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder --chown=${APP_USER}:${APP_GROUP} /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder --chown=${APP_USER}:${APP_GROUP} /app/src/ ./src/
COPY --chown=${APP_USER}:${APP_GROUP} .env.example ./.env

# Set secure permissions
RUN chmod -R 550 /app && \
    chmod -R 770 /app/logs && \
    chmod 640 .env

# Switch to non-root user
USER ${APP_USER}:${APP_GROUP}

# Health check with timeout
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health/live || exit 1

# Use tini as init system
ENTRYPOINT ["/usr/bin/tini", "--"]

# Expose port
EXPOSE ${PORT}

# Start application with optimized settings
CMD ["python", "-m", "uvicorn", \
    "src.app.main:app", \
    "--host", "0.0.0.0", \
    "--port", "8080", \
    "--proxy-headers", \
    "--forwarded-allow-ips", "*", \
    "--workers", "4", \
    "--access-log"]
