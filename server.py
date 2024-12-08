import http.server
import socketserver
import urllib.parse
import json

menu_items = {
    "Burger": 149,
    "Pizza": 299,
    "Pasta": 249,
    "Fries": 99,
    "Salad": 129,
    "Soda": 49,
    "Coffee": 79
}

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/calculate_bill":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            post_data = urllib.parse.parse_qs(post_data)

            total = 0
            details = []
            for item, price in menu_items.items():
                if item in post_data:
                    try:
                        quantity = int(post_data[item][0])
                        if quantity > 0:
                            cost = quantity * price
                            total += cost
                            details.append(f"{item} x {quantity} = ₹{cost:.2f}")
                    except ValueError:
                        pass

            response = {"total": f"₹{total:.2f}", "details": details}
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")  # Add CORS header
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

    def do_OPTIONS(self):
        # Handle preflight request for CORS
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

PORT = 8000
with socketserver.TCPServer(("", PORT), MyRequestHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
