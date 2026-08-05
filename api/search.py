from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse, urlencode
from urllib.request import Request, build_opener, HTTPCookieProcessor
from http.cookiejar import CookieJar
import json

HOME = "https://paksim.xyz/"
API  = "https://paksim.xyz/psg-search.php"

UA = ("Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36")


def search_paksim(q):
    """stdlib hi use karta hai — koi external package nahi chahiye."""
    jar = CookieJar()
    opener = build_opener(HTTPCookieProcessor(jar))   # cookies auto-handle

    hdrs = {
        "User-Agent": UA,
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://paksim.xyz",
        "Referer": "https://paksim.xyz/",
    }

    # 1) fresh PHPSESSID lene ke liye homepage hit
    opener.open(Request(HOME, headers=hdrs), timeout=15)

    # 2) search POST — cookie ab jar me hai, apne aap jayegi
    data = urlencode({"q": q}).encode()
    hdrs["Content-Type"] = "application/x-www-form-urlencoded"
    resp = opener.open(Request(API, data=data, headers=hdrs), timeout=25)

    return resp.status, resp.read().decode("utf-8", "ignore")


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
        self._handle(q)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode("utf-8", "ignore")
        q = parse_qs(raw).get("q", [""])[0]
        self._handle(q)

    def _handle(self, q):
        # HAR cheez try/except me — function kabhi crash hi nahi hoga
        if not q:
            return self._send({"ok": False, "error": "q param required"}, 400)
        try:
            status, text = search_paksim(q)
            try:
                result = json.loads(text)
            except json.JSONDecodeError:
                return self._send({
                    "ok": False,
                    "error": "upstream non-JSON response",
                    "http_status": status,
                    "body": text[:500],
                }, 502)

            records = []
            if isinstance(result, list):
                records = result
            elif isinstance(result, dict):
                for k in ("data", "result", "records", "results"):
                    if isinstance(result.get(k), list):
                        records = result[k]
                        break
                else:
                    records = [result]

            return self._send({
                "ok": bool(records),
                "count": len(records),
                "records": records,
                "upstream_status": status,
            })
        except Exception as e:
            return self._send({"ok": False, "error": str(e)}, 500)
