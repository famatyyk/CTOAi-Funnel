#!/usr/bin/env python3
"""CTOAi-Funnel - jednorazowe czyszczenie leadow TESTOWYCH.

Bezpieczne: kasuje TYLKO wpisy o znanej sygnaturze testowej, nie ruszа
prawdziwych klientow. Mozna odpalic wielokrotnie bez szkody.

Uzycie na Fly:
    fly ssh console --app ctoai-funnel -C "python cleanup_leads.py"

Podglad bez kasowania:
    fly ssh console --app ctoai-funnel -C "python cleanup_leads.py --dry-run"
"""
import sqlite3, os, sys

_DATA = "/data" if os.path.isdir("/data") else os.path.dirname(__file__)
DB = os.path.join(_DATA, "leads.db")

# Sygnatury danych testowych z fazy wdrozenia (email / client_id).
TEST_EMAILS = ("test-hermes@example.com", "test@przyklad.com")
TEST_CLIENT_IDS = ("anon",)

DRY = "--dry-run" in sys.argv

def main():
    if not os.path.isfile(DB):
        print(f"Brak bazy: {DB} (nic do czyszczenia)")
        return
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row

    q_email = ",".join("?" * len(TEST_EMAILS))
    q_cid = ",".join("?" * len(TEST_CLIENT_IDS))
    where = f"email IN ({q_email}) OR client_id IN ({q_cid})"
    params = (*TEST_EMAILS, *TEST_CLIENT_IDS)

    rows = c.execute(f"SELECT id, client_id, email, paid FROM leads WHERE {where}",
                     params).fetchall()
    print(f"Baza: {DB}")
    print(f"Znaleziono {len(rows)} testowych leadow:")
    for r in rows:
        print(f"  #{r['id']}  client_id={r['client_id']!r}  email={r['email']!r}  paid={r['paid']}")

    total = c.execute("SELECT COUNT(*) FROM leads").fetchone()[0]

    if DRY:
        print("\n[DRY-RUN] nic nie usunieto. Bez --dry-run skasuje powyzsze.")
        c.close()
        return

    n = c.execute(f"DELETE FROM leads WHERE {where}", params).rowcount
    c.commit()
    left = c.execute("SELECT COUNT(*) FROM leads").fetchone()[0]
    # jesli tabela pusta - zresetuj licznik ID (pierwszy realny lead = #1)
    if left == 0:
        c.execute("DELETE FROM sqlite_sequence WHERE name='leads'")
        c.commit()
        print("\nTabela pusta -> zresetowano licznik ID (nastepny lead = #1).")
    c.close()
    print(f"\nUsunieto {n} z {total} leadow. Pozostalo: {left}.")

if __name__ == "__main__":
    main()
