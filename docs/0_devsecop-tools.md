# Free and Open Source DevSecOps Tools

This repo include a comprehensive collection of free and open-source tools that cover the entire DevSecOps lifecycle. Here's the big picture:

1. **Developer Security Tools**
- Pre-commit tools that catch issues before code is committed
- Code formatting and linting tools
- Type checkers and basic security scanners

2. **Application Security**
- Secret management solutions for protecting sensitive data
- Dependency scanning to find vulnerable packages
- Static (SAST) and Dynamic (DAST) security testing tools
- Supply chain security tools to ensure code integrity

3. **Infrastructure Security**
- Container security scanners (like Trivy and Clair)
- Kubernetes security tools (kube-bench, kube-hunter)
- Infrastructure as Code security scanners (checkov, tfsec)
- Network security tools (Wireshark, nmap)

4. **Pipeline & Operations**
- CI/CD security tools integrated with popular platforms
- Testing tools for unit, integration, and load testing
- Monitoring and observability solutions
- Policy enforcement tools to ensure security compliance

The document also includes practical examples showing:
- How to set up pre-commit hooks
- How to integrate security checks in Jenkins pipelines
- How to implement Kubernetes security policies
- How to write basic security policies using Open Policy Agent (OPA)

![alt text](overview.png)

# DevSecOps Tools Reference Table

## Development Security

### Pre-commit Tools
| Tool | Type | Purpose | Key Features |
|------|------|---------|--------------|
| pre-commit | Framework | Git hook management | - Multi-language support<br>- Plugin ecosystem<br>- Easy configuration |
| black | Code Formatter | Python formatting | - Deterministic output<br>- PEP 8 compliant<br>- IDE integration |
| ruff | Linter | Python linting | - High performance<br>- Extensible rules<br>- Auto-fixes |
| mypy | Type Checker | Python type checking | - Static type verification<br>- Type inference<br>- Plugin system |
| hadolint | Linter | Dockerfile validation | - Best practice checks<br>- Shell script validation<br>- Integration support |
| yamllint | Validator | YAML validation | - Syntax verification<br>- Style checking<br>- Customizable rules |
| detect-secrets | Scanner | Secrets detection | - Pattern matching<br>- Custom rules<br>- CI integration |
| gitleaks | Scanner | Secrets detection | - Git history scanning<br>- Multiple secret types<br>- High accuracy |

### Secrets Management
| Tool | Type | Key Features |
|------|------|--------------|
| Mozilla SOPS | Encryption Tool | - Multiple cloud KMS support<br>- File encryption<br>- Git integration |
| git-crypt | Git Tool | - Transparent encryption<br>- File-specific rules<br>- GPG support |
| Sealed Secrets | Kubernetes Tool | - One-way encryption<br>- Controller-based<br>- GitOps friendly |
| AWS Secrets Manager | Cloud Service | - Rotation support<br>- Fine-grained access<br>- API integration |
| Azure Key Vault | Cloud Service | - Certificate management<br>- Key management<br>- HSM support |
| Google Secret Manager | Cloud Service | - Version control<br>- IAM integration<br>- Audit logging |

## Security Testing

### SAST Tools
| Tool | Language Focus | Key Features |
|------|---------------|--------------|
| SonarQube CE | Multi-language | - Code quality metrics<br>- Security hotspots<br>- Technical debt tracking |
| Bandit | Python | - AST scanning<br>- Plugin system<br>- Configuration options |
| Semgrep | Multi-language | - Pattern matching<br>- Custom rules<br>- Quick scanning |
| PMD | Java | - Custom rules<br>- Extensible<br>- Multiple formats |
| ESLint | JavaScript | - Pluggable<br>- Automatic fixing<br>- Custom rules |
| CodeQL | Multi-language | - Query language<br>- Deep analysis<br>- GitHub integration |

### DAST Tools
| Tool | Type | Key Features |
|------|------|--------------|
| OWASP ZAP | Web Scanner | - Active/passive scanning<br>- API testing<br>- Automation support |
| Nikto | Web Scanner | - Comprehensive checks<br>- Multiple report formats<br>- Plugin architecture |
| w3af | Web Scanner | - Plugin-based<br>- Multiple interfaces<br>- Advanced scanning |
| SQLmap | SQL Injection | - Automatic exploitation<br>- Database fingerprinting<br>- Multiple techniques |

## Infrastructure Security

### Container Security
| Tool | Purpose | Key Features |
|------|---------|--------------|
| Trivy | Vulnerability Scanner | - Fast scanning<br>- Low false positives<br>- Multiple formats |
| Clair | Container Analysis | - Layer scanning<br>- API integration<br>- Version tracking |
| Docker Bench | Security Checker | - CIS benchmark<br>- Best practices<br>- Detailed reports |
| Falco | Runtime Security | - Real-time monitoring<br>- Custom rules<br>- Container insights |

### Infrastructure Testing
| Tool | Focus | Key Features |
|------|-------|--------------|
| checkov | IaC Scanner | - Multiple IaC types<br>- Policy as code<br>- CI integration |
| tfsec | Terraform | - Security scanning<br>- Custom rules<br>- Inline ignores |
| kube-bench | Kubernetes | - CIS benchmarks<br>- Comprehensive checks<br>- Remediation advice |
| kube-hunter | Kubernetes | - Penetration testing<br>- Network scanning<br>- Risk assessment |

## Operations Tools

### CI/CD Security
| Tool | Type | Key Features |
|------|------|--------------|
| Jenkins | CI Server | - Plugin ecosystem<br>- Pipeline as code<br>- Extensive integration |
| GitLab CI | CI/CD Platform | - Built-in security<br>- Container registry<br>- Auto DevOps |
| GitHub Actions | CI/CD Service | - Workflow automation<br>- Matrix builds<br>- Community actions |
| Argo CD | GitOps Tool | - Kubernetes native<br>- Declarative setup<br>- Auto-sync |

### Monitoring & Testing
| Tool | Category | Key Features |
|------|----------|--------------|
| Prometheus | Metrics | - Time-series DB<br>- Alert management<br>- Pull model |
| Grafana | Visualization | - Multiple sources<br>- Custom dashboards<br>- Alerting |
| JMeter | Load Testing | - Scalable testing<br>- Multiple protocols<br>- Extensible |
| Postman | API Testing | - Request builder<br>- Automation<br>- Team collaboration |

### Network Security
| Tool | Type | Key Features |
|------|------|--------------|
| Wireshark | Packet Analyzer | - Deep packet inspection<br>- Protocol analysis<br>- Capture filters |
| nmap | Network Scanner | - Port scanning<br>- Service detection<br>- Script engine |
| Snort | IDS/IPS | - Real-time traffic analysis<br>- Rule-based detection<br>- Protocol analysis |
