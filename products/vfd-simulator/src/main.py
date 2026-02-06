#!/usr/bin/env python3
"""
VFD Simulator - Main Entry Point
=================================
Starts the VFD simulator with Modbus TCP server and Web UI.

Usage:
    python main.py [--modbus-port 502] [--web-port 8080]

Author: Jarvis Agent for FactoryLM
Created: 2026-02-06
Issue: #27
"""

import asyncio
import argparse
import logging
import signal
import sys

from vfd_simulator import VFDSimulator, VFDParameters, VFDCommand
from modbus_server import ModbusTCPServer
from web_ui import WebUI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("VFD-Main")


def print_banner():
    """Print startup banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║     ██╗   ██╗███████╗██████╗     ███████╗██╗███╗   ███╗  ║
    ║     ██║   ██║██╔════╝██╔══██╗    ██╔════╝██║████╗ ████║  ║
    ║     ██║   ██║█████╗  ██║  ██║    ███████╗██║██╔████╔██║  ║
    ║     ╚██╗ ██╔╝██╔══╝  ██║  ██║    ╚════██║██║██║╚██╔╝██║  ║
    ║      ╚████╔╝ ██║     ██████╔╝    ███████║██║██║ ╚═╝ ██║  ║
    ║       ╚═══╝  ╚═╝     ╚═════╝     ╚══════╝╚═╝╚═╝     ╚═╝  ║
    ║                                                           ║
    ║            Variable Frequency Drive Simulator             ║
    ║                      FactoryLM Demo                       ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


async def main(args):
    """Main entry point"""
    print_banner()
    
    # Create VFD parameters
    params = VFDParameters(
        motor_hp=args.motor_hp,
        motor_voltage=args.motor_voltage,
        motor_amps=args.motor_amps,
        base_frequency=args.base_freq,
        max_frequency=args.max_freq,
        accel_time=args.accel_time,
        decel_time=args.decel_time
    )
    
    # Create simulator
    vfd = VFDSimulator(params)
    
    # Create servers
    modbus_server = ModbusTCPServer(vfd, host="0.0.0.0", port=args.modbus_port)
    web_ui = WebUI(vfd, host="0.0.0.0", port=args.web_port)
    
    # Print configuration
    logger.info("=" * 60)
    logger.info("VFD Simulator Configuration:")
    logger.info(f"  Motor: {params.motor_hp} HP, {params.motor_voltage}V, {params.motor_amps}A")
    logger.info(f"  Frequency Range: {params.min_frequency}-{params.max_frequency} Hz")
    logger.info(f"  Accel/Decel: {params.accel_time}s / {params.decel_time}s")
    logger.info("=" * 60)
    logger.info(f"Modbus TCP Server: port {args.modbus_port}")
    logger.info(f"Web UI: http://localhost:{args.web_port}")
    logger.info("=" * 60)
    
    # Setup shutdown handler
    shutdown_event = asyncio.Event()
    
    def handle_shutdown(sig):
        logger.info(f"Received signal {sig}, shutting down...")
        shutdown_event.set()
    
    # Register signal handlers
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, lambda s=sig: handle_shutdown(s))
        except NotImplementedError:
            # Windows doesn't support add_signal_handler
            pass
    
    # Start all tasks
    try:
        await asyncio.gather(
            vfd.run_async(interval=0.1),
            modbus_server.start(),
            web_ui.start(),
            shutdown_event.wait()
        )
    except asyncio.CancelledError:
        pass
    finally:
        logger.info("Shutting down...")
        vfd.stop()
        modbus_server.stop()


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="VFD Simulator - Variable Frequency Drive Emulator",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Server options
    parser.add_argument("--modbus-port", type=int, default=502,
                        help="Modbus TCP port")
    parser.add_argument("--web-port", type=int, default=8080,
                        help="Web UI port")
    
    # Motor parameters
    parser.add_argument("--motor-hp", type=float, default=0.5,
                        help="Motor horsepower")
    parser.add_argument("--motor-voltage", type=int, default=230,
                        help="Motor voltage")
    parser.add_argument("--motor-amps", type=float, default=2.0,
                        help="Motor full load amps")
    
    # Drive parameters
    parser.add_argument("--base-freq", type=float, default=60.0,
                        help="Base frequency (Hz)")
    parser.add_argument("--max-freq", type=float, default=60.0,
                        help="Maximum frequency (Hz)")
    parser.add_argument("--accel-time", type=float, default=5.0,
                        help="Acceleration time (seconds)")
    parser.add_argument("--decel-time", type=float, default=5.0,
                        help="Deceleration time (seconds)")
    
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    
    try:
        asyncio.run(main(args))
    except KeyboardInterrupt:
        print("\nShutdown complete.")
        sys.exit(0)
