# Python FastAPI Application with CI/CD Pipeline

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.0-green.svg)](https://fastapi.tiangolo.com/)
[![Poetry](https://img.shields.io/badge/Poetry-1.7.0-blue.svg)](https://python-poetry.org/)
[![Docker](https://img.shields.io/badge/Docker-24.0.7-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A production-ready Python FastAPI application with a complete CI/CD pipeline, implementing industry best practices for modern cloud-native applications.

## 🌟 Features

- **Modern FastAPI Application**
  - Async/await syntax
  - Type hints throughout
  - OpenAPI documentation
  - Dependency injection
  - Middleware support

- **Production-Ready Architecture**
  - Layered architecture
  - Dependency management with Poetry
  - Configuration management
  - Comprehensive logging
  - Error handling
  - Health checks

- **Database Integration**
  - PostgreSQL with asyncpg
  - Redis caching
  - Migration support
  - Connection pooling

- **Security**
  - API key authentication
  - CORS configuration
  - Rate limiting
  - Security headers
  - Input validation

- **Monitoring & Observability**
  - Prometheus metrics
  - Grafana dashboards
  - Structured logging
  - Health check endpoints
  - OpenTelemetry tracing

- **CI/CD Pipeline**
  - GitHub Actions
  - Jenkins integration
  - SonarQube analysis
  - Docker multi-stage builds
  - GitOps with ArgoCD

## 📋 Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Poetry
- kubectl (for K8s deployment)
- Git

## 🚀 Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/lethanhson9901/app-source.git
cd app-source
```

2. **Set up the environment**
```bash
# Create necessary directories and configs
chmod +x setup.sh
./setup.sh

# Copy and configure environment variables
cp .env.example .env
```

3. **Run with Docker Compose**
```bash
# Start all services
chmod +x run.sh
./run.sh

# Or manually

docker compose build app # manually build: `docker build -t local/python-app:latest .`

docker compose up -d
```

4. **Access the services**
- API: http://localhost:8080
- API Documentation: http://localhost:8080/docs
- Metrics: http://localhost:8080/metrics
- Grafana: http://localhost:8080/grafana (admin/admin)

## 🛠️ Development

### Local Development Setup

1. **Install dependencies**
```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install
```

2. **Set up pre-commit hooks**
```bash
poetry run pre-commit install
poetry run pre-commit install --hook-type commit-msg
```

    To disable/remove pre-commit hooks, you have a few options:

    1. To skip pre-commit checks for a single commit:
    ```bash
    git commit -m "your message" --no-verify
    ```

    2. To temporarily disable pre-commit:
    ```bash
    SKIP=pre-commit git commit -m "your message"
    ```

    3. To completely uninstall pre-commit hooks:
    ```bash
    pre-commit uninstall
    pre-commit uninstall --hook-type commit-msg
    ```

    4. You can also manually remove the hooks by deleting them from `.git/hooks/`:
    ```bash
    rm .git/hooks/pre-commit
    rm .git/hooks/commit-msg
    ```

    Would you like me to explain more about any of these methods or their implications?
3. **Run tests**
```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src --cov-report=html
```

4. **Code quality checks**
```bash
# Format code
poetry run black src/

# Lint code
poetry run ruff src/

# Type checking
poetry run mypy src/
```

### Docker Development

```bash
# Build and run services
docker-compose up -d --build

# View logs
docker-compose logs -f

# Run tests in container
docker-compose exec app poetry run pytest

# Stop services
docker-compose down
```

## 🏗️ Project Structure

```
.
├── app-source/
│   ├── deployments/           # Kubernetes/Helm configurations
│   ├── src/
│   │   ├── app/              # Application code
│   │   ├── monitoring/       # Monitoring configurations
│   │   └── tests/           # Test suites
│   ├── Dockerfile
│   └── pyproject.toml
├── infrastructure/           # Infrastructure as Code
└── app-config/              # GitOps configurations
```

## 🚢 Deployment

### Kubernetes Deployment

1. **Set up Kubernetes cluster**
```bash
# Using kind
kind create cluster --config kind-config.yaml
```

2. **Deploy applications**
```bash
# Install ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Deploy application
kubectl apply -f app-config/argocd/applications/myapp.yaml
```

### Production Considerations

- Set appropriate resource limits
- Configure horizontal pod autoscaling
- Set up proper monitoring
- Configure backups
- Implement proper security measures

## 🔍 Monitoring

### Available Metrics

- HTTP request count and latency
- Database connection pool stats
- Redis cache hit/miss ratio
- Custom business metrics

### Grafana Dashboards

- Application metrics
- Resource usage
- Error rates
- Request tracing

## 🔒 Security

- Non-root container execution
- Read-only root filesystem
- Resource limitations
- Network policies
- Security context configuration

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- FastAPI for the amazing framework
- Poetry for dependency management
- ArgoCD for GitOps deployment
- The open-source community

## 📚 Additional Documentation

- [API Documentation](docs/API.md)
- [Development Guide](docs/DEVELOPMENT.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Monitoring Guide](docs/MONITORING.md)

## 📫 Support

For support, please open an issue in the repository or contact the maintainers.

---
Made with ❤️ by [Your Name]