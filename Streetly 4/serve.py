#!/usr/bin/env python3
"""
Simple HTTP server to serve the Streetly frontend
"""

import http.server
import socketserver
import os
import sys

PORT = 8001

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.end_headers()

if __name__ == "__main__":
    # Change to the directory containing the HTML files
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🚀 Streetly Frontend Server running at http://localhost:{PORT}")
        print(f"📁 Serving files from: {os.getcwd()}")
        print(f"🗺️  Open map.html at: http://localhost:{PORT}/map.html")
        print("Press Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped")
            sys.exit(0)
