import http.server
import socketserver
import os
from pathlib import Path

def serve(directory="_site", port=8000):
    """Serve a directory with a simple HTTP server"""
    directory = Path(directory)
    
    if not directory.exists():
        print(f"Directory {directory} does not exist.")
        return False
    
    os.chdir(directory)
    
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
    
    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print(f"Serving at http://localhost:{port}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        return True
    except OSError as e:
        print(f"Error: {e}")
        return False
