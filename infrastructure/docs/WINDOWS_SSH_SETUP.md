# Windows SSH Setup for Jarvis

Complete guide to enable SSH access from JarvisVPS to Windows laptops.

---

## Quick Setup (Recommended)

**Download and run the setup script:**

```powershell
# Run PowerShell as Administrator
# Download setup script
Invoke-WebRequest -Uri "http://100.68.120.99:8080/scripts/setup-ssh-key.ps1" -OutFile setup-ssh-key.ps1

# Or copy from VPS via Tailscale
scp root@100.68.120.99:/root/jarvis-workspace/infrastructure/scripts/setup-ssh-key.ps1 .

# Run it
.\setup-ssh-key.ps1
```

---

## Manual Setup

### Step 1: Install OpenSSH Server

```powershell
# Check if installed
Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH.Server*'

# Install if needed
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
```

### Step 2: Start SSH Service

```powershell
# Start the service
Start-Service sshd

# Set to start automatically
Set-Service -Name sshd -StartupType 'Automatic'

# Verify it's running
Get-Service sshd
```

### Step 3: Add VPS Public Key

```powershell
# Create the authorized_keys file for administrators
$key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOY0hljziGSbgrv8E/wmCXovYypHw1IKWX5XYyw/hqvY root@srv1078052"

# Add to administrators_authorized_keys (for admin users)
Add-Content C:\ProgramData\ssh\administrators_authorized_keys $key
```

### Step 4: Fix Permissions (CRITICAL!)

Windows SSH is VERY strict about permissions. The authorized_keys file must only be readable by SYSTEM and Administrators.

```powershell
# Remove inheritance and set correct permissions
icacls C:\ProgramData\ssh\administrators_authorized_keys /inheritance:r
icacls C:\ProgramData\ssh\administrators_authorized_keys /grant "SYSTEM:(F)"
icacls C:\ProgramData\ssh\administrators_authorized_keys /grant "Administrators:(F)"
```

### Step 5: Configure sshd_config

```powershell
# Edit SSH config
notepad C:\ProgramData\ssh\sshd_config
```

Ensure these lines are present (uncommented):
```
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys
```

For admin users, also ensure this is at the END of the file:
```
Match Group administrators
    AuthorizedKeysFile __PROGRAMDATA__/ssh/administrators_authorized_keys
```

### Step 6: Restart SSH

```powershell
Restart-Service sshd
```

### Step 7: Configure Firewall

```powershell
# Allow SSH through firewall
New-NetFirewallRule -Name "OpenSSH-Server-In-TCP" -DisplayName "OpenSSH Server (sshd)" -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
```

---

## Verification

### From the Windows machine:

```powershell
# Check SSH service
Get-Service sshd

# Check authorized_keys exists and has content
Get-Content C:\ProgramData\ssh\administrators_authorized_keys

# Check permissions
icacls C:\ProgramData\ssh\administrators_authorized_keys
```

### From VPS:

```bash
# Test connection
ssh mike@<windows-ip> "hostname && whoami"

# If it works, you'll see the hostname and username
```

---

## Troubleshooting

### "Permission denied (publickey)"

**Cause:** Key not in authorized_keys OR permissions wrong

**Fix:**
1. Verify the key is in the file:
   ```powershell
   Get-Content C:\ProgramData\ssh\administrators_authorized_keys | Select-String "AAAAC3NzaC1"
   ```

2. Fix permissions:
   ```powershell
   icacls C:\ProgramData\ssh\administrators_authorized_keys /inheritance:r /grant "SYSTEM:(F)" /grant "Administrators:(F)"
   ```

3. Restart SSH:
   ```powershell
   Restart-Service sshd
   ```

### "Connection refused"

**Cause:** SSH service not running or firewall blocking

**Fix:**
1. Start SSH:
   ```powershell
   Start-Service sshd
   ```

2. Check firewall:
   ```powershell
   Get-NetFirewallRule -Name "*ssh*" | Format-Table Name, Enabled, Action
   ```

### "Host key verification failed"

**Cause:** Host key changed (reinstall, etc.)

**Fix on VPS:**
```bash
ssh-keygen -R <windows-ip>
```

### Debug Mode

**On VPS, connect with verbose output:**
```bash
ssh -v mike@<windows-ip> "hostname"
```

**On Windows, check SSH logs:**
```powershell
Get-WinEvent -LogName "OpenSSH/Operational" -MaxEvents 20
```

---

## Security Notes

1. **Never use password authentication** - Key-based only
2. **Keep authorized_keys permissions locked down** - SYSTEM and Administrators only
3. **Use Tailscale** - All traffic encrypted, no port forwarding needed
4. **Monitor access** - Check logs regularly

---

## VPS Public Key Reference

This is the key that needs to be in `administrators_authorized_keys`:

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOY0hljziGSbgrv8E/wmCXovYypHw1IKWX5XYyw/hqvY root@srv1078052
```

Fingerprint: `SHA256:Bt9FzW1sBCpoR7P8f63sMYG2S+ls6U8ZMUhUMMjhJ1M`
