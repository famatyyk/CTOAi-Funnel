# CTOAi-Funnel

Zautomatyzowany lejek sprzedażowy dla **Project Doctor** (audyt repo Python/AI, 19 €).
Sam odbiera leady, rozmawia (wykrywanie intencji) i ujawnia Twój kontakt
TYLKO po wyraźnej chęci zakupu. Zero zewnętrznych zależności (czysty Python stdlib).

## Uruchomienie (lokalnie)
```
cd CTOAi-Funnel
python server.py
# otwórz http://localhost:8080
```
Podgląd leadów: `http://localhost:8080/api/leads?token=ZMIEN_NA_LOSOWY_TOKEN_123`

## Deploy (Fly.io) — gotowe
Wymaga: `flyctl` zainstalowany + `fly auth login`.
```
cd CTOAi-Funnel
fly launch          # pierwszy raz: utworzy apke, volume /data, wykryje fly.toml
fly deploy          # kolejne wdrozenia
```
- `fly.toml` ma mount `/data` → leady przetrwaja restart (efemeryczny dysk Fly.io).
- Serwer bierze port z `$PORT` (Fly wstrzykuje). Lokalnie (bez `$PORT`) używa 8080.
- Po deploy: `https://<app>.fly.dev` to Twój landing.
- Leady: `https://<app>.fly.dev/api/leads?token=29df95e9...4004`

Alternatywa: Render / Railway / VPS — wystarczy `python server.py` w kontenerze
(zbudowanym z DoDockerfile) i bind na `$PORT`.

## Konfiguracja (config.py)
- `CONTACT_INFO.email` — **CTOComapnyAi@proton.me** (ujawaniany po intencji)
- `ADMIN_TOKEN` — `29df95e9bbf7c264cd8ee54eb5210f6f10e55095245f44d4c091d814ac334004`
- `INTENT_KEYWORDS` — słowa wyzwalające ujawnienie kontaktu
- `PHASE2.deploy.enabled` — True (serwer deploy-aware: `$PORT`)
- `PHASE2.*` — opcjonalne moduły (Telegram/LLM/mail/Stripe), WYŁĄCZONE (enabled:False)

## Co działa (MVP)
- Landing + formularz leada + czat
- Wykrywanie intencji (słowa klucze PL/EN)
- Gate: kontakt ujawniany tylko po intencji
- Lista leadów dla Ciebie (token)

## Phase 2 (wymaga Twoich kluczy)
- Prawdziwy czat przez LLM (naturalna rozmowa) — podmień `do_POST /api/chat`
- Wysyłka maili (SMTP / Resend / Postmark)
- Płatność (Stripe Checkout) przed ujawnieniem kontaktu
- Hosting (Fly.io / Render / VPS) + domena
- Telegram/Discord powiadomienie o "hot" leadzie
