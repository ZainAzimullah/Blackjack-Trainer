import http.server
import socketserver
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", 8090), Handler) as httpd:
    print(f"Serving on port 8090")
    httpd.serve_forever()
