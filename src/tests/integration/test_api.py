# # src/tests/integration/test_api.py
# import pytest
# from httpx import AsyncClient
# from ...app.main import app
# from ...app.config import settings

# @pytest.mark.asyncio
# async def test_get_items():
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         response = await ac.get(
#             "/api/v1/items",
#             headers={"X-API-Key": settings.API_KEY}
#         )
#         assert response.status_code == 200
#         assert isinstance(response.json(), list)

# ---

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

# # deployments/helm/python-app/Chart.yaml
# apiVersion: v2
# name: python-app
# description: A Python application with best practices
# version: 0.1.0
# appVersion: "1.0.0"
# dependencies:
#   - name: postgresql
#     version: 12.x.x
#     repository: https://charts.bitnami.com/bitnami
#     condition: postgresql.enabled
#   - name: redis
#     version: 17.x.x
#     repository: https://charts.bitnami.com/bitnami
#     condition: redis.enabled

# # deployments/helm/python-app/values.yaml
# replicaCount: 2

# image:
#   repository: ghcr.io/username/python-app
#   tag: latest
#   pullPolicy: Always

# nameOverride: ""
# fullnameOverride: ""

# serviceAccount:
#   create: true
#   annotations: {}
#   name: ""

# podSecurityContext:
#   fsGroup: 1000

# securityContext:
#   capabilities:
#     drop:
#     - ALL
#   readOnlyRootFilesystem: true
#   runAsNonRoot: true
#   runAsUser: 1000

# service:
#   type: ClusterIP
#   port: 80

# ingress:
#   enabled: true
#   className: nginx
#   annotations:
#     cert-manager.io/cluster-issuer: letsencrypt-prod
#   hosts:
#     - host: app.example.com
#       paths:
#         - path: /
#           pathType: Prefix

# resources:
#   limits:
#     cpu: 500m
#     memory: 512Mi
#   requests:
#     cpu: 200m
#     memory: 256Mi

# autoscaling:
#   enabled: true
#   minReplicas: 2
#   maxReplicas: 10
#   targetCPUUtilizationPercentage: 80
#   targetMemoryUtilizationPercentage: 80

# nodeSelector: {}
# tolerations: []
# affinity: {}

# postgresql:
#   enabled: true
#   auth:
#     username: appuser
#     database: appdb
#   primary:
#     persistence:
#       size: 10Gi

# redis:
#   enabled: true
#   auth:
#     enabled: true
#   master:
#     persistence:
#       size: 5Gi

# # deployments/helm/python-app/values.schema.json
# {
#   "$schema": "https://json-schema.org/draft-07/schema",
#   "type": "object",
#   "required": ["image", "replicaCount"],
#   "properties": {
#     "image": {
#       "type": "object",
#       "required": ["repository", "tag"],
#       "properties": {
#         "repository": {
#           "type": "string"
#         },
#         "tag": {
#           "type": "string"
#         },
#         "pullPolicy": {
#           "type": "string",
#           "enum": ["Always", "IfNotPresent", "Never"]
#         }
#       }
#     },
#     "replicaCount": {
#       "type": "integer",
#       "minimum": 1
#     }
#   }
# }

# # deployments/helm/python-app/templates/deployment.yaml
# apiVersion: apps/v1
# kind: Deployment
# metadata:
#   name: {{ include "python-app.fullname" . }}
#   labels:
#     {{- include "python-app.labels" . | nindent 4 }}
# spec:
#   {{- if not .Values.autoscaling.enabled }}
#   replicas: {{ .Values.replicaCount }}
#   {{- end }}
#   selector:
#     matchLabels:
#       {{- include "python-app.selectorLabels" . | nindent






