#!/usr/bin/env python3
"""
Web Interface for Industrial Gateway
Provides configuration UI, real-time data dashboard, and REST API
"""

from quart import Quart, render_template, jsonify, request
import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger('web')


def create_app(tag_db, adapters: Dict, config: Dict) -> Quart:
    """Create the Quart web application"""
    
    app = Quart(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Store references
    app.tag_db = tag_db
    app.adapters = adapters
    app.gateway_config = config
    
    # ============== Web Pages ==============
    
    @app.route('/')
    async def index():
        """Dashboard page"""
        return await render_template('index.html',
            gateway_name=config.get('gateway', {}).get('name', 'Industrial Gateway'),
            adapters=adapters
        )
    
    @app.route('/config')
    async def config_page():
        """Configuration page"""
        return await render_template('config.html',
            config=config
        )
    
    # ============== REST API ==============
    
    @app.route('/api/status')
    async def api_status():
        """Get gateway status"""
        adapter_status = {}
        for name, adapter in adapters.items():
            adapter_status[name] = {
                'connected': adapter.connected,
                'running': adapter.running,
                'host': adapter.config.get('host', 'N/A'),
                'protocol': adapter.config.get('protocol', 'unknown')
            }
        
        return jsonify({
            'status': 'running',
            'timestamp': datetime.now().isoformat(),
            'adapters': adapter_status,
            'tag_count': len(tag_db.get_tag_names())
        })
    
    @app.route('/api/tags')
    async def api_tags():
        """Get all tag values"""
        tags = await tag_db.read_all()
        return jsonify({
            'timestamp': datetime.now().isoformat(),
            'tags': tags
        })
    
    @app.route('/api/tags/<tag_name>')
    async def api_tag(tag_name: str):
        """Get a specific tag value"""
        tag = await tag_db.read(tag_name)
        if tag:
            return jsonify({
                'name': tag_name,
                **tag.to_dict()
            })
        else:
            return jsonify({'error': 'Tag not found'}), 404
    
    @app.route('/api/tags/<tag_name>', methods=['POST'])
    async def api_write_tag(tag_name: str):
        """Write a value to a tag"""
        data = await request.get_json()
        value = data.get('value')
        
        if value is None:
            return jsonify({'error': 'Value required'}), 400
        
        # Find the adapter that owns this tag and write to it
        for adapter in adapters.values():
            if any(t.name == tag_name for t in getattr(adapter, 'tags', [])):
                success = await adapter.write_tag(tag_name, value)
                if success:
                    return jsonify({'status': 'ok', 'tag': tag_name, 'value': value})
                else:
                    return jsonify({'error': 'Write failed'}), 500
        
        return jsonify({'error': 'Tag not found in any adapter'}), 404
    
    @app.route('/api/adapters')
    async def api_adapters():
        """Get adapter information"""
        result = {}
        for name, adapter in adapters.items():
            result[name] = {
                'connected': adapter.connected,
                'running': adapter.running,
                'config': {
                    'host': adapter.config.get('host'),
                    'protocol': adapter.config.get('protocol'),
                    'scan_rate': adapter.config.get('scan_rate', 1.0)
                },
                'tags': [t.name for t in getattr(adapter, 'tags', [])]
            }
        return jsonify(result)
    
    @app.route('/api/config', methods=['GET'])
    async def api_get_config():
        """Get current configuration"""
        return jsonify(config)
    
    @app.route('/api/config', methods=['POST'])
    async def api_set_config():
        """Update configuration (requires restart)"""
        new_config = await request.get_json()
        
        # Save to file
        import yaml
        with open('config/gateway.yaml', 'w') as f:
            yaml.dump(new_config, f, default_flow_style=False)
        
        return jsonify({
            'status': 'ok',
            'message': 'Configuration saved. Restart gateway to apply changes.'
        })
    
    # ============== WebSocket for real-time updates ==============
    
    @app.websocket('/ws/tags')
    async def ws_tags():
        """WebSocket endpoint for real-time tag updates"""
        import asyncio
        
        try:
            while True:
                tags = await tag_db.read_all()
                await websocket.send_json({
                    'type': 'update',
                    'timestamp': datetime.now().isoformat(),
                    'tags': tags
                })
                await asyncio.sleep(0.5)
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
    
    return app


# ============== HTML Templates (inline for simplicity) ==============

TEMPLATES = {
    'index.html': '''
<!DOCTYPE html>
<html>
<head>
    <title>{{ gateway_name }}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #1a1a2e; color: #eee; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        header { background: #16213e; padding: 20px; margin-bottom: 20px; border-radius: 8px; }
        h1 { font-size: 24px; margin-bottom: 10px; }
        .status { display: inline-block; padding: 4px 12px; border-radius: 4px; font-size: 12px; }
        .status.online { background: #00c853; color: #000; }
        .status.offline { background: #ff5252; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
        .card { background: #16213e; border-radius: 8px; padding: 20px; }
        .card h2 { font-size: 18px; margin-bottom: 15px; color: #0f4c75; }
        .tag-list { max-height: 300px; overflow-y: auto; }
        .tag { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #2a3f5f; }
        .tag-name { color: #aaa; }
        .tag-value { font-family: monospace; color: #4fc3f7; }
        #refresh { background: #0f4c75; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🏭 {{ gateway_name }}</h1>
            <span class="status online" id="status">Connected</span>
            <button id="refresh" style="float: right;">Refresh</button>
        </header>
        
        <div class="grid" id="adapters">
            <!-- Adapters will be loaded here -->
        </div>
        
        <div class="card" style="margin-top: 20px;">
            <h2>📊 All Tags</h2>
            <div class="tag-list" id="tags">
                <!-- Tags will be loaded here -->
            </div>
        </div>
    </div>
    
    <script>
        async function loadData() {
            try {
                // Load adapters
                const adaptersRes = await fetch('/api/adapters');
                const adapters = await adaptersRes.json();
                
                let adaptersHtml = '';
                for (const [name, info] of Object.entries(adapters)) {
                    adaptersHtml += `
                        <div class="card">
                            <h2>${name}</h2>
                            <p>Protocol: ${info.config.protocol}</p>
                            <p>Host: ${info.config.host}</p>
                            <p>Status: <span class="status ${info.connected ? 'online' : 'offline'}">${info.connected ? 'Connected' : 'Disconnected'}</span></p>
                            <p>Tags: ${info.tags.length}</p>
                        </div>
                    `;
                }
                document.getElementById('adapters').innerHTML = adaptersHtml;
                
                // Load tags
                const tagsRes = await fetch('/api/tags');
                const data = await tagsRes.json();
                
                let tagsHtml = '';
                for (const [name, info] of Object.entries(data.tags)) {
                    tagsHtml += `
                        <div class="tag">
                            <span class="tag-name">${name}</span>
                            <span class="tag-value">${info.value}</span>
                        </div>
                    `;
                }
                document.getElementById('tags').innerHTML = tagsHtml || '<p>No tags yet</p>';
                
            } catch (e) {
                document.getElementById('status').className = 'status offline';
                document.getElementById('status').textContent = 'Error';
            }
        }
        
        document.getElementById('refresh').onclick = loadData;
        loadData();
        setInterval(loadData, 2000);
    </script>
</body>
</html>
''',
    'config.html': '''
<!DOCTYPE html>
<html>
<head>
    <title>Gateway Configuration</title>
    <style>
        body { font-family: sans-serif; background: #1a1a2e; color: #eee; padding: 20px; }
        pre { background: #16213e; padding: 20px; border-radius: 8px; overflow: auto; }
    </style>
</head>
<body>
    <h1>Configuration</h1>
    <pre>{{ config | tojson(indent=2) }}</pre>
    <p><a href="/" style="color: #4fc3f7;">← Back to Dashboard</a></p>
</body>
</html>
'''
}

# Write templates to files
def ensure_templates():
    import os
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(template_dir, exist_ok=True)
    for name, content in TEMPLATES.items():
        path = os.path.join(template_dir, name)
        if not os.path.exists(path):
            with open(path, 'w') as f:
                f.write(content)

ensure_templates()
