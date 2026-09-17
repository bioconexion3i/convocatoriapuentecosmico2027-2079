#!/usr/bin/env python3
import datetime
import http.server
import os
import socketserver
import urllib.error
import urllib.request

HOST = "0.0.0.0"
PORT = 8000
UPSTREAM_API = "http://127.0.0.1:5000"
LOG_DIR = "/home/bio/nodo_merida/logs"
LOG_FILE = os.path.join(LOG_DIR, "cosmograma.log")
ERROR_LOG = os.path.join(LOG_DIR, "cosmograma_error.log")

os.makedirs(LOG_DIR, exist_ok=True)


class CosmogramaHandler(http.server.SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, format, *args):
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{datetime.datetime.now().isoformat()} - {format % args}\n")

    def log_error(self, format, *args):
        with open(ERROR_LOG, "a", encoding="utf-8") as f:
            f.write(f"{datetime.datetime.now().isoformat()} - {format % args}\n")

    def do_GET(self):
        if self.path == "/api/oraculo/hoy":
            self.proxy_oraculo()
            return
        super().do_GET()

    def do_OPTIONS(self):
        if self.path.startswith("/api/"):
            self.send_response(204)
            self.send_header("Allow", "GET, OPTIONS")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        self.send_error(405, "Method Not Allowed")

    def proxy_oraculo(self):
        url = f"{UPSTREAM_API}{self.path}"

        try:
            request = urllib.request.Request(
                url,
                method="GET",
                headers={"Accept": "application/json"},
            )

            with urllib.request.urlopen(request, timeout=10) as response:
                body = response.read()
                content_type = response.headers.get(
                    "Content-Type",
                    "application/json; charset=utf-8",
                )

                self.send_response(response.status)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(body)

        except urllib.error.HTTPError as error:
            body = error.read() or b'{"error":"API upstream error"}'
            self.send_response(error.code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        except Exception as error:
            self.log_error("Proxy API error: %s", error)
            body = b'{"error":"Servicio de oraculo no disponible"}'
            self.send_response(502)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)


class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with ThreadingHTTPServer((HOST, PORT), CosmogramaHandler) as httpd:
        print(f"Cosmograma disponible en http://{HOST}:{PORT}")
        print(f"Proxy de API: /api/* → {UPSTREAM_API}/api/*")
        httpd.serve_forever()
