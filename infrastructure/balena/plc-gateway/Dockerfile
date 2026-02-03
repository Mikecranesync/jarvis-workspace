FROM python:3.11-slim

# Install system dependencies including dnsmasq for DHCP
RUN apt-get update && apt-get install -y \
    gcc \
    iputils-ping \
    net-tools \
    curl \
    dnsmasq \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install --no-cache-dir \
    pycomm3 \
    paho-mqtt \
    flask \
    requests \
    python-dotenv \
    schedule

# Create app directory
WORKDIR /app

# Copy application code
COPY app/ /app/

# Copy dnsmasq config
COPY dnsmasq.conf /etc/dnsmasq.conf

# Expose API port
EXPOSE 5000

# Start script that runs dnsmasq + app
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
