import socket
import sys
import argparse
from datetime import datetime

def is_port_open(host: str, port: int) -> bool:
    """
    Sprawdza, czy port na danym hoście jest otwarty.
    Zwraca True jeśli port jest otwarty, inaczej False.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            return result == 0
    except socket.error as e:
        print(f"[!] Błąd przy skanowaniu portu {port}: {e}")
        return False

def scan_port_range(host: str, start_port: int, end_port: int):
    """
    Skanuje porty od start_port do end_port na hoście host.
    """
    print(f"\n Rozpoczynam skanowanie {host} (porty {start_port}-{end_port})")
    print("-" * 60)

    start_time = datetime.now()
    open_ports = []

    for port in range(start_port, end_port + 1):
        if is_port_open(host, port):
            print(f"[+] Port {port} jest otwarty")
            open_ports.append(port)

    end_time = datetime.now()
    duration = end_time - start_time

    print("\n Skanowanie zakończone")
    print(f"Czas skanowania: {duration}")

    if open_ports:
        print("\n Otwarte porty:")
        for port in open_ports:
            print(f"  - Port {port}")
    else:
        print("\n Nie znaleziono otwartych portów.")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Prosty skaner portów TCP")
    parser.add_argument("host", help="Adres IP lub nazwa hosta")
    parser.add_argument("start_port", type=int, help="Numer początkowego portu")
    parser.add_argument("end_port", type=int, help="Numer końcowego portu")
    return parser.parse_args()

def validate_ports(start_port: int, end_port: int):
    if not (1 <= start_port <= 65535 and 1 <= end_port <= 65535):
        print("[!] Porty muszą mieścić się w zakresie 1–65535.")
        sys.exit(1)
    if start_port > end_port:
        print("[!] Port początkowy nie może być większy niż końcowy.")
        sys.exit(1)

def main():
    args = parse_arguments()
    validate_ports(args.start_port, args.end_port)
    scan_port_range(args.host, args.start_port, args.end_port)

if __name__ == "__main__":
    main()
