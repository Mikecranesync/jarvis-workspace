# FactoryLM Remote

Self-hosted remote desktop for industrial/manufacturing, built on RustDesk.

## Quick Start

```bash
# Deploy relay server
docker compose up -d
```

## Architecture

```
[Technician Phone/Laptop] <--WebRTC--> [Relay Server] <--WebRTC--> [Factory PLC Laptop]
```

## License

AGPL-3.0 (same as upstream RustDesk)
