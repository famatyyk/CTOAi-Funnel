#!/usr/bin/env python3
"""CTOAi-Funnel - auto-posting ofert (bez Twojego klikania).
Wrzuca oferte Project Doctor na Discord/Telegram co `interval_min` minut.
Uruchom w tle:  python autopost.py
Wymaga w config.py: PHASE2.autopost.{discord_webhook | telegram_bot+telegram_chat}
"""
import json, time, urllib.request, urllib.error
import config


def post_discord(webhook, text):
    req = urllib.request.Request(webhook,
        data=json.dumps({"content": text}).encode(),
        headers={"Content-Type": "application/json"}, method="POST")
    urllib.request.urlopen(req, timeout=10)


def post_telegram(bot, chat, text):
    url = f"https://api.telegram.org/bot{bot}/sendMessage"
    req = urllib.request.Request(url,
        data=json.dumps({"chat_id": chat, "text": text}).encode(),
        headers={"Content-Type": "application/json"}, method="POST")
    urllib.request.urlopen(req, timeout=10)


def run_once():
    a = config.PHASE2.get("autopost", {})
    if not a.get("enabled"):
        print("[autopost] wylaczony w configu (enabled=False)")
        return
    text = a.get("offer_text", "")
    if a.get("discord_webhook"):
        try:
            post_discord(a["discord_webhook"], text)
            print("[autopost] Discord: OK")
        except Exception as e:
            print(f"[autopost] Discord: BLAD {e}")
    if a.get("telegram_bot") and a.get("telegram_chat"):
        try:
            post_telegram(a["telegram_bot"], a["telegram_chat"], text)
            print("[autopost] Telegram: OK")
        except Exception as e:
            print(f"[autopost] Telegram: BLAD {e}")


if __name__ == "__main__":
    a = config.PHASE2.get("autopost", {})
    interval = a.get("interval_min", 1440) * 60
    print(f"[autopost] start, interwal={interval}s")
    # pierwsze wstawienie od razu
    run_once()
    while True:
        time.sleep(interval)
        run_once()
