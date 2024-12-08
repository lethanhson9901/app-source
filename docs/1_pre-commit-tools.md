# Pre-commit Tools Setup

## 1. Installation

```bash
# Install pre-commit
pip install pre-commit

# Install additional Python tools
pip install black ruff mypy bandit detect-secrets yamllint

# Install hadolint for Dockerfile linting
# For Linux:
wget -O /usr/local/bin/hadolint https://github.com/hadolint/hadolint/releases/download/v2.12.0/hadolint-Linux-x86_64
chmod +x /usr/local/bin/hadolint
```

## 2. Pre-commit Configuration

Create `.pre-commit-config.yaml` in your project root:

```yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: trailing-whitespace
        exclude: ^reports/
    -   id: end-of-file-fixer
        exclude: ^reports/
    -   id: check-yaml
        args: [--allow-multiple-documents]
    -   id: check-added-large-files
        args: ['--maxkb=1000']
    -   id: check-json
    -   id: check-ast
    -   id: debug-statements
    -   id: detect-private-key

-   repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
    -   id: black
        language_version: python3
        args: [--line-length=100]
        files: ^src/

-   repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.0.261
    hooks:
    -   id: ruff
        args: [--fix, --exit-non-zero-on-fix]
        files: ^src/

-   repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.2.0
    hooks:
    -   id: mypy
        additional_dependencies: [types-all]
        files: ^src/
        args: [--ignore-missing-imports, --disallow-untyped-defs]

-   repo: https://github.com/hadolint/hadolint
    rev: v2.12.0
    hooks:
    -   id: hadolint
        files: ^Dockerfile$|^dockerfiles/.*
        args: ['--ignore', 'DL3008', '--ignore', 'DL3013']

-   repo: https://github.com/adrienverge/yamllint.git
    rev: v1.32.0
    hooks:
    -   id: yamllint
        files: ^(\.pre-commit-config\.yaml|docker-compose\.yml)$
        args: [-c=.yamllint.yaml]

-   repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
    -   id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
        exclude: poetry.lock

-   repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
    -   id: bandit
        args: ['-c', 'pyproject.toml']
        additional_dependencies: ['bandit[toml]']
```

## 3. Additional Tool Configurations

### Create .yamllint.yaml:
```yaml
extends: default

rules:
  line-length:
    max: 100
    level: warning
  document-start: disable
  truthy:
    allowed-values: ['true', 'false', 'yes', 'no']

ignore: |
  reports/
  .git/
  node_modules/
```

### Update pyproject.toml for Bandit:
```toml
[tool.bandit]
exclude_dirs = ["tests", "reports"]
skips = ["B101", "B104"]  # Skip assert statements and hardcoded bind
targets = ["src"]

[tool.black]
line-length = 100
target-version = ['py311']
include = '\.pyi?$'

[tool.ruff]
line-length = 100
select = ["E", "F", "B", "I"]
ignore = ["E501"]
exclude = ["reports"]

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
check_untyped_defs = true
```

## 4. Initialize detect-secrets:
```bash
# Create a baseline for detect-secrets
detect-secrets scan > .secrets.baseline
```

## 5. Git hooks installation:
```bash
# Initialize pre-commit
pre-commit install

# Install specific hooks
pre-commit install --hook-type pre-push
pre-commit install --hook-type commit-msg
```

## 6. Usage Examples

```bash
# Run against all files
pre-commit run --all-files

# Run a specific hook
pre-commit run black --all-files

# Update hooks to latest versions
pre-commit autoupdate
```

## Tool-specific Commands

```bash
# Auto-format Python code according to PEP 8 style guide using black
black src/

# Run Ruff for fast Python linting and code quality checks
ruff check src/

# Perform static type checking with mypy to catch type-related errors
mypy src/

# Scan Python code for common security issues using Bandit
bandit -r src/

# Check Dockerfile for best practices and common mistakes
hadolint Dockerfile

# Validate YAML files for syntax and formatting issues
yamllint .

# Search for potential hardcoded secrets and credentials in source code
detect-secrets scan src/
```
