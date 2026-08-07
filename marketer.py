#!/usr/bin/env python3
"""CTOAi-Funnel - agent rynkowy (marketer).
Automatycznie wystawia i odnawia oferte Project Doctor na Twoich kontach
przez API/platformy, do ktorych podales tokeny w config.py (PHASE2.marketing).
Uruchom w tle:  python marketer.py
Wymaga w config.py: PHASE2.marketing.{kofi_page, discord_webhook, telegram_bot+chat, x_bearer}
UWAGA: agent uzywa TYLKO Twoich kont (zalozyles je recznie). Nie tworzy nowych kont.
"""
import json, time, urllib.request, urllib.error
import config


def _post_json(url, payload, headers=None, method="POST"):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data,
        headers=headers or {"Content-Type": "application/json"}, method=method)
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.status, r.read().decode()


def _post_form(url, fields):
    import urllib.parse
    data = urllib.parse.urlencode(fields).encode()
    req = urllib.request.Request(url, data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}, method="POST")
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.status, r.read().decode()


def post_discord(webhook, text):
    return _post_json(webhook, {"content": text})


def post_telegram(bot, chat, text):
    return _post_json(f"https://api.telegram.org/bot{bot}/sendMessage",
                      {"chat_id": chat, "text": text})


def post_x(bearer, text):
    # Twitter/X v2: wymaga app + bearer token (recznie zalozone konto)
    return _post_json("https://api.twitter.com/2/tweets",
                      {"text": text},
                      headers={"Authorization": f"Bearer {bearer}",
                               "Content-Type": "application/json"})


def post_kofi_commission(page_url, text):
    # Ko-fi NIE ma API do tworzenia commission - to jednorazowy krok reczny w dashboardzie.
    # Agent tylko przypomina (log), ze oferta powinna byc na Twojej stronie Ko-fi.
    print(f"[kofi] oferta powinna byc recznie wystawiona na: {page_url}")
    return 200, "manual-step"


def run_once():
    m = config.PHASE2.get("marketing", {})
    if not m.get("enabled"):
        print("[marketer] wylaczony w configu (PHASE2.marketing.enabled=False)")
        return
    text = m.get("offer_text", "🔍 Project Doctor — audyt Twojego repozytorium Python/AI. Cena od 19 EUR.")
    print(f"[marketer] start, wystawiam oferte na: {', '.join([k for k in m if m[k] and k not in ('enabled','offer_text','interval_min')])}")

    if m.get("discord_webhook"):
        try:
            st, _ = post_discord(m["discord_webhook"], text)
            print(f"[marketer] Discord: {st}")
        except Exception as e:
            print(f"[marketer] Discord BLAD: {e}")

    if m.get("telegram_bot") and m.get("telegram_chat"):
        try:
            st, _ = post_telegram(m["telegram_bot"], m["telegram_chat"], text)
            print(f"[marketer] Telegram: {st}")
        except Exception as e:
            print(f"[marketer] Telegram BLAD: {e}")

    if m.get("x_bearer"):
        try:
            st, _ = post_x(m["x_bearer"], text)
            print(f"[marketer] X/Twitter: {st}")
        except Exception as e:
            print(f"[marketer] X/Twitter BLAD: {e}")

    if m.get("kofi_page"):
        post_kofi_commission(m["kofi_page"], text)


if __name__ == "__main__":
    m = config.PHASE2.get("marketing", {})
    interval = m.get("interval_min", 1440) * 60
    print(f"[marketer] start, interwal={interval}s")
    run_once()
    while True:
        time.sleep(interval)
        run_once()
