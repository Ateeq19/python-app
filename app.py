import os
import json
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 6200

# Helper: load HTML templates
def load_template(name):
    path = os.path.join("templates", name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# Helper: render with layout.html
def render_page(body_html, title="Python App"):
    layout = load_template("layout.html")
    return layout.replace("{{title}}", title).replace("{{content}}", body_html)


# Custom server handler
class MyHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        # Serve static files
        if path.startswith("/static/"):
            return super().do_GET()

        # Home page
        if path == "/":
            body = load_template("index.html")
            return self.respond_html(render_page(body, "Home"))

        # About page
        elif path == "/about":
            body = load_template("about.html")
            return self.respond_html(render_page(body, "About"))

        # API endpoint: returns JSON
        elif path == "/api/user":
            data = {
                "name": "Ateeq",
                "role": "DevOps / Python learner",
                "message": "Welcome to the API!"
            }
            return self.respond_json(data)

        # Query string example: /greet?name=Ateeq
        elif path == "/greet":
            name = params.get("name", ["Guest"])[0]
            message = f"<h2>Hello {name}!</h2>"
            return self.respond_html(render_page(message, "Greeting"))

        # 404 page
        return self.respond_html("<h1>404 - Page Not Found</h1>", status=404)


    # --- Response helpers ---
    def respond_html(self, content, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode())

    def respond_json(self, data):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())


# Run the server
with HTTPServer(("0.0.0.0", PORT), MyHandler) as httpd:
    print(f"🚀 Server running at http://localhost:{PORT}")
    httpd.serve_forever()
