#!/usr/bin/env python3
"""
Simple HTTP server to serve the Streetly frontend
This serves your exact frontend files without any changes
"""

import http.server
import socketserver
import os
import sys

# Change to the directory containing this script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

PORT = 3001

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers to allow API calls to your backend
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

if __name__ == "__main__":
    print("🚀 Starting Streetly Frontend Server...")
    print(f"📁 Serving files from: {os.getcwd()}")
    print(f"🌐 Access your frontend at: http://localhost:{PORT}")
    print("📋 Your exact UI will be displayed with no changes")
    print("🔗 Backend API should be running on: http://localhost:8080")
    print("")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped.")
        sys.exit(0)
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {PORT} is already in use. Please stop any other servers on this port.")
        else:
            print(f"❌ Error starting server: {e}")
        sys.exit(1)
