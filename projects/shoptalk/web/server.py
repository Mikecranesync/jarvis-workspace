#!/usr/bin/env python3
"""
Simple web server for ShopTalk demo.
Serves the static demo page and proxies to the API server.
"""

import http.server
import socketserver
import os

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

if __name__ == "__main__":
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"ShopTalk Demo Server")
        print(f"=" * 40)
        print(f"Serving at: http://localhost:{PORT}")
        print(f"Directory: {DIRECTORY}")
        print(f"\nPress Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")
