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
# Top level default configuration for all hooks
default_language_version:
  python: python3.11
default_stages: [commit, push]
fail_fast: true
minimum_pre_commit_version: "3.5.0"

repos:
# Essential Git checks
- repo: https://github.com/pre-commit/pre-commit-hooks
  rev: v5.0.0
  hooks:
  - id: check-case-conflict
  - id: check-merge-conflict
  - id: check-symlinks
  - id: check-yaml
    args: [--allow-multiple-documents]
  - id: check-toml
  - id: check-json
  - id: detect-private-key
  - id: end-of-file-fixer
  - id: trailing-whitespace
    args: [--markdown-linebreak-ext=md]
  - id: mixed-line-ending
    args: [--fix=lf]
  - id: check-added-large-files
    args: ['--maxkb=500']
  - id: check-ast
  - id: debug-statements

# Python code formatting
- repo: https://github.com/psf/black
  rev: 24.10.0
  hooks:
  - id: black
    files: ^src/
    exclude: ^tests/

# Python import sorting
- repo: https://github.com/PyCQA/isort
  rev: 5.13.2
  hooks:
  - id: isort
    files: ^src/

# Python linting with Ruff
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: v0.8.2
  hooks:
  - id: ruff
    args: [--fix]
    files: ^src/

# Python type checking
- repo: https://github.com/pre-commit/mirrors-mypy
  rev: v1.13.0
  hooks:
  - id: mypy
    additional_dependencies: [
      types-requests,
      types-PyYAML,
      types-setuptools,
      types-redis,
      types-jwt
    ]
    args: [--config-file=pyproject.toml]
    files: ^src/

# Python security checks
- repo: https://github.com/PyCQA/bandit
  rev: 1.8.0
  hooks:
  - id: bandit
    args: ['-c', 'pyproject.toml']
    additional_dependencies: ['bandit[toml]']

# Secrets scanning
- repo: https://github.com/Yelp/detect-secrets
  rev: v1.5.0
  hooks:
  - id: detect-secrets
    args: [
      '--baseline', '.secrets.baseline',
      '--exclude-files', 'poetry.lock',
      '--exclude-files', '.*test.*'
    ]

# Dockerfile linting
- repo: https://github.com/hadolint/hadolint
  rev: v2.13.1-beta
  hooks:
  - id: hadolint
    args: [
      '--ignore', 'DL3008',
      '--ignore', 'DL3013',
      '--ignore', 'DL3059'
    ]
    files: ^Dockerfile$|^dockerfiles/.*

# Docker Compose validation
- repo: https://github.com/IamTheFij/docker-pre-commit
  rev: v3.0.1
  hooks:
  - id: docker-compose-check

# YAML linting
- repo: https://github.com/adrienverge/yamllint
  rev: v1.35.1
  hooks:
  - id: yamllint
    args: [-c=.yamllint.yaml]

# Terraform checks
- repo: https://github.com/antonbabenko/pre-commit-terraform
  rev: v1.96.2
  hooks:
  - id: terraform_fmt
  - id: terraform_validate
  - id: terraform_tflint
  - id: terraform_checkov

# Shell script checks
- repo: https://github.com/shellcheck-py/shellcheck-py
  rev: v0.10.0.1
  hooks:
  - id: shellcheck
    args: ['-x']

# Commit message checks
- repo: https://github.com/commitizen-tools/commitizen
  rev: v4.1.0
  hooks:
  - id: commitizen
    stages: [commit-msg]

```
---
I'll explain each tool's purpose and importance in your pre-commit setup:

1. **pre-commit-hooks (Essential Git Checks)**
```yaml
- repo: https://github.com/pre-commit/pre-commit-hooks
```
- `check-case-conflict`: Important for cross-platform development, prevents issues like having both `test.py` and `Test.py`
- `check-merge-conflict`: Catches forgotten merge markers like `>>>>`, `<<<<`, `====`
- `check-yaml/toml/json`: Validates configuration files syntax before commit
- `detect-private-key`: Security check for accidentally committed SSH keys, certificates
- `check-added-large-files`: Prevents repository bloat
- `check-ast`: Ensures Python files are syntactically valid
- `debug-statements`: Catches forgotten debugger statements (pdb, ipdb, breakpoint())

2. **Black (Code Formatter)**
```yaml
- repo: https://github.com/psf/black
```
- Enforces consistent Python code style
- Non-configurable by design to prevent style debates
- Files pattern `^src/`: Only formats source code, ignoring tests
- Current version: 24.10.0

3. **isort (Import Sorter)**
```yaml
- repo: https://github.com/PyCQA/isort
```
- Organizes imports into sections: standard library, third-party, local
- Alphabetizes within sections
- Version 5.13.2
- Only processes `src/` directory

4. **Ruff (Fast Linter)**
```yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
```
- Written in Rust, extremely fast
- Combines functionality of multiple Python linters
- Can automatically fix issues (`--fix`)
- Version v0.8.2

5. **mypy (Type Checker)**
```yaml
- repo: https://github.com/pre-commit/mirrors-mypy
```
- Static type checking for Python
- Additional type stubs installed for common packages
- Uses `pyproject.toml` for configuration
- Version v1.13.0

6. **Bandit (Security Linter)**
```yaml
- repo: https://github.com/PyCQA/bandit
```
- Scans for common security issues
- Checks for SQL injection, hardcoded passwords, etc.
- Uses `pyproject.toml` for configuration
- Version 1.8.0

7. **detect-secrets**
```yaml
- repo: https://github.com/Yelp/detect-secrets
```
- Identifies accidentally committed secrets/credentials
- Uses `.secrets.baseline` for approved exceptions
- Excludes `poetry.lock` and test files
- Version v1.5.0

8. **hadolint (Dockerfile Linter)**
```yaml
- repo: https://github.com/hadolint/hadolint
```
- Validates Dockerfile best practices
- Ignores specific rules:
  - DL3008: Pin versions in apt-get install
  - DL3013: Pin versions in pip install
  - DL3059: Multiple consecutive RUN commands
- Version v2.13.1-beta

9. **docker-compose-check**
```yaml
- repo: https://github.com/IamTheFij/docker-pre-commit
```
- Validates docker-compose file syntax
- Catches configuration errors before commit

10. **yamllint**
```yaml
- repo: https://github.com/adrienverge/yamllint
```
- Lints YAML files for format and structure
- Uses custom config `.yamllint.yaml`
- Version v1.35.1

11. **pre-commit-terraform**
```yaml
- repo: https://github.com/antonbabenko/pre-commit-terraform
```
- `terraform_fmt`: Consistent formatting
- `terraform_validate`: Configuration validation
- `terraform_tflint`: Advanced Terraform linting
- `terraform_checkov`: Security and compliance checks
- Version v1.96.2

12. **shellcheck**
```yaml
- repo: https://github.com/shellcheck-py/shellcheck-py
```
- Finds bugs in shell scripts
- `-x` flag follows source statements
- Version v0.10.0.1

13. **commitizen**
```yaml
- repo: https://github.com/commitizen-tools/commitizen
```
- Enforces conventional commit messages
- Format: `type(scope): description`
- Runs during commit-msg stage
- Version v4.1.0

This configuration provides a comprehensive safety net for code quality, security, and consistency across multiple technologies in your development workflow.
---
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

---
