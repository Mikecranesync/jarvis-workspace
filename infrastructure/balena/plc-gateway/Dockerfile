FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    iputils-ping \
    iputils-arping \
    net-tools \
    iproute2 \
    tcpdump \
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

# Start script
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
