import http.server
import socketserver

PORT = 8888
DIRECTORY = "web"  # Current directory
HOST = "0.0.0.0"  # Bind to all network interfaces

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
    print(f"Serving at {HOST}:{PORT}")
    httpd.serve_forever()
