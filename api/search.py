from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
import requests

API = "https://paksim.xyz/psg-search.php"
HOME = "https://paksim.xyz/"

UA = ("Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36")


def search_paksim(q):
    s = requests.Session()
    s.headers.update({
        "user-agent": UA,
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "x-requested-with": "XMLHttpRequest",
        "origin": "https://paksim.xyz",
        "referer": "https://paksim.xyz/",
    })

    # 1) Pehle homepage hit karo → fresh PHPSESSID cookie mil jayegi (auto-save)
    s.get(HOME, timeout=15)

    # 2) Ab search karo — cookie khud-ba-khud request me jayegi
    r = s.post(API, data={"q": q}, timeout=20)
    return r


def normalize(result):
    """Response shape kuch bhi ho, list me convert kar deta hai."""
    if isinstance(result, list):
        return result
    if isinstance(result, dict):
        for key in ("data", "result", "records", "results"):
            if isinstance(result.get(key), list):
                return result[key]
    return []


class handler(BaseHTTPRequestHandler):

    def _send(self, obj, status=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._send({})

    def do_GET(self):
        q = parse_qs(urlparse(self.path).query).get("q", [""])[0]
        self.run(q, self.path)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode("utf-8", "ignore")
        q = parse_qs(raw).get("q", [""])[0]
        self.run(q, self.path)

    def run(self, q, path):
        if not q:
            return self._send({"ok": False, "error": "q param required"}, 400)

        try:
            resp = search_paksim(q)
            try:
                result = resp.json()
            except Exception:
                # JSON nahi → 403/HTML/challenge aaya hoga, raw dikha do
                return self._send({
                    "ok": False,
                    "error": "non-JSON response",
                    "http_status": resp.status_code,
                    "body": resp.text[:500],
                }, 502)

            records = normalize(result)
            out = {"ok": bool(records), "count": len(records), "records": records}

            # ?debug=1 lagao to raw response bhi milta hai
            if "debug" in parse_qs(urlparse(path).query):
                out["raw"] = result

            return self._send(out)
        except Exception as e:
            return self._send({"ok": False, "error": str(e)}, 500)
