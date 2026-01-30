#!/usr/bin/env python3
"""
Modbus TCP Simulator for Testing
Runs a Modbus server with simulated values
"""

import asyncio
import random
import time
from pymodbus.server import StartAsyncTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock


async def updating_writer(context):
    """Update register values periodically"""
    counter = 0
    while True:
        # Get the slave context
        slave_id = 1
        register = 3  # Holding registers
        
        # Update demo values
        counter = (counter + 1) % 65536
        random_val = random.randint(0, 1000)
        
        # Write to registers
        context[slave_id].setValues(register, 0, [counter])
        context[slave_id].setValues(register, 1, [random_val])
        context[slave_id].setValues(register, 2, [int(time.time()) % 65536])
        
        await asyncio.sleep(1)


async def run_server():
    """Start the Modbus TCP server"""
    
    # Create data store
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0] * 100),  # Discrete inputs
        co=ModbusSequentialDataBlock(0, [0] * 100),  # Coils
        hr=ModbusSequentialDataBlock(0, [0] * 100),  # Holding registers
        ir=ModbusSequentialDataBlock(0, [0] * 100)   # Input registers
    )
    context = ModbusServerContext(slaves=store, single=True)
    
    # Device identification
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'FactoryLM'
    identity.ProductCode = 'SimPLC'
    identity.VendorUrl = 'https://factorylm.com'
    identity.ProductName = 'Modbus Simulator'
    identity.ModelName = 'SimPLC-1000'
    
    # Start updating task
    asyncio.create_task(updating_writer(context))
    
    print("Starting Modbus TCP Simulator on port 5020...")
    print("Registers:")
    print("  HR 0: Counter (increments)")
    print("  HR 1: Random value (0-1000)")
    print("  HR 2: Timestamp (lower 16 bits)")
    print()
    
    await StartAsyncTcpServer(
        context=context,
        identity=identity,
        address=("0.0.0.0", 5020)
    )


if __name__ == "__main__":
    asyncio.run(run_server())
