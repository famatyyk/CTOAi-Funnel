#!/usr/bin/env python3
"""CTOAi-Funnel - lejek sprzedazowy Project Doctor (stdlib, zero zalezności).
Uruchom:  python server.py   ->  http://localhost:8080
API:
  GET  /                       landing
  POST /api/lead {email,repo,message} -> zapis leada
  POST /api/chat {client_id,message}  -> czat; po intencji zwraca kontakt
  GET  /api/leads?token=ADMIN           -> lista leadow (tylko z tokenem)
"""
import json, sqlite3, os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import config

# DB: lokalnie w katalogu, na hostingu (Fly.io/Render) w /data jesli istnieje.
_DATA = "/data" if os.path.isdir("/data") else os.path.dirname(__file__)
DB = os.path.join(_DATA, "leads.db")
PORT = 8080


def init_db():
    c = sqlite3.connect(DB)
    c.execute("""CREATE TABLE IF NOT EXISTS leads(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id TEXT, email TEXT, repo TEXT,
        message TEXT, hot INTEGER DEFAULT 0, paid INTEGER DEFAULT 0,
        language TEXT DEFAULT 'python',
        created TEXT DEFAULT CURRENT_TIMESTAMP)""")
    # dodaj kolumne language jesli brak (migracja dla istniejacych baz)
    try:
        c.execute("ALTER TABLE leads ADD COLUMN language TEXT DEFAULT 'python'")
    except sqlite3.OperationalError:
        pass
    c.commit()
    c.close()


def add_lead(client_id, email, repo, message, hot=0, language="python"):
    c = sqlite3.connect(DB)
    c.execute("INSERT INTO leads(client_id,email,repo,message,hot,language) VALUES(?,?,?,?,?,?)",
              (client_id, email, repo, message, hot, language))
    c.commit()
    c.close()


def mark_hot(client_id, message):
    c = sqlite3.connect(DB)
    cur = c.cursor()
    cur.execute("UPDATE leads SET hot=1, message=? WHERE client_id=?", (message, client_id))
    if cur.rowcount == 0:
        cur.execute("INSERT INTO leads(client_id,email,repo,message,hot) VALUES(?,?,?,?,?)",
                    (client_id, client_id, "", message, 1))
    c.commit()
    c.close()


def add_payment(email, message, amount=""):
    c = sqlite3.connect(DB)
    c.execute("INSERT INTO leads(client_id,email,repo,message,hot,paid) VALUES(?,?,?,?,?,?)",
              (email or "kofi", email, "kofi", message, 1, 1))
    c.commit()
    c.close()


def detect_intent(text):
    t = (text or "").lower()
    return any(k in t for k in config.INTENT_KEYWORDS)


class H(BaseHTTPRequestHandler):
    def _send(self, code, obj=None, body=None, ctype="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        if obj is not None:
            self.wfile.write(json.dumps(obj, ensure_ascii=False).encode("utf-8"))
        elif body is not None:
            self.wfile.write(body)

    def _serve(self, path):
        fp = os.path.join(os.path.dirname(__file__), path)
        if not os.path.isfile(fp):
            self._send(404, {"error": "no file"})
            return
        with open(fp, "rb") as f:
            data = f.read()
        if fp.endswith(".html"):
            ct = "text/html; charset=utf-8"
        elif fp.endswith(".js"):
            ct = "application/javascript"
        elif fp.endswith(".css"):
            ct = "text/css"
        else:
            ct = "text/plain"
        self._send(200, body=data, ctype=ct)

    def do_GET(self):
        p = urlparse(self.path)
        if p.path == "/health":
            self._send(200, {"status": "ok"})
        elif p.path in ("/", "/index.html"):
            self._serve("static/index.html")
        elif p.path.startswith("/static/"):
            self._serve(p.path[1:])
        elif p.path == "/api/leads":
            tok = p.query.split("token=")[-1]
            if tok == config.ADMIN_TOKEN:
                c = sqlite3.connect(DB)
                c.row_factory = sqlite3.Row
                rows = c.execute("SELECT * FROM leads ORDER BY id DESC").fetchall()
                self._send(200, [dict(r) for r in rows])
            else:
                self._send(403, {"error": "bad token"})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        p = urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            data = json.loads(raw or b"{}")
        except Exception:
            data = {}
        if p.path == "/api/lead":
            cid = data.get("email") or data.get("client_id") or "anon"
            lang = (data.get("language") or "python").lower()
            if lang not in ("python", "cpp", "c++", "lua", "js", "ts", "build", "luahub", "winapi", "ctf", "acl"):
                lang = "python"
            price = "29 EUR" if lang in ("cpp", "c++", "build", "winapi", "acl") else "19 EUR"
            add_lead(cid, data.get("email", ""), data.get("repo", ""), data.get("message", ""), language=lang)
            self._send(200, {"ok": True, "client_id": cid, "language": lang, "price": price,
                             "message": f"Zgłoszenie przyjęte. Audyt ({lang}) — {price}."})
        elif p.path == "/api/chat":
            cid = data.get("client_id") or "anon"
            msg = data.get("message", "")
            if detect_intent(msg):
                mark_hot(cid, msg)
                self._send(200, {"intent": True, "reply": config.INTENT_REPLY,
                                 "contact": config.CONTACT_INFO})
            else:
                self._send(200, {"intent": False, "reply": config.DEFLECT_REPLY})
        elif p.path == config.PHASE2.get("kofi", {}).get("webhook_path", "/api/kofi-webhook"):
            # Ko-fi: POST application/x-www-form-urlencoded, pole 'data' = JSON string
            from urllib.parse import parse_qs
            try:
                form = parse_qs(raw.decode("utf-8", "ignore"))
                payload = json.loads(form.get("data", ["{}"])[0])
            except Exception:
                payload = {}
            # Weryfikacja: token z naglowka 'X-Kofi-Verification' LUB pole 'verification_token'
            got_token = self.headers.get("X-Kofi-Verification", "") or (payload.get("verification_token", ""))
            expected = config.PHASE2.get("kofi", {}).get("verify_token", "")
            if got_token != expected:
                self._send(403, {"error": "bad kofi token"})
                return
            # Tylko platnosci (Commission/Tip z is_payment_received)
            if payload.get("is_payment_received") or payload.get("type") in ("Commission", "Tip", "Subscription"):
                email = payload.get("email", "kofi-client")
                add_payment(email, json.dumps(payload, ensure_ascii=False))
                # TODO: powiadomienie Telegram/email (PHASE2)
            self._send(200, {"ok": True})
        else:
            self._send(404, {"error": "no route"})


if __name__ == "__main__":
    init_db()
    dep = config.PHASE2.get("deploy", {})
    if dep.get("enabled"):
        bind = dep.get("bind", "0.0.0.0")
        PORT = int(os.environ.get(dep.get("port_env", "PORT"), dep.get("port_default", 8080)))
    else:
        bind = "0.0.0.0"
    print(f"CTOAi-Funnel na http://{bind}:{PORT}  (db={DB})")
    HTTPServer((bind, PORT), H).serve_forever()
