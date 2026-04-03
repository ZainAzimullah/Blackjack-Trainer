import http.server
import os
import socketserver
import threading
import time

os.chdir(os.path.dirname(os.path.abspath(__file__)))

PORT = 8090
PING_PATH = "/__ping"
# If no heartbeat for this long, exit (tab closed or game left)
STALE_SECONDS = 5
# Exit if nothing has ever pinged after this long (orphan server)
IDLE_NO_CLIENT_SECONDS = 300

last_heartbeat = None
server_start = time.time()
httpd_ref = None


class GameHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global last_heartbeat
        if self.path == PING_PATH or self.path.startswith(PING_PATH + "?"):
            last_heartbeat = time.time()
            self.send_response(204)
            self.end_headers()
            return
        super().do_GET()

    def log_message(self, format, *args):
        try:
            msg = format % args
        except TypeError:
            msg = str(args)
        if PING_PATH in msg:
            return
        super().log_message(format, *args)


def watchdog():
    global httpd_ref
    while True:
        time.sleep(2)
        now = time.time()
        if last_heartbeat is None:
            if now - server_start > IDLE_NO_CLIENT_SECONDS and httpd_ref:
                print("No game client — stopping server.")
                httpd_ref.shutdown()
            continue
        if now - last_heartbeat > STALE_SECONDS and httpd_ref:
            print("Game closed — stopping server.")
            httpd_ref.shutdown()
            break


socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("", PORT), GameHandler) as httpd:
    httpd_ref = httpd
    threading.Thread(target=watchdog, daemon=True).start()
    print(f"Serving on port {PORT} (stops ~{STALE_SECONDS}s after you close the game tab)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
print("Server stopped.")
