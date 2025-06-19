from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

class CustomHandler(BaseHTTPRequestHandler):
    router = None 

    def do_GET(self):
        self.handle_request('GET')

    def do_POST(self):
        self.handle_request('POST')

    def do_PUT(self):
        self.handle_request('PUT')

    def do_DELETE(self):
        self.handle_request('DELETE')

    def handle_request(self, method):
        parsed_path = urlparse(self.path)
        route = parsed_path.path
        handler = self.router.resolve(method, route)
        if handler:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8') if content_length else ''
            query = parse_qs(parsed_path.query)
            try:
                data = json.loads(body) if body else {}
                response = handler(data, query)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
            except Exception as e:
                self.send_error(500, f"Server Error: {e}")
        else:
            self.send_error(404, "Route not found")

def run_server(router, port=8000):
    CustomHandler.router = router
    server = HTTPServer(('localhost', port), CustomHandler)
    print(f"🚀 Server started on http://localhost:{port}")
    server.serve_forever()

def http_response(body, status=200, content_type="text/plain"):
    return {
        "status": status,
        "headers": {"Content-Type": content_type},
        "body": body
    }

