import requests

# Ustawienia
API_KEY = 'acf45b95366b4ce88047a3af553fc6c8'
query = input("Podaj temat do wyszukania: ")
url = f'https://newsapi.org/v2/everything?q={query}&language=pl&pageSize=5&apiKey={API_KEY}'

# Zapytanie
response = requests.get(url)
if response.status_code != 200:
    print("Błąd podczas pobierania danych:", response.status_code)
    exit()

data = response.json()

# Wyświetl artykuły
print(f"\n🔎 Artykuły dla zapytania: {query}")
for article in data.get("articles", []):
    print("\n📰", article["title"])
    print("   Źródło:", article["source"]["name"])
    print("   URL:", article["url"])
