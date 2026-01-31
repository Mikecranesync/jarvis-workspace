# ShopTalk Edge AI - Makefile

.PHONY: install test demo demo-es api clean help

# Default target
help:
	@echo "ShopTalk Edge AI"
	@echo ""
	@echo "Usage:"
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Run quick component test"
	@echo "  make demo       - Run full demo (English)"
	@echo "  make demo-es    - Run full demo (Spanish)"
	@echo "  make api        - Start API server"
	@echo "  make clean      - Clean up temp files"

# Install dependencies
install:
	pip3 install -r requirements.txt --break-system-packages

# Run quick test
test:
	python3 demo.py --test

# Run demo
demo:
	python3 demo.py --scenario jam

# Run demo in Spanish
demo-es:
	python3 demo.py --scenario jam --language es --voice

# Run demo with all scenarios
demo-all:
	@echo "=== Normal Operation ==="
	python3 main.py --simulate --scenario normal --samples 50
	@echo ""
	@echo "=== Conveyor Jam ==="
	python3 main.py --simulate --scenario jam --samples 150
	@echo ""
	@echo "=== Overload ==="
	python3 main.py --simulate --scenario overload --samples 150

# Start API server (simulation mode)
api:
	python3 main.py --api --simulate

# Start API server with PLC
api-plc:
	python3 main.py --api --host $(PLC_HOST) --port $(PLC_PORT)

# Run world model test
test-model:
	python3 src/model/world_model.py

# Clean temp files
clean:
	rm -rf __pycache__ src/__pycache__ src/*/__pycache__
	rm -rf data/*.csv data/*.json
	rm -rf /tmp/shoptalk_audio/*

# Build for deployment (create single directory with all deps)
build:
	mkdir -p dist
	cp -r src dist/
	cp main.py demo.py requirements.txt dist/
	@echo "Build complete in dist/"
