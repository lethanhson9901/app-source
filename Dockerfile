# Stage 1: Builder/Compiler
FROM python:3.11-slim-bookworm as builder

# Set build arguments and environment variables
ARG POETRY_VERSION=1.7.0
ARG POETRY_HOME="/opt/poetry"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=${POETRY_VERSION} \
    POETRY_HOME=${POETRY_HOME} \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

# Add Poetry to PATH
ENV PATH="${POETRY_HOME}/bin:$PATH"

# Set shell options
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry using official installer
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && poetry --version

# Create and set working directory
WORKDIR /app

# Copy only dependency files first to leverage caching
COPY pyproject.toml poetry.lock ./

# Install dependencies with poetry
RUN poetry install --only main --no-root --no-cache

# Copy source code
COPY src/ src/

# Stage 2: Runtime
FROM python:3.11-slim-bookworm

# Set labels according to OCI standard
LABEL org.opencontainers.image.title="Python FastAPI Application" \
      org.opencontainers.image.description="FastAPI application with Poetry dependency management" \
      org.opencontainers.image.version="1.0.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="/app" \
    PORT=8080 \
    TZ=UTC

# Install system dependencies and create non-root user
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq5 \
        curl \
        tini \
    && rm -rf /var/lib/apt/lists/* \
    && addgroup --system --gid 1001 appgroup \
    && adduser --system --uid 1001 --gid 1001 appuser

# Create and set working directory
WORKDIR /app

# Copy virtual environment and source code from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /app/src/ ./src/

# Copy configuration files
COPY .env.example ./.env

# Set up logging directory with correct permissions
RUN mkdir -p /app/logs \
    && chown -R appuser:appgroup /app \
    && chmod -R 550 /app \
    && chmod -R 770 /app/logs

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health/live || exit 1

# Expose port
EXPOSE ${PORT}

# Use Tini as init system
ENTRYPOINT ["/usr/bin/tini", "--"]

# Start application
CMD ["python", "-m", "uvicorn", "src.app.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8080", \
     "--proxy-headers", \
     "--forwarded-allow-ips", "*"]
