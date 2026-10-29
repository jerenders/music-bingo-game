#!/usr/bin/env python3
"""Local dev server: python3 scripts/dev.py   (or ./dev)

Serves the app at http://localhost:8765 from the repo itself. Whenever you load the page it rebuilds first
if src/, data/, vendor/ or scripts/build.py changed since the last build, so after a `git pull` you just
refresh the browser. Pulls the latest from GitHub on start (skip with --no-pull). Ctrl+C to stop.
Binds to localhost only, so nothing on your network can reach it."""
import http.server, os, socketserver, subprocess, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
DIST = os.path.join(ROOT, "dist", "index.html")
WATCH = ["src/template.html", "scripts/build.py"] + glob.glob("data/categories/*.json") + glob.glob("vendor/*")

def stale():
    if not os.path.exists(DIST): return True
    t = os.path.getmtime(DIST)
    return any(os.path.getmtime(p) > t for p in WATCH + glob.glob("data/categories/*.json") if os.path.exists(p))

def rebuild():
    print("rebuilding...", flush=True)
    r = subprocess.run([sys.executable, "scripts/build.py"], capture_output=True, text=True)
    if r.returncode: print(r.stdout + r.stderr)
    else: print("built dist/index.html", flush=True)

class H(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        p = path.split("?")[0].split("#")[0]
        if p in ("/", "/index.html"):
            if stale(): rebuild()
            return DIST
        if p.startswith(("/songs/", "/vendor/")):
            return os.path.join(ROOT, p.lstrip("/"))
        return os.path.join(ROOT, "__not_found__")
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()
    def log_message(self, *a): pass

if __name__ == "__main__":
    if "--no-pull" not in sys.argv and os.path.isdir(os.path.join(ROOT, ".git")):  # a downloaded ZIP has no .git, so skip the pull
        r = subprocess.run(["git", "pull", "--ff-only", "-q"], capture_output=True, text=True)
        print("git pull:", (r.stdout + r.stderr).strip() or "up to date", flush=True)
    if stale(): rebuild()
    socketserver.TCPServer.allow_reuse_address = True
    for port in range(8765, 8775):
        try: srv = socketserver.TCPServer(("127.0.0.1", port), H); break
        except OSError: continue
    else: sys.exit("no free port between 8765 and 8774")
    print(f"\nOpen http://localhost:{port}   (Ctrl+C to stop; refresh the page to pick up changes)\n", flush=True)
    try: srv.serve_forever()
    except KeyboardInterrupt: print("stopped")
