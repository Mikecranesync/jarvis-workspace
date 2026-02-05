# FactoryLM Windows Device Configuration

Enterprise-grade device management for small teams.

## Quick Setup (Any Device)

Run in **Admin PowerShell**:

```powershell
# Full device setup (lid close, power, monitoring)
irm https://raw.githubusercontent.com/Mikecranesync/jarvis-workspace/main/scripts/windows/bootstrap.ps1 | iex
```

## Individual Scripts

| Script | Purpose |
|--------|---------|
| `configure-lid-close.ps1` | Prevent sleep on lid close |
| `install-tailscale.ps1` | Install + configure Tailscale |
| `bootstrap.ps1` | Full device setup (runs all) |

## What Gets Configured

- ✅ Lid close → Do Nothing
- ✅ Sleep when plugged in → Never
- ✅ Hibernate → Disabled
- ✅ USB selective suspend → Disabled
- ✅ Tailscale → Installed and running
- ✅ Startup → Tailscale auto-starts

## Enterprise Patterns Used

1. **Config-as-Code** - All settings in version control
2. **Idempotent Scripts** - Safe to run multiple times
3. **One-liner Deploy** - `irm | iex` pattern
4. **Centralized Monitoring** - VPS detects offline devices
5. **Zero-Touch Provisioning** - New device? Run one command.

No Active Directory. No domain controllers. No licensing fees.
