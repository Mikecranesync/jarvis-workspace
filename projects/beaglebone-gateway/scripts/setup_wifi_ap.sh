#!/bin/bash
#
# Wi-Fi Access Point Setup Script
# Creates a Wi-Fi network that laptops can connect to
#
# Usage: sudo ./setup_wifi_ap.sh [SSID] [PASSWORD]
#

set -e

SSID="${1:-IndustrialGateway}"
PASSWORD="${2:-FactoryLM2026}"
INTERFACE="${3:-wlan0}"

echo "============================================"
echo "  Wi-Fi Access Point Setup"
echo "============================================"
echo ""
echo "SSID: $SSID"
echo "Interface: $INTERFACE"
echo ""

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root: sudo ./setup_wifi_ap.sh"
    exit 1
fi

# Install required packages
echo "[1/5] Installing hostapd and dnsmasq..."
apt install -y hostapd dnsmasq

# Stop services during configuration
systemctl stop hostapd 2>/dev/null || true
systemctl stop dnsmasq 2>/dev/null || true

# Configure hostapd
echo "[2/5] Configuring hostapd..."
cat > /etc/hostapd/hostapd.conf << EOF
interface=$INTERFACE
driver=nl80211
ssid=$SSID
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=$PASSWORD
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
EOF

# Point hostapd to config
sed -i 's|#DAEMON_CONF=""|DAEMON_CONF="/etc/hostapd/hostapd.conf"|' /etc/default/hostapd

# Configure dnsmasq
echo "[3/5] Configuring dnsmasq..."
mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig 2>/dev/null || true
cat > /etc/dnsmasq.conf << EOF
interface=$INTERFACE
dhcp-range=192.168.50.10,192.168.50.50,255.255.255.0,24h
domain=local
address=/gateway.local/192.168.50.1
EOF

# Configure static IP for Wi-Fi interface
echo "[4/5] Configuring network interface..."
cat > /etc/network/interfaces.d/$INTERFACE << EOF
auto $INTERFACE
iface $INTERFACE inet static
    address 192.168.50.1
    netmask 255.255.255.0
EOF

# Enable IP forwarding and NAT (optional - for internet sharing)
echo "[5/5] Configuring routing..."
echo "net.ipv4.ip_forward=1" > /etc/sysctl.d/90-ip-forward.conf
sysctl -p /etc/sysctl.d/90-ip-forward.conf

# Optional: NAT for internet sharing through eth0
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
iptables -A FORWARD -i eth0 -o $INTERFACE -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i $INTERFACE -o eth0 -j ACCEPT

# Save iptables rules
iptables-save > /etc/iptables.rules

# Create restore script
cat > /etc/network/if-pre-up.d/iptables << 'EOF'
#!/bin/sh
iptables-restore < /etc/iptables.rules
EOF
chmod +x /etc/network/if-pre-up.d/iptables

# Unmask and enable services
systemctl unmask hostapd
systemctl enable hostapd
systemctl enable dnsmasq

# Start services
echo ""
echo "Starting services..."
systemctl start hostapd
systemctl start dnsmasq

echo ""
echo "============================================"
echo "  Wi-Fi Access Point Setup Complete!"
echo "============================================"
echo ""
echo "Network Information:"
echo "  SSID: $SSID"
echo "  Password: $PASSWORD"
echo "  Gateway IP: 192.168.50.1"
echo "  DHCP Range: 192.168.50.10 - 192.168.50.50"
echo ""
echo "Connect your laptop to '$SSID' and access:"
echo "  Web Interface: http://192.168.50.1:8080"
echo "  OPC UA: opc.tcp://192.168.50.1:4840"
echo ""
echo "To check status:"
echo "  systemctl status hostapd"
echo "  systemctl status dnsmasq"
echo ""
