from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed
from cryptography.hazmat.backends import default_backend
import sys

def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    # Zapisz klucze do plików
    with open("private_key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open("public_key.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    print("Klucze RSA zostały wygenerowane.")
    return private_key, public_key

def load_private_key(path="private_key.pem"):
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(
            f.read(),
            password=None
        )

def sign_file(file_path, private_key):
    with open(file_path, "rb") as f:
        data = f.read()

    # Hash danych
    digest = hashes.Hash(hashes.SHA256())
    digest.update(data)
    hashed = digest.finalize()

    # Podpisz hasz
    signature = private_key.sign(
        hashed,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        Prehashed(hashes.SHA256())
    )

    # Zapisz podpis do pliku
    with open(file_path + ".sig", "wb") as f:
        f.write(signature)

    print(f"Plik '{file_path}' został podpisany. Podpis zapisany jako '{file_path}.sig'.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Użycie: python sign_file.py <plik_do_podpisania>")
        sys.exit(1)

    file_to_sign = sys.argv[1]

    try:
        private_key = load_private_key()
    except FileNotFoundError:
        private_key, _ = generate_keys()

    sign_file(file_to_sign, private_key)
