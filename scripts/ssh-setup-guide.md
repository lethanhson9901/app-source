# Ultimate SSH Setup Guide: Ubuntu to Windows

## Table of Contents
- [Prerequisites](#prerequisites)
- [Windows Setup](#windows-setup)
- [Ubuntu Setup](#ubuntu-setup)
- [Testing Connection](#testing-connection)
- [Advanced Configuration](#advanced-configuration)
- [Troubleshooting](#troubleshooting)
- [Security Best Practices](#security-best-practices)

## Prerequisites

### Required Software
- Windows 10/11
- Ubuntu (any recent version)
- Administrator access on Windows
- sudo privileges on Ubuntu

### Network Requirements
- Both machines on same network
- Port 22 open for SSH traffic
- No restrictive firewall rules

## Windows Setup

### 1. Install OpenSSH Server

Using PowerShell (as Administrator):
```powershell
# Install OpenSSH Server
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

# Start SSH service
Start-Service sshd

# Enable automatic start
Set-Service -Name sshd -StartupType 'Automatic'
```

Alternative installation through Settings:
1. Settings → Apps → Optional features
2. Add feature → OpenSSH Server
3. Install

### 2. Configure Firewall

```powershell
# Allow SSH traffic
New-NetFirewallRule -Name 'OpenSSH-Server-In-TCP' -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22

# Allow ICMP (ping) - Optional but recommended for testing
New-NetFirewallRule -DisplayName "Allow ICMPv4-In" -Protocol ICMPv4 -IcmpType 8 -Enabled True -Profile Any -Action Allow
New-NetFirewallRule -DisplayName "Allow ICMPv4-Out" -Protocol ICMPv4 -IcmpType 8 -Enabled True -Profile Any -Action Allow
```

### 3. Find Windows IP Address
```powershell
ipconfig
```
Note down the IPv4 address (usually starts with 192.168. or 10.0.)

## Ubuntu Setup

### 1. Install SSH Client
```bash
# Update package list
sudo apt update

# Install OpenSSH client
sudo apt install openssh-client -y
```

### 2. Generate SSH Keys (Optional but Recommended)
```bash
# Generate key pair
ssh-keygen -t ed25519 -C "your_email@example.com"

# Copy key to Windows
ssh-copy-id username@windows_ip
```

## Testing Connection

### 1. Basic Connectivity Test
```bash
# Test network connectivity
ping windows_ip

# Test SSH connection
ssh username@windows_ip
```

### 2. File Transfer Test
```bash
# Create test file
echo "test" > test.txt

# Copy to Windows
scp test.txt username@windows_ip:C:/Users/username/Desktop/
```

## Advanced Configuration

### 1. SSH Config File
Create/edit `~/.ssh/config` on Ubuntu:
```
Host windows-pc
    HostName windows_ip
    User username
    Port 22
    IdentityFile ~/.ssh/id_ed25519
```

### 2. Windows SSH Configuration
Edit `C:\ProgramData\ssh\sshd_config`:
```conf
# Allow public key authentication
PubkeyAuthentication yes

# Disable password authentication (optional)
PasswordAuthentication no

# Allow specific users
AllowUsers username1 username2
```

## Troubleshooting

### Common Issues and Solutions

1. Connection Refused
```powershell
# Check SSH service status
Get-Service sshd

# Restart SSH service
Restart-Service sshd
```

2. Permission Issues
```powershell
# Check SSH folder permissions
icacls "C:\ProgramData\ssh"
```

3. Network Issues
```bash
# Check network interface
ip addr show

# Check route
route -n
```

## Security Best Practices

1. Key-based Authentication
- Generate strong SSH keys
- Protect private keys with passphrase
- Disable password authentication

2. Firewall Configuration
- Limit SSH access to specific IP ranges
- Use non-standard ports (optional)
- Enable connection logging

3. Regular Maintenance
- Keep systems updated
- Monitor SSH logs
- Regularly rotate SSH keys

4. SSH Config Hardening
```conf
# Disable root login
PermitRootLogin no

# Use SSH Protocol 2
Protocol 2

# Set login grace time
LoginGraceTime 60
```

## Command Reference

### Windows Commands
```powershell
# Service management
Get-Service sshd
Start-Service sshd
Stop-Service sshd
Restart-Service sshd

# Check port status
netstat -an | findstr :22

# Check firewall rules
Get-NetFirewallRule | Where-Object DisplayName -like "*SSH*"
```

### Ubuntu Commands
```bash
# SSH connection
ssh username@windows_ip

# Key management
ssh-keygen
ssh-copy-id
ssh-add

# File transfer
scp source_file username@windows_ip:destination
rsync -avz source_folder username@windows_ip:destination
```

### Advanced Usage
```bash
# Port forwarding
ssh -L local_port:remote_host:remote_port username@windows_ip

# Jump host
ssh -J jumphost username@windows_ip

# Keep connection alive
ssh -o ServerAliveInterval=60 username@windows_ip
```

Remember to replace:
- `username` with your Windows username
- `windows_ip` with your Windows PC's IP address
- `your_email@example.com` with your email
