---
title: "7 legalnych narzędzi C++ / Lua / Windows, które zbudowałem zamiast cheatów"
published: false
tags: cpp, lua, windows, devtools, security, showdev
---

## Dlaczego?

Większość ludzi zainteresowanych reverse engineeringiem i automatyzacją ląduje w szarej strefie: injectory, bypassy anti-cheat, boty do gier. To droga donikąd — ToS, ban, ryzyko prawne.

Postanowiłem pójść w drugą stronę: **narzędzia, które wykrywają i diagnozują, zamiast łamać.** Wszystkie są read-only, działają w Twoim środowisku i nie dotykają obcych procesów.

Oto 7 narzędzi, które zbudowałem i które możesz kupić / obejrzeć za darmo na GitHubie.

## 1. Project Doctor — statyczny audyt kodu
Analizuje Python / C++ / Lua / JS / TS. Wykrywa:
- surowe `new` i `strcpy` w C++
- brak `target_compile_features` w CMake
- `load` / `os.execute` w Lua
- wycieki sekretów, brak testów

Wynik: Health 0–100 + 5 kroków naprawczych.
**Cena: od 19 € (C++ / Build 29 €)**

## 2. Lua Script Hub
Gotowe, **bezpieczne** skrypty Lua dla modderów (love2d / GMod / Factorio). Wzorce bez `load`/`os.execute` — edukacyjne, kopiowalne.
**Cena: 19 €**

## 3. WinAPI Toolkit
Legalna automatyzacja Windows przez Win32 API (C++). Przykład: enumeracja widocznych okien i ich tytułów — read-only, bez wstrzykiwania.
**Cena: 29 €**

## 4. CTF Pack
Generator edukacyjnych zadań RE/CTF (ukryta flaga w blobie, quiz analizy kodu). Bez malware, bez crackme chronionego softu.
**Cena: 19 €**

## 5. Anti-Cheat Lab
**TYLKO detekcja.** Skanuje sygnatury nazw modułów (cheatengine, speedhack, aimbot) — jak antywirus. Brak bypassu anti-cheat, brak cheatów.
**Cena: 29 €**

## 6. Memory Scanner
Skaner wzorców bajtów w **własnej** pamięci (debug-tool C++). Read-only, brak obcych procesów.
**Cena: 29 €**

## 7. Game Mod Audit
Statyczny audyt modów (Factorio / Minecraft). Sprawdza manifest + ryzykowne wzorce Lua przed publikacją.
**Cena: 19 €**

## Gdzie to zobaczyć?
- Landing: https://ctoai-funnel.fly.dev/
- Wszystkie repo: github.com/famatyyk (CTOAi-Project-Doctor, CTOAi-LuaHub, CTOAi-WinToolkit, CTOAi-CTFGen, CTOAi-ACLab, CTOAi-MemScan, CTOAi-ModAudit)

## Co dalej?
Buduję **CTOAi Doctor CI** — GitHub Action, który odpala audyt na każdym PR. Jeśli chcesz być w beta, napisz na landingu.

Legalnie. Read-only. Bez ingerencji w obce procesy.
