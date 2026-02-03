FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    iputils-ping \
    net-tools \
    curl \
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

# Expose API port
EXPOSE 5000

# Run the gateway
CMD ["python", "main.py"]
