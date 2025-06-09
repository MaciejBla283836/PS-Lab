# Waluta od użytkownika
$waluta = Read-Host "Podaj kod waluty: (np. USD, EUR)"

# API
$nbpUrl = "https://api.nbp.pl/api/exchangerates/rates/A/$waluta/last/5?format=json"

try {
    $response = Invoke-RestMethod -Uri $nbpUrl -Method GET
} catch {
    Write-Error "Błąd podczas pobierania danych z NBP API: $_"
    exit
}

# Parsowanie i wyświetlanie wyników
$rates = $response.rates

Write-Host "--- Kurs waluty $waluta z ostatnich 5 dni roboczych ---"

for ($i = 0; $i -lt $rates.Count; $i++) {
    $date = $rates[$i].effectiveDate
    $value = [math]::Round($rates[$i].mid, 4)
    Write-Host "$date : $value zł"

    # Oblicz różnicę względem poprzedniego dnia
    if ($i -gt 0) {
        $diff = [math]::Round($rates[$i].mid - $rates[$i - 1].mid, 4)
        $sign = if ($diff -gt 0) { "+" } elseif ($diff -lt 0) { "-" } else { "" }
        Write-Host "   → Zmiana względem poprzedniego dnia: $sign$([math]::Abs($diff)) zł"
    }
}