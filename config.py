# CTOAi-Funnel - konfiguracja.
# Twoj kontakt ujawniany LEADOWI tylko po wyraznej checi zakupu.
CONTACT_INFO = {
    "email": "CTOComapnyAi@proton.me",
    "note": "Napisz tutaj, a oddzwonimy / odpiszemy w 24h."
}

# Token do podglodu leadow (WYGENEROWANY: secrets.token_hex(32), 2026-08-07).
ADMIN_TOKEN = "29df95e9bbf7c264cd8ee54eb5210f6f10e55095245f44d4c091d814ac334004"

# Slowa klucze = wyrazona chec zakupu (PL/EN, mala wielkosc).
INTENT_KEYWORDS = [
    "kupi", "kupuj", "kupie", "zamaw", "zamow", "chc", "chce",
    "interesuje", "platne", "zaplac", "pay", "buy", "order",
    "purchase", "platna", "wykup", "wynajm", "skorzyst"
]

# Canned odpowiedz gdy NIE MA jeszcze intencji (rozmawiamy dalej).
DEFLECT_REPLY = (
    "Project Doctor to statyczny audyt Twojego repo Python/AI "
    "(struktura, testy, CI, sekrety, ryzyka). Raport MD+JSON w 24-48h. "
    "Masz pytania o zakres, cene (19 EUR) lub demo?"
)
INTENT_REPLY = "Super - przygotuje audyt. Skontaktuj sie bezposrednio:"

# =====================================================================
# PHASE 2 - rozszerzenia (CZEKAJA NA KLUCZE / MOZLIWOSCI).
# Wszystkie WYLOCZONE (flagi False). Podaj klucze -> wlaczam jeden po drugim.
# =====================================================================
PHASE2 = {
    # (b) Powiadomienie na Telegram o hot leadzie
    "telegram": {
        "enabled": False,
        "bot_token": "",   # podaj: 123456:ABC-DEF...
        "chat_id": "",     # podaj: Twoj chat id
    },
    # (c) Prawdziwy czat przez LLM (naturalna rozmowa) - zamiast DEFLECT_REPLY
    "llm_chat": {
        "enabled": False,
        "provider": "openai",  # lub "nous" / "local"
        "api_key": "",
        "model": "gpt-4o-mini",
    },
    # (c) Wysylka maila po pozostawieniu leada
    "email_out": {
        "enabled": False,
        "smtp_host": "",
        "smtp_user": "",
        "smtp_pass": "",
        "from": "CTOComapnyAi@proton.me",
    },
    # (c) Platnosc Stripe przed ujawnieniem kontaktu
    "stripe": {
        "enabled": False,
        "secret_key": "",
        "price_id": "",
    },
    # (c) Deploy-ready: gdy True, serwer nasluchuje na $PORT (Fly.io/Render)
    "deploy": {
        "enabled": True,
        "bind": "0.0.0.0",
        "port_env": "PORT",
        "port_default": 8080,
    },
    # (d) Ko-fi webhook - odbior PLATNOSCI (z panelu API: Verification token)
    "kofi": {
        "enabled": True,
        "verify_token": "a3faf472-d610-4cd3-93f7-b635206cc393",  # TODO: zastap swoim z panelu Ko-fi
        "webhook_path": "/api/kofi-webhook",
    },
    # (e) Auto-posting ofert (bez Twojego klikania) - Discord/Telegram webhooki
    "autopost": {
        "enabled": False,
        "discord_webhook": "",   # podaj: https://discord.com/api/webhooks/...
        "telegram_bot": "",      # podaj: token bota
        "telegram_chat": "",     # podaj: Twoj chat id
        "interval_min": 1440,    # co ile minut wstawiac oferte (1440 = raz dziennie)
        "offer_text": (
            "🔍 Project Doctor — audyt Twojego repozytorium Python/AI\n"
            "Struktura, testy, CI, sekrety, ryzyka. Raport MD+JSON w 24-48h.\n"
            "Cena: od 19 EUR. Napisz, a wygenerujemy raport."
        ),
    },
    # (f) Agent rynkowy (marketer) - wystawia/odnawia oferty na Twoich kontach przez API.
    #     UWAGA: uzywa TYLKO Twoich kont (zalozyles je recznie). Nie tworzy nowych.
    "marketing": {
        "enabled": False,
        "interval_min": 1440,    # co ile minut odnawiac oferte (1440 = raz dziennie)
        "offer_text": (
            "🔍 Project Doctor — audyt Twojego repozytorium Python/AI\n"
            "Struktura, testy, CI, sekrety, ryzyka. Raport MD+JSON w 24-48h.\n"
            "Cena: od 19 EUR. Napisz, a wygenerujemy raport."
        ),
        "discord_webhook": "",   # podaj: https://discord.com/api/webhooks/...
        "telegram_bot": "",      # podaj: token bota
        "telegram_chat": "",     # podaj: Twoj chat id
        "x_bearer": "",          # podaj: Twitter/X API bearer token (wymaga app + zalozone konto)
        "kofi_page": "https://ko-fi.com/NAZWA_TWOJEGO_KONTA",  # recznie wystaw commission w dashboardzie
    },
}
