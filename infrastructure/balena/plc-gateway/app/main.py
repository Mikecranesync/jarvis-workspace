#!/usr/bin/env python3
"""FactoryLM PLC Gateway v2.4 - Complete with tag listing"""

import os
from datetime import datetime
from flask import Flask, jsonify, request

try:
    from pycomm3 import LogixDriver
    PYCOMM3_AVAILABLE = True
except ImportError:
    PYCOMM3_AVAILABLE = False

try:
    from pymodbus.client import ModbusTcpClient
    PYMODBUS_AVAILABLE = True
except ImportError:
    PYMODBUS_AVAILABLE = False

app = Flask(__name__)
PLC_IP = os.getenv('PLC_IP', '192.168.1.100')
DEVICE_ID = os.getenv('DEVICE_ID', 'edge-pi-001')

plc_client = None
plc_protocol = None
plc_connected = False

def connect_plc():
    global plc_client, plc_connected, plc_protocol
    print(f"Connecting to {PLC_IP}...")
    
    if PYCOMM3_AVAILABLE:
        try:
            plc_client = LogixDriver(PLC_IP)
            plc_client.open()
            plc_connected = True
            plc_protocol = 'ethernetip'
            print("Connected via EtherNet/IP")
            return True
        except Exception as e:
            print(f"EtherNet/IP failed: {e}")
    
    plc_connected = False
    return False

def read_tag(tag):
    if not plc_connected: return None
    try:
        result = plc_client.read(tag)
        return result.value if result else None
    except: return None

def write_tag(tag, value):
    if not plc_connected: return False
    try:
        if isinstance(value, str):
            value = value.lower() in ['true','1','on']
        result = plc_client.write(tag, value)
        return result is not None
    except: return False

@app.route('/')
def index():
    return jsonify({
        'service': 'FactoryLM PLC Gateway', 'version': '2.4.0',
        'device': DEVICE_ID, 'plc_ip': PLC_IP,
        'plc_protocol': plc_protocol, 'plc_connected': plc_connected,
        'pycomm3': PYCOMM3_AVAILABLE, 'pymodbus': PYMODBUS_AVAILABLE
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'plc_connected': plc_connected})

@app.route('/plc/connect', methods=['POST'])
def api_connect():
    return jsonify({'success': connect_plc(), 'connected': plc_connected, 'protocol': plc_protocol})

@app.route('/plc/read/<path:tag>')
def api_read(tag):
    if not plc_connected: return jsonify({'error': 'Not connected'}), 503
    return jsonify({'tag': tag, 'value': read_tag(tag), 'timestamp': datetime.now().isoformat()})

@app.route('/plc/write', methods=['POST'])
def api_write():
    if not plc_connected: return jsonify({'error': 'Not connected'}), 503
    data = request.get_json()
    return jsonify({'success': write_tag(data['tag'], data['value']), 'tag': data['tag'], 'value': data['value']})

@app.route('/plc/set/<output>/<state>', methods=['POST'])
def set_output(output, state):
    if not plc_connected: return jsonify({'error': 'Not connected'}), 503
    tag = f"_IO_EM_DO_{output.zfill(2)}"
    value = state.lower() in ['on','true','1']
    return jsonify({'tag': tag, 'value': value, 'success': write_tag(tag, value)})

@app.route('/plc/info')
def plc_info():
    if not plc_connected: return jsonify({'error': 'Not connected'}), 503
    try:
        info = plc_client.info
        return jsonify(dict(info) if info else {'protocol': plc_protocol})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/plc/tags')
def list_tags():
    if not plc_connected: return jsonify({'error': 'Not connected'}), 503
    try:
        tags = plc_client.get_tag_list()
        return jsonify({
            'count': len(tags),
            'tags': [{'name': t['tag_name'], 'type': str(t.get('data_type','?'))} for t in tags]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/plc/programs')
def list_programs():
    if not plc_connected: return jsonify({'error': 'Not connected'}), 503
    try:
        programs = plc_client.get_program_tag_list('MainProgram')
        return jsonify({'programs': [str(p) for p in programs]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print(f"Starting Gateway v2.4 - PLC: {PLC_IP}")
    connect_plc()
    app.run(host='0.0.0.0', port=5000, threaded=True)
