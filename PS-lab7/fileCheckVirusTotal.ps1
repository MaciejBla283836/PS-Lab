$apiKey = "59e4e514ff9111c84e0c18fb03cdfe9d54e317359325b77621a7b9a278e82ebb"
$plik = "C:\Users\marce\Documents\Studia\Semestr_II\Programowanie_Skryptowe\PS-lab\PS-lab7\eicar.com"

# Oblicz SHA256
function Get-FileHashSHA256 {
    param ($filePath)
    return (Get-FileHash -Algorithm SHA256 -Path $filePath).Hash.ToLower()
}

$hash = Get-FileHashSHA256 -filePath $plik
Write-Host "Obliczona suma kontrolna (SHA256): $hash"

# Zapytanie do VirusTotal
$vtUrl = "https://www.virustotal.com/api/v3/files/$hash"

$headers = @{
    "x-apikey" = $apiKey
}

try {
    $response = Invoke-RestMethod -Uri $vtUrl -Headers $headers -Method GET
} catch {
    Write-Error "Błąd podczas komunikacji z VirusTotal: $_"
    exit
}

# Interpretacja odpowiedzi
$maliciousCount = $response.data.attributes.last_analysis_stats.malicious
$undetectedCount = $response.data.attributes.last_analysis_stats.undetected
$totalEngines = $maliciousCount + $undetectedCount + $response.data.attributes.last_analysis_stats.suspicious

Write-Host "`n--- Raport VirusTotal ---"
Write-Host "Malicious: $maliciousCount"
Write-Host "Undetected: $undetectedCount"
Write-Host "Liczba silników AV: $totalEngines"

if ($maliciousCount -gt 0) {
    Write-Warning "UWAGA: Plik został wykryty jako złośliwy przez $maliciousCount silnik(i)."
} else {
    Write-Host "Plik wydaje się być bezpieczny (brak wykryć)."
}
