#!/usr/bin/env python3
"""
VFD Modbus TCP Server
=====================
Provides Modbus TCP interface to the VFD Simulator.
Allows PLCs to communicate with the simulated VFD.

Author: Jarvis Agent for FactoryLM
Created: 2026-02-06
Issue: #27
"""

import asyncio
import logging
import struct
from typing import Optional

from vfd_simulator import (
    VFDSimulator, VFDParameters, ModbusRegisters,
    VFDCommand, VFDStatus, VFDFault
)

logger = logging.getLogger("Modbus-Server")


class ModbusTCPServer:
    """
    Modbus TCP Server wrapping VFD Simulator
    
    Implements Modbus TCP protocol for:
    - Function 03: Read Holding Registers
    - Function 06: Write Single Register
    - Function 16: Write Multiple Registers
    """
    
    MBAP_HEADER_SIZE = 7
    
    def __init__(self, vfd: VFDSimulator, host: str = "0.0.0.0", port: int = 502):
        self.vfd = vfd
        self.host = host
        self.port = port
        self._server: Optional[asyncio.Server] = None
        self._running = False
        
        # Initialize register storage (100 registers)
        self._registers = [0] * 100
        
        # Connect VFD state to registers
        self.vfd.add_callback(self._update_registers)
    
    def _update_registers(self, state):
        """Update Modbus registers from VFD state"""
        self._registers[ModbusRegisters.STATUS_WORD] = state.status_word
        self._registers[ModbusRegisters.OUTPUT_FREQ] = int(state.output_frequency * 10)
        self._registers[ModbusRegisters.OUTPUT_CURRENT] = int(state.output_current * 10)
        self._registers[ModbusRegisters.OUTPUT_VOLTAGE] = int(state.output_voltage)
        self._registers[ModbusRegisters.DC_BUS_VOLTAGE] = int(state.dc_bus_voltage)
        self._registers[ModbusRegisters.MOTOR_RPM] = int(state.motor_rpm)
        self._registers[ModbusRegisters.FAULT_CODE] = state.fault_code
        
        # Run time as two registers (hours)
        run_hours = int(state.run_time)
        run_fraction = int((state.run_time - run_hours) * 100)
        self._registers[ModbusRegisters.RUN_TIME_H] = run_hours
        self._registers[ModbusRegisters.RUN_TIME_L] = run_fraction
    
    def _process_write(self, address: int, value: int):
        """Process a write to a register"""
        self._registers[address] = value
        
        if address == ModbusRegisters.COMMAND_WORD:
            self.vfd.write_command(value)
            logger.info(f"Command Word written: {value:#06x}")
        elif address == ModbusRegisters.SPEED_REF:
            self.vfd.write_speed_reference(value)
            logger.info(f"Speed Reference written: {value}")
    
    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Handle a Modbus TCP client connection"""
        addr = writer.get_extra_info('peername')
        logger.info(f"Client connected: {addr}")
        
        try:
            while self._running:
                # Read MBAP header
                header = await reader.read(self.MBAP_HEADER_SIZE)
                if not header:
                    break
                
                if len(header) < self.MBAP_HEADER_SIZE:
                    continue
                
                # Parse MBAP header
                transaction_id = struct.unpack('>H', header[0:2])[0]
                protocol_id = struct.unpack('>H', header[2:4])[0]
                length = struct.unpack('>H', header[4:6])[0]
                unit_id = header[6]
                
                if protocol_id != 0:  # Not Modbus
                    continue
                
                # Read PDU
                pdu = await reader.read(length - 1)
                if not pdu:
                    break
                
                function_code = pdu[0]
                response_pdu = self._process_request(function_code, pdu[1:])
                
                # Build response
                response_header = struct.pack(
                    '>HHHB',
                    transaction_id,
                    protocol_id,
                    len(response_pdu) + 1,
                    unit_id
                )
                
                writer.write(response_header + response_pdu)
                await writer.drain()
                
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Client error: {e}")
        finally:
            writer.close()
            await writer.wait_closed()
            logger.info(f"Client disconnected: {addr}")
    
    def _process_request(self, function_code: int, data: bytes) -> bytes:
        """Process Modbus request and return response PDU"""
        
        if function_code == 0x03:  # Read Holding Registers
            return self._read_holding_registers(data)
        elif function_code == 0x06:  # Write Single Register
            return self._write_single_register(data)
        elif function_code == 0x10:  # Write Multiple Registers
            return self._write_multiple_registers(data)
        else:
            # Illegal function
            return bytes([function_code | 0x80, 0x01])
    
    def _read_holding_registers(self, data: bytes) -> bytes:
        """Handle Read Holding Registers (0x03)"""
        start_address = struct.unpack('>H', data[0:2])[0]
        quantity = struct.unpack('>H', data[2:4])[0]
        
        if start_address + quantity > len(self._registers):
            return bytes([0x83, 0x02])  # Illegal data address
        
        # Build response
        byte_count = quantity * 2
        response = bytes([0x03, byte_count])
        
        for i in range(quantity):
            value = self._registers[start_address + i]
            response += struct.pack('>H', value)
        
        return response
    
    def _write_single_register(self, data: bytes) -> bytes:
        """Handle Write Single Register (0x06)"""
        address = struct.unpack('>H', data[0:2])[0]
        value = struct.unpack('>H', data[2:4])[0]
        
        if address >= len(self._registers):
            return bytes([0x86, 0x02])  # Illegal data address
        
        self._process_write(address, value)
        
        # Echo request as response
        return bytes([0x06]) + data[0:4]
    
    def _write_multiple_registers(self, data: bytes) -> bytes:
        """Handle Write Multiple Registers (0x10)"""
        start_address = struct.unpack('>H', data[0:2])[0]
        quantity = struct.unpack('>H', data[2:4])[0]
        byte_count = data[4]
        
        if start_address + quantity > len(self._registers):
            return bytes([0x90, 0x02])  # Illegal data address
        
        # Process each register
        for i in range(quantity):
            offset = 5 + (i * 2)
            value = struct.unpack('>H', data[offset:offset+2])[0]
            self._process_write(start_address + i, value)
        
        # Response: function code, start address, quantity
        return bytes([0x10]) + data[0:4]
    
    async def start(self):
        """Start the Modbus TCP server"""
        self._running = True
        self._server = await asyncio.start_server(
            self._handle_client,
            self.host,
            self.port
        )
        
        addr = self._server.sockets[0].getsockname()
        logger.info(f"Modbus TCP Server listening on {addr[0]}:{addr[1]}")
        
        async with self._server:
            await self._server.serve_forever()
    
    def stop(self):
        """Stop the server"""
        self._running = False
        if self._server:
            self._server.close()


async def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="VFD Modbus TCP Simulator")
    parser.add_argument("--host", default="0.0.0.0", help="Bind address")
    parser.add_argument("--port", type=int, default=502, help="Modbus TCP port")
    parser.add_argument("--motor-hp", type=float, default=0.5, help="Motor HP")
    parser.add_argument("--motor-voltage", type=int, default=230, help="Motor voltage")
    args = parser.parse_args()
    
    # Configure VFD parameters
    params = VFDParameters(
        motor_hp=args.motor_hp,
        motor_voltage=args.motor_voltage
    )
    
    # Create VFD and server
    vfd = VFDSimulator(params)
    server = ModbusTCPServer(vfd, host=args.host, port=args.port)
    
    # Run both VFD simulation and Modbus server
    try:
        await asyncio.gather(
            vfd.run_async(interval=0.1),
            server.start()
        )
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        vfd.stop()
        server.stop()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    asyncio.run(main())
