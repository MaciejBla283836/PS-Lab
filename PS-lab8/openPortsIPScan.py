import shodan

# Ustawienia
API_KEY = '51BpbZm8IE4s0jyRmYsKZoR1G423Aeg2' 
api = shodan.Shodan(API_KEY)

# Adres
ip = input("Podaj adres IP do sprawdzenia: ")

try:
    # Pobierz informacje o hoście
    host = api.host(ip)

    # Podstawowe informacje
    print(f"Informacje o hoście: {ip}")
    print(f"Organizacja  : {host.get('org', 'Brak danych')}")
    print(f"Kraj         : {host.get('country_name', 'Brak danych')}")
    print(f"System       : {host.get('os', 'Nieznany')}")
    print(f"Hostnames    : {', '.join(host.get('hostnames', []))}")
    print(f"Domena(y)    : {', '.join(host.get('domains', []))}")

    # Otwarte porty
    print("Otwarte porty i usługi:")
    for item in host['data']:
        port = item['port']
        banner = item.get('product') or item.get('banner') or 'Nieznana usługa'
        print(f" - Port {port}: {banner}")

except shodan.APIError as e:
    print(f"Błąd API Shodan: {e}")
