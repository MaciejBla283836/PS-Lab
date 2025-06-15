from cryptography.fernet import Fernet

# Wygeneruj klucz i zapisz do pliku 
def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

# Wczytaj klucz z pliku
def load_key():
    return open("key.key", "rb").read()

# Zaszyfruj plik
def encrypt_file(filename):
    key = load_key()
    f = Fernet(key)

    with open(filename, "rb") as file:
        data = file.read()

    encrypted = f.encrypt(data)

    with open(filename + ".enc", "wb") as file:
        file.write(encrypted)

# Odszyfruj plik
def decrypt_file(filename, output_filename):
    key = load_key()
    f = Fernet(key)

    with open(filename, "rb") as file:
        encrypted_data = file.read()

    decrypted = f.decrypt(encrypted_data)

    with open(output_filename, "wb") as file:
        file.write(decrypted)

if __name__ == "__main__":
    try:
        key = generate_key()
    except FileNotFoundError:
        key, _ = generate_key()

    encrypt_file("plik.txt")                # Zaszyfruje plik.txt → plik.txt.enc
    decrypt_file("plik.txt.enc", "odszyfrowany_plik.txt")  # Odszyfrowanie

