# Raspberry Pi Setup for Jarvis Node

Complete guide to set up a Raspberry Pi as a Jarvis Node with camera, GPIO, and remote control capabilities.

---

## Hardware Requirements

- Raspberry Pi 4 (recommended) or Pi 3B+
- 16GB+ microSD card
- Power supply (5V 3A for Pi 4)
- Ethernet cable (for initial setup)
- Optional: Pi Camera Module
- Optional: Sensors, relays, etc. for GPIO

---

## Part 1: Flash the SD Card

### Option A: With Monitor/Keyboard (Easiest)

1. Download Raspberry Pi Imager: https://www.raspberrypi.com/software/
2. Choose OS: **Raspberry Pi OS (32-bit)**
3. Choose Storage: Select your SD card
4. Click **Write**

### Option B: Headless (No Monitor)

1. Flash Raspberry Pi OS Lite using Imager
2. Before ejecting, create these files on the boot partition:

**Enable SSH:**
```bash
# Create empty file named 'ssh'
touch /Volumes/boot/ssh
```

**Configure WiFi (optional):**
```bash
# Create wpa_supplicant.conf
cat > /Volumes/boot/wpa_supplicant.conf << 'EOF'
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="YOUR_WIFI_NAME"
    psk="YOUR_WIFI_PASSWORD"
    key_mgmt=WPA-PSK
}
EOF
```

**Set default user:**
Create `userconf.txt` with encrypted password:
```bash
echo 'pi:$6$rBoByrWRKMY1EHFy$ho.LISnfm83CLBWBE/yqJ6Lq1TinRlxw/ImMTPcvvMuUfhQYcMmFnpFXUPowjy2br1NA0IACwF9JKugSNuHoe0' > /Volumes/boot/userconf.txt
```
(This sets password to 'raspberry' - change after first boot!)

---

## Part 2: First Boot Setup

### If Direct Ethernet Connection to Laptop

1. Enable Internet Sharing on laptop:
   - Windows: Control Panel → Network → Sharing
   - Share WiFi to Ethernet adapter

2. Find the Pi's IP:
   ```powershell
   arp -a | findstr 192.168.137
   ```

3. SSH in:
   ```bash
   ssh pi@192.168.137.x
   ```

### If Connected to Router

1. Find Pi on network:
   ```bash
   ping raspberrypi.local
   # or check router's DHCP leases
   ```

2. SSH in:
   ```bash
   ssh pi@raspberrypi.local
   ```

---

## Part 3: Install Jarvis Node

Once SSH'd into the Pi, run the setup script:

```bash
# Download and run the setup script
curl -sL https://raw.githubusercontent.com/mikecranesync/jarvis/main/installers/raspberry-pi/first-boot.sh | sudo bash
```

**Or manually:**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3-pip python3-venv git curl

# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

# Create Jarvis Node directory
sudo mkdir -p /opt/jarvis-node
cd /opt/jarvis-node

# Create virtual environment
sudo python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install fastapi uvicorn pillow requests psutil

# If using camera:
sudo apt install -y libcamera-apps python3-picamera2
pip install picamera2

# Download Jarvis Node script
sudo curl -o jarvis_node_pi.py https://raw.githubusercontent.com/.../jarvis_node_pi.py

# Create systemd service (see script in installers/)
# Enable and start
sudo systemctl enable jarvis-node
sudo systemctl start jarvis-node
```

---

## Part 4: Connect to Tailscale

```bash
sudo tailscale up
```

Follow the URL to authenticate, then the Pi will appear in your Tailscale network.

Get the Tailscale IP:
```bash
tailscale ip -4
```

---

## Part 5: Add VPS SSH Key

```bash
# Create SSH directory
mkdir -p ~/.ssh

# Add VPS public key
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOY0hljziGSbgrv8E/wmCXovYypHw1IKWX5XYyw/hqvY root@srv1078052" >> ~/.ssh/authorized_keys

# Set permissions
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

---

## Part 6: Test from VPS

```bash
# From VPS, test SSH
ssh pi@<pi-tailscale-ip> "hostname && uname -a"

# Test Jarvis Node API
curl http://<pi-tailscale-ip>:8765/health
```

---

## API Endpoints

Once Jarvis Node is running, these endpoints are available:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Basic status |
| `/health` | GET | Detailed health (CPU, memory, temp) |
| `/shell` | POST | Run shell command |
| `/camera/photo` | GET | Take photo (if camera installed) |
| `/gpio` | POST | Control GPIO pin |
| `/gpio/{pin}` | GET | Read GPIO pin |
| `/system` | GET | System information |

### Examples:

```bash
# Health check
curl http://pi:8765/health

# Run command
curl -X POST http://pi:8765/shell -H "Content-Type: application/json" -d '{"command": "ls -la"}'

# Take photo
curl http://pi:8765/camera/photo | jq -r .image_base64 | base64 -d > photo.jpg

# Set GPIO pin high
curl -X POST http://pi:8765/gpio -H "Content-Type: application/json" -d '{"pin": 17, "mode": "OUT", "value": 1}'

# Read GPIO pin
curl http://pi:8765/gpio/17
```

---

## Troubleshooting

### Can't find Pi on network

1. Check ethernet lights are blinking
2. Try `ping raspberrypi.local`
3. Check router DHCP leases
4. Use `nmap -sn 192.168.1.0/24` to scan subnet

### SSH connection refused

1. Ensure SSH is enabled:
   ```bash
   sudo systemctl enable ssh
   sudo systemctl start ssh
   ```

2. Check if sshd is running:
   ```bash
   sudo systemctl status ssh
   ```

### Jarvis Node not starting

1. Check service status:
   ```bash
   sudo systemctl status jarvis-node
   ```

2. Check logs:
   ```bash
   sudo journalctl -u jarvis-node -f
   ```

3. Test manually:
   ```bash
   cd /opt/jarvis-node
   source venv/bin/activate
   python jarvis_node_pi.py
   ```

### Camera not working

1. Enable camera in raspi-config:
   ```bash
   sudo raspi-config
   # Interface Options → Camera → Enable
   ```

2. Test camera:
   ```bash
   libcamera-still -o test.jpg
   ```

---

## GPIO Pinout Reference

```
                    3.3V  (1) (2)  5V
          GPIO 2 (SDA)  (3) (4)  5V
          GPIO 3 (SCL)  (5) (6)  GND
               GPIO 4  (7) (8)  GPIO 14 (TXD)
                  GND  (9) (10) GPIO 15 (RXD)
              GPIO 17 (11) (12) GPIO 18 (PCM_CLK)
              GPIO 27 (13) (14) GND
              GPIO 22 (15) (16) GPIO 23
                 3.3V (17) (18) GPIO 24
    GPIO 10 (SPI_MOSI) (19) (20) GND
     GPIO 9 (SPI_MISO) (21) (22) GPIO 25
    GPIO 11 (SPI_SCLK) (23) (24) GPIO 8 (SPI_CE0)
                  GND (25) (26) GPIO 7 (SPI_CE1)
              GPIO 0  (27) (28) GPIO 1
              GPIO 5  (29) (30) GND
              GPIO 6  (31) (32) GPIO 12
             GPIO 13  (33) (34) GND
             GPIO 19  (35) (36) GPIO 16
             GPIO 26  (37) (38) GPIO 20
                  GND (39) (40) GPIO 21
```

---

## Useful Commands

```bash
# Check CPU temperature
vcgencmd measure_temp

# Check memory
free -h

# Check disk space
df -h

# Check Tailscale status
tailscale status

# View Jarvis Node logs
sudo journalctl -u jarvis-node -f

# Restart Jarvis Node
sudo systemctl restart jarvis-node
```
