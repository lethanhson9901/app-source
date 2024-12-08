# 🔐 Git-crypt: Complete Implementation Guide

[![Security Tool](https://img.shields.io/badge/Category-Security-blue.svg)](https://github.com/AGWA/git-crypt)
[![Encryption](https://img.shields.io/badge/Feature-Encryption-green.svg)](https://github.com/AGWA/git-crypt)
[![Best Practices](https://img.shields.io/badge/Standard-Best%20Practices-orange.svg)](https://github.com/AGWA/git-crypt)

## 📑 Table of Contents
- [Introduction](#-introduction)
- [Core Concepts](#-core-concepts)
- [Installation Guide](#-installation-guide)
- [Implementation](#-implementation)
- [Best Practices](#-best-practices)
- [Common Patterns](#-common-patterns)
- [Troubleshooting](#-troubleshooting)
- [Team Management](#-team-management)

## 📖 Introduction

### What is Git-crypt?
Git-crypt is a transparent file encryption tool that integrates seamlessly with Git. It automatically encrypts files when they're pushed to a repository and decrypts them when pulled by authorized users. This allows you to store sensitive information in a Git repository while keeping it secure.

### Key Features
- 🔄 Transparent encryption/decryption
- 🔑 GPG key-based access control
- 📁 Selective file encryption
- 🤝 Multi-user support
- 🔍 Diff compatibility

## 🎯 Core Concepts

### How Git-crypt Works
1. **Filter System**: Uses Git's built-in filter system
2. **Encryption**: AES-256 encryption in CTR mode
3. **Key Management**: GPG for key distribution
4. **File Selection**: Uses `.gitattributes` for file selection

## 📥 Installation Guide

### Ubuntu Installation
```bash
# Update package list
sudo apt update

# Install git-crypt
sudo apt install -y git-crypt

# Install GPG if not installed
sudo apt install -y gnupg2

# Verify installation
git-crypt --version
```

### Generate GPG Key
```bash
# Generate a new GPG key
$ gpg --full-generate-key

gpg (GnuPG) 2.4.4; Copyright (C) 2024 g10 Code GmbH
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Please select what kind of key you want:
   (1) RSA and RSA
   (2) DSA and Elgamal
   (3) DSA (sign only)
   (4) RSA (sign only)
   (9) ECC (sign and encrypt) *default*
  (10) ECC (sign only)
  (14) Existing key from card
Your selection?
```
#### Explained

#### 1. RSA and RSA
**Purpose:** Dual-purpose key (Signing & Encryption)
- **What it does:** Creates two separate RSA keys
    - First key for signing documents/messages
    - Second key for encrypting data
- **Advantages:**
    - Very well-tested and trusted
    - Widely supported across all platforms
    - Good for long-term key validity
- **Best for:** Users needing maximum compatibility
- **Recommended key size:** 2048 or 4096 bits

#### 2. DSA and Elgamal
**Purpose:** Dual-purpose key (Signing & Encryption)
- **What it does:**
    - DSA component handles digital signatures
    - Elgamal component handles encryption
- **Note:** Generally considered legacy
- **Limitations:**
    - Less widely supported than RSA
    - Being phased out in modern applications
- **Not recommended** for new key generation

#### 3. DSA (sign only)
**Purpose:** Single-purpose key (Signing only)
- **What it does:** Creates a key only for signing
- **Limitations:**
    - Cannot encrypt data
    - Older algorithm
    - Limited key size options
- **Best for:** Legacy systems requiring DSA specifically
- **Note:** Not recommended for new installations

#### 4. RSA (sign only)
**Purpose:** Single-purpose key (Signing only)
- **What it does:** Creates an RSA key for signatures only
- **Advantages:**
    - Widely compatible
    - Well-understood algorithm
- **Best for:**
    - Code signing
    - Document signing
    - When encryption isn't needed
- **Note:** Cannot be used for encryption

#### 9. ECC (sign and encrypt) [DEFAULT]
**Purpose:** Dual-purpose key (Signing & Encryption)
- **What it does:** Creates a modern elliptic curve key
- **Advantages:**
    - Faster than RSA
    - Smaller key sizes
    - Strong security
- Modern algorithm
- **Best for:**
    - Most current users
    - Mobile devices
    - Modern applications
- **Why it's default:** Best balance of security and performance

#### 10. ECC (sign only)
**Purpose:** Single-purpose key (Signing only)
- **What it does:** Creates an ECC key for signatures
- **Advantages:**
    - Fast signature operations
    - Small key size
    - Modern security
- **Limitations:** No encryption capability
- **Best for:** Modern signing-only requirements

#### 14. Existing key from card
**Purpose:** Use hardware-stored keys
- **What it does:** Uses pre-existing keys on hardware
- **Advantages:**
    - Enhanced security through hardware
    - Protection against key extraction
- **Best for:**
    - Security-conscious users
    - Corporate environments
- **Required:** Hardware security device (smart card/token)

#### Recommendations

#### For Most Users
✅ Choose Option 9 (ECC)
- Modern security
- Excellent performance
- Good compatibility with current systems
- Smaller key sizes

#### For Legacy Systems
✅ Choose Option 1 (RSA and RSA)
- Maximum compatibility
- Well-understood security
- Widely supported

#### For Signing Only
✅ Choose Option 10 (ECC sign only)
- Modern algorithm
- Efficient for signing
- Smaller signatures

```text
Please select what kind of key you want:
   (1) RSA and RSA
   (2) DSA and Elgamal
   (3) DSA (sign only)
   (4) RSA (sign only)
   (9) ECC (sign and encrypt) *default*
  (10) ECC (sign only)
  (14) Existing key from card
Your selection? 9
Please select which elliptic curve you want:
   (1) Curve 25519 *default*
   (4) NIST P-384
   (6) Brainpool P-256
Your selection? 1
Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years
Key is valid for? (0) 1y
Key expires at Mon Dec  8 20:13:34 2025 +07
Is this correct? (y/N) y

GnuPG needs to construct a user ID to identify your key.

Real name: your-name
Email address: abc@example.com
Comment: test git-crypt
You selected this USER-ID:
    "your-name (test git-crypt) <abc@example.com>"

Change (N)ame, (C)omment, (E)mail or (O)kay/(Q)uit? o
We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.
We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.
gpg: directory '/home/son/.gnupg/openpgp-revocs.d' created
gpg: revocation certificate stored as '/home/son/.gnupg/openpgp-revocs.d/xxx.rev'
public and secret key created and signed.

pub   ed25519 2024-12-08 [SC] [expires: 2025-12-08]
      xxx
uid                      your-name (test git-crypt) <abc@example.com>
sub   cv25519 2024-12-08 [E] [expires: 2025-12-08]
```

```bash
# List your keys
gpg --list-secret-keys --keyid-format LONG

# Export public key (for team sharing)
gpg --armor --export your.email@domain.com > public-key.gpg
```

## 🛠️ Implementation

### 1. Repository Initialization
```bash
# Initialize a new repository
git init my-secure-project
cd my-secure-project

# Initialize git-crypt
git-crypt init

# Export git-crypt key (for backup)
git-crypt export-key ./git-crypt-key
```

### 2. Configure Encryption Rules
```bash
# Create .gitattributes
cat > .gitattributes <<EOL
# Encrypt all files in secrets directory
secrets/** filter=git-crypt diff=git-crypt

# Encrypt specific file types
*.key filter=git-crypt diff=git-crypt
*.env filter=git-crypt diff=git-crypt
*.secret filter=git-crypt diff=git-crypt

# Encrypt specific files
config/production.yaml filter=git-crypt diff=git-crypt
config/credentials.json filter=git-crypt diff=git-crypt

# Don't encrypt these files even if they match patterns above
!secrets/README.md
!secrets/example.env.template
EOL
```

### 3. Directory Structure
```bash
# Create secure directory structure
mkdir -p {secrets,config}/{production,staging,development}

# Create example files
cat > secrets/production/.env <<EOL
DATABASE_URL=postgresql://user:pass@localhost:5432/db #pragma: allowlist secret
API_KEY=your-secret-api-key
JWT_SECRET=your-jwt-secret
EOL

cat > secrets/README.md <<EOL
# Secrets Directory
This directory contains encrypted sensitive data.
Please contact the security team for access.
EOL
```

## 🏆 Best Practices

### 1. Key Management
```bash
# Generate project-specific GPG key
gpg --batch --full-generate-key <<EOF
%no-protection
Key-Type: RSA
Key-Length: 4096
Key-Usage: sign,encrypt
Subkey-Type: RSA
Subkey-Length: 4096
Subkey-Usage: sign,encrypt
Name-Real: Project Name
Name-Email: project@company.com
Expire-Date: 1y
EOF

# Backup keys
mkdir -p ~/.keys/backup
git-crypt export-key ~/.keys/backup/project-name.key
chmod 600 ~/.keys/backup/project-name.key
```

### 2. Access Control Script
```bash
#!/bin/bash
# manage-access.sh

function add_user() {
    local user_email=$1
    local key_file="public-keys/${user_email}.gpg"

    # Import user's public key
    gpg --import "$key_file"

    # Add user to git-crypt
    git-crypt add-gpg-user $(gpg --list-keys --keyid-format LONG "$user_email" | grep pub | cut -d/ -f2 | cut -d' ' -f1)

    echo "✅ Added user: $user_email"
}

function remove_user() {
    local user_email=$1

    # Remove user's public key
    gpg --delete-key "$user_email"

    echo "✅ Removed user: $user_email"
    echo "⚠️  Remember to rotate git-crypt key!"
}
```

### 3. File Organization
```plaintext
project/
├── .gitattributes           # Encryption rules
├── .git-crypt/              # Git-crypt metadata
├── secrets/
│   ├── production/
│   │   ├── .env
│   │   └── certificates/
│   ├── staging/
│   │   └── .env
│   └── README.md           # Unencrypted
├── config/
│   ├── production.yaml     # Encrypted
│   └── staging.yaml        # Encrypted
└── scripts/
    └── manage-access.sh    # Access management
```

### 4. Security Checklist
```markdown
## Pre-commit Checks
- [ ] No unencrypted secrets in commit
- [ ] All sensitive files match .gitattributes
- [ ] GPG keys properly backed up
- [ ] Access control list updated

## Repository Setup
- [ ] git-crypt initialized
- [ ] .gitattributes configured
- [ ] Key backup created
- [ ] README updated with instructions

## User Management
- [ ] GPG keys collected
- [ ] Users added to git-crypt
- [ ] Access documented
- [ ] Key rotation schedule set
```

## 🔄 Common Patterns

### 1. Environment-specific Encryption
```bash
# .gitattributes
secrets/production/** filter=git-crypt diff=git-crypt HIGH
secrets/staging/** filter=git-crypt diff=git-crypt MEDIUM
secrets/development/** filter=git-crypt diff=git-crypt LOW
```

### 2. Automated Key Rotation
```bash
#!/bin/bash
# rotate-keys.sh

echo "🔄 Starting key rotation..."

# Create new key
git-crypt init

# Export new key
git-crypt export-key ../new-key

# Re-add all users
for key in public-keys/*.gpg; do
    email=$(basename "$key" .gpg)
    echo "Adding user: $email"
    ./manage-access.sh add-user "$email"
done

echo "✅ Key rotation complete"
```

## ❗ Troubleshooting

| Issue | Solution |
|-------|----------|
| `not a git-crypt repository` | Run `git-crypt init` |
| `failed to decrypt` | Check if user has access |
| `git-crypt: gpg failed` | Verify GPG key availability |
| Files not encrypting | Check `.gitattributes` patterns |

## 👥 Team Management

### Onboarding New Team Member
```bash
# 1. Collect their GPG public key
gpg --import teammate-key.gpg

# 2. Add them to git-crypt
git-crypt add-gpg-user teammate@company.com

# 3. Document access
echo "teammate@company.com (added $(date +%Y-%m-%d))" >> ACCESS.md

# 4. Create welcome guide
cat > WELCOME.md <<EOL
# Welcome to the Project!

## Getting Started with git-crypt
1. Install git-crypt: \`sudo apt install git-crypt\`
2. Clone repository: \`git clone repo-url\`
3. Unlock repository: \`git-crypt unlock\`

## Security Guidelines
- Never commit unencrypted secrets
- Keep your GPG key secure
- Report any security concerns immediately

## Contact
Security Team: security@company.com
EOL
```

## 📚 Reference

### Essential Commands
```bash
# Initialize in a repository
git-crypt init

# Add GPG user
git-crypt add-gpg-user USER_ID

# Lock repository
git-crypt lock

# Unlock repository
git-crypt unlock

# Export key
git-crypt export-key PATH

# Status check
git-crypt status
```

### Quick Start Template
```bash
#!/bin/bash
# quickstart.sh

# Initialize repository
git init
git-crypt init

# Setup encryption rules
cat > .gitattributes <<EOL
secrets/** filter=git-crypt diff=git-crypt
*.env filter=git-crypt diff=git-crypt
EOL

# Create directory structure
mkdir -p secrets/{production,staging,development}

# Create example files
echo "DATABASE_URL=example" > secrets/development/.env

# Initial commit
git add .
git commit -m "Initial setup with git-crypt"

echo "✅ Repository initialized with git-crypt"
```

---

🔔 **Note**: Always backup your git-crypt keys and GPG keys in a secure location.

🤝 **Support**: For issues and questions, check the [official git-crypt repository](https://github.com/AGWA/git-crypt).
