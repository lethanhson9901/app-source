# 🛡️ Enterprise Security Tools Guide
> A detailed guide to understanding and implementing security tools with best practices

[![Security Best Practices](https://img.shields.io/badge/Security-Best%20Practices-blue.svg)](https://github.com/topics/security-tools)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-20.04+-orange.svg)](https://ubuntu.com/)
[![Documentation](https://img.shields.io/badge/Documentation-Comprehensive-green.svg)](https://github.com/topics/documentation)

## 📑 Table of Contents
- [Git-crypt](#-git-crypt)
- [Mozilla SOPS](#-mozilla-sops)
- [GitLeaks](#-gitleaks)
- [TruffleHog](#-trufflehog)

## 🔐 Git-crypt

### What is Git-crypt?
Git-crypt is a transparent file encryption tool that automatically encrypts files pushed to a Git repository and decrypts them when pulled by authorized users. It uses GPG keys for access control and ensures sensitive data remains secure while maintaining the benefits of Git version control.

### Key Features
- 🔄 Transparent encryption/decryption
- 🔑 GPG-based access control
- 📁 File-specific encryption
- 🤝 Team collaboration support

### Best Practices Setup

```bash
# 1. Installation
sudo apt install -y git-crypt

# 2. Generate a robust GPG key
gpg --full-generate-key

# 3. Initialize in repository
git init
git-crypt init

# 4. Create comprehensive .gitattributes
cat > .gitattributes <<EOL
# Encrypt all files in secrets directory
secrets/** filter=git-crypt diff=git-crypt

# Encrypt specific file types
*.key filter=git-crypt diff=git-crypt
*.pem filter=git-crypt diff=git-crypt
*.env filter=git-crypt diff=git-crypt
*.secret filter=git-crypt diff=git-crypt

# Encrypt specific files
config/production.yaml filter=git-crypt diff=git-crypt
config/credentials.json filter=git-crypt diff=git-crypt
EOL

# 5. Create a secure backup of the encryption key
git-crypt export-key ~/git-crypt-key
# Store this key securely offline
```

### Security Best Practices
1. **Key Management**
   - Generate unique keys per repository
   - Use 4096-bit GPG keys
   - Store backup keys in secure offline storage
   - Rotate keys annually

2. **File Organization**
   ```plaintext
   repository/
   ├── .gitattributes
   ├── secrets/
   │   ├── production/
   │   │   ├── api-keys.env
   │   │   └── certificates/
   │   └── staging/
   │       └── test-keys.env
   └── config/
       ├── public-config.yaml
       └── private-config.yaml
   ```

3. **Access Control**
   - Maintain a list of authorized GPG keys
   - Review access quarterly
   - Remove departed team members immediately
   - Document key rotation procedures

## 🔐 Mozilla SOPS

### What is SOPS?
SOPS (Secrets OPerationS) is a tool for encrypting and decrypting files with multiple encryption methods and key management services. It supports various formats (YAML, JSON, ENV, INI) and allows for selective encryption of specific values while maintaining file structure.

### Key Features
- 🔢 Multiple encryption backends (GPG, AWS KMS, GCP KMS)
- 📄 Format-preserving encryption
- 🎯 Selective value encryption
- 🔄 Version control friendly

### Best Practices Setup

```bash
# 1. Installation
SOPS_VERSION="v3.7.3"
wget "https://github.com/mozilla/sops/releases/download/${SOPS_VERSION}/sops-${SOPS_VERSION}.linux.amd64"
chmod +x sops-${SOPS_VERSION}.linux.amd64
sudo mv sops-${SOPS_VERSION}.linux.amd64 /usr/local/bin/sops

# 2. Create comprehensive configuration
cat > .sops.yaml <<EOL
creation_rules:
  # Production environment
  - path_regex: production/.*\.yaml$
    pgp: 'PRODUCTION_GPG_KEY_FINGERPRINT'
    encrypted_regex: '^(password|secret|key|token|private_key)$'

  # Staging environment
  - path_regex: staging/.*\.yaml$
    pgp: 'STAGING_GPG_KEY_FINGERPRINT'
    encrypted_regex: '^(password|secret|key|token|private_key)$'

  # Default rule
  - pgp: 'DEFAULT_GPG_KEY_FINGERPRINT'
    encrypted_regex: '^(password|secret|key|token|private_key)$'
EOL

# 3. Create directory structure
mkdir -p {production,staging}/secrets

# 4. Create example configuration
cat > production/secrets/config.yaml <<EOL
database:
  host: db.example.com
  username: admin
  password: super-secret-password
api:
  endpoint: api.example.com
  key: secret-api-key
EOL

# 5. Encrypt file
sops -e -i production/secrets/config.yaml
```

### Security Best Practices
1. **Configuration Management**
   - Use environment-specific encryption keys
   - Implement strict regex patterns
   - Version control `.sops.yaml`
   - Document encryption patterns

2. **File Organization**
   ```plaintext
   project/
   ├── .sops.yaml
   ├── production/
   │   └── secrets/
   │       ├── api.yaml
   │       └── database.yaml
   └── staging/
       └── secrets/
           ├── api.yaml
           └── database.yaml
   ```

3. **Key Rotation**
   - Schedule regular key rotation
   - Maintain key backup procedures
   - Document recovery process
   - Test recovery regularly

## 🔍 GitLeaks

### What is GitLeaks?
GitLeaks is a SAST (Static Application Security Testing) tool that scans repositories for secrets and sensitive information. It uses pattern matching and entropy analysis to detect potential security risks in code and commits.

### Key Features
- 🔎 Pattern-based secret detection
- 📊 Entropy analysis
- 🕒 Git history scanning
- ⚡ Pre-commit integration

### Best Practices Setup

```bash
# 1. Installation
GITLEAKS_VERSION="v8.8.7"
wget "https://github.com/zricethezav/gitleaks/releases/download/${GITLEAKS_VERSION}/gitleaks_${GITLEAKS_VERSION}_linux_x64.tar.gz"
tar -xzf gitleaks_${GITLEAKS_VERSION}_linux_x64.tar.gz
sudo mv gitleaks /usr/local/bin/

# 2. Create comprehensive configuration
cat > .gitleaks.toml <<EOL
[allowlist]
  description = "Allowlisted files"
  paths = [
    '''node_modules''',
    '''yarn.lock''',
    '''package-lock.json''',
    '''fixtures/''',
    '''__snapshots__/'''
  ]

[[rules]]
  description = "AWS Access Key"
  regex = '''(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}'''
  tags = ["aws", "credentials"]

[[rules]]
  description = "Generic API Key"
  regex = '''(?i)(api_key|apikey|secret)(.{0,20})?['\"][0-9a-zA-Z]{32,45}['\"]'''
  tags = ["api", "key"]

[[rules]]
  description = "Generic Secret"
  regex = '''(?i)secret(.{0,20})?['\"][0-9a-zA-Z]{32,45}['\"]'''
  tags = ["secret"]

[[rules]]
  description = "Private Key"
  regex = '''-----BEGIN ((EC|PGP|DSA|RSA|OPENSSH) )?PRIVATE KEY( BLOCK)?-----'''
  tags = ["key", "private"]
EOL

# 3. Create scan script
cat > scan-repo.sh <<EOL
#!/bin/bash
echo "🔍 Scanning repository..."
gitleaks detect --source . --verbose --report-path gitleaks-report.json
echo "✅ Scan complete. Check gitleaks-report.json for results."
EOL
chmod +x scan-repo.sh
```

### Security Best Practices
1. **Scanning Strategy**
   - Run pre-commit hooks
   - Schedule regular scans
   - Monitor historical commits
   - Review scan reports weekly

2. **Rule Management**
   - Customize rules for your stack
   - Update patterns regularly
   - Document false positives
   - Maintain allowlists carefully

3. **Integration Points**
   - CI/CD pipelines
   - Pre-commit hooks
   - Pull request checks
   - Automated reporting

## 🕵️ TruffleHog

### What is TruffleHog?
TruffleHog is a secret scanning tool that searches through Git repositories for secrets, using pattern matching, high entropy string detection, and commit history analysis. It's designed to find accidentally committed secrets and credentials.

### Key Features
- 🔬 Deep repository scanning
- 📈 Entropy analysis
- 🕒 Commit history search
- 🎯 Regular expression matching

### Best Practices Setup

```bash
# 1. Installation
pip3 install trufflehog

# 2. Create comprehensive scan script
cat > trufflehog-scan.sh <<EOL
#!/bin/bash

echo "🔍 Starting TruffleHog scan..."

# Scan current repository
trufflehog git file://. \
  --only-verified \
  --json \
  --fail \
  --no-update \
  > trufflehog-report.json

# Format report
if [ -s trufflehog-report.json ]; then
    echo "⚠️ Secrets found! Check trufflehog-report.json"
    exit 1
else
    echo "✅ No verified secrets found!"
    exit 0
fi
EOL
chmod +x trufflehog-scan.sh

# 3. Create pre-commit hook
cat > .git/hooks/pre-commit <<EOL
#!/bin/bash
./trufflehog-scan.sh
EOL
chmod +x .git/hooks/pre-commit
```

### Security Best Practices
1. **Scanning Configuration**
   - Use `--only-verified` flag
   - Enable JSON output
   - Implement fail-fast
   - Regular scheduled scans

2. **Integration Strategy**
   - Pre-commit hooks
   - CI/CD pipelines
   - Pull request checks
   - Automated reporting

3. **Maintenance**
   - Regular tool updates
   - Report review process
   - False positive management
   - Team notification system

## 📊 Comparison Table

| Feature | Git-crypt | SOPS | GitLeaks | TruffleHog |
|---------|-----------|------|----------|------------|
| Primary Use | File Encryption | Secret Management | Secret Detection | Secret Detection |
| Integration | Git | Any | Git | Git |
| Encryption | GPG | Multiple | N/A | N/A |
| CI/CD Ready | ✅ | ✅ | ✅ | ✅ |
| Pre-commit | ❌ | ❌ | ✅ | ✅ |
| Learning Curve | Medium | Medium | Low | Low |

## 🔄 Maintenance Recommendations

1. **Weekly Tasks**
   - Run full repository scans
   - Update tool versions
   - Review scan reports
   - Update allowlists

2. **Monthly Tasks**
   - Audit access controls
   - Review encryption patterns
   - Update documentation
   - Test recovery procedures

3. **Quarterly Tasks**
   - Rotate encryption keys
   - Review security policies
   - Update tool configurations
   - Team security training

4. **Annual Tasks**
   - Full security audit
   - Tool evaluation
   - Process review
   - Documentation update

## 📚 Additional Resources

- [Git-crypt Documentation](https://github.com/AGWA/git-crypt)
- [SOPS Documentation](https://github.com/mozilla/sops)
- [GitLeaks Documentation](https://github.com/zricethezav/gitleaks)
- [TruffleHog Documentation](https://github.com/trufflesecurity/trufflehog)

---

🔔 **Note**: Always test these tools in a safe environment before implementing them in production systems.

⚖️ **License**: This guide is licensed under the MIT License.
