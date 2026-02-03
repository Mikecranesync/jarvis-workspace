FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc iputils-ping iputils-arping net-tools iproute2 tcpdump dnsmasq procps \
    && rm -rf /var/lib/apt/lists/*

# PLC Communication Libraries
RUN pip install --no-cache-dir \
    pycomm3 \
    pymodbus>=3.6.0 \
    paho-mqtt \
    flask \
    requests \
    python-dotenv \
    schedule

WORKDIR /app
COPY app/ /app/
COPY dnsmasq.conf /etc/dnsmasq.conf
COPY start.sh /start.sh
COPY keepalive.sh /app/keepalive.sh
RUN chmod +x /start.sh /app/keepalive.sh

EXPOSE 5000
CMD ["/start.sh"]
