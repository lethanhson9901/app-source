# # Dockerfile.multistage
# FROM python:3.11-slim as builder

# WORKDIR /app
# ENV PYTHONPATH=/app

# # Install poetry and dependencies
# RUN pip install poetry
# COPY pyproject.toml poetry.lock ./
# RUN poetry export -f requirements.txt --output requirements.txt

# # Runtime stage
# FROM python:3.11-slim

# WORKDIR /app
# ENV PYTHONPATH=/app
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# # Create non-root user
# RUN adduser --disabled-password --gecos '' appuser && \
#     apt-get update && \
#     apt-get install -y --no-install-recommends curl && \
#     rm -rf /var/lib/apt/lists/*

# # Install dependencies
# COPY --from=builder /app/requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy application
# COPY src/ .

# # Security: Set ownership and permissions
# RUN chown -R appuser:appuser /app
# USER appuser

# HEALTHCHECK --interval=30s --timeout=3s \
#     CMD curl -f http://localhost:8080/health/live || exit 1

# EXPOSE 8080
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
