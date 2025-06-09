# Ścieżki
$sourceFolder = "C:\Users\marce\Documents\Studia\Semestr_II\Programowanie_Skryptowe\PS-lab\PS-lab7\watchFolderSrc"
$destinationFolder = "C:\Users\marce\Documents\Studia\Semestr_II\Programowanie_Skryptowe\PS-lab\PS-lab7\watchFolderDes"

# Utwórz folder docelowy, jeśli nie istnieje
if (-not (Test-Path -Path $destinationFolder)) {
    New-Item -ItemType Directory -Path $destinationFolder
    Write-Host "Utworzono folder docelowy: $destinationFolder"
}

# Utwórz obiekt FileSystemWatcher
$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = $sourceFolder
$watcher.Filter = "*.txt"
$watcher.IncludeSubdirectories = $false
$watcher.EnableRaisingEvents = $true

# Zdefiniuj akcję przy wykryciu nowego pliku
$action = {
    Start-Sleep -Milliseconds 500  # Małe opóźnienie, aby upewnić się, że plik został w pełni zapisany
    $filePath = $Event.SourceEventArgs.FullPath
    $fileName = $Event.SourceEventArgs.Name
    $destinationPath = Join-Path -Path $destinationFolder -ChildPath $fileName

    try {
        Move-Item -Path $filePath -Destination $destinationPath -Force
        Write-Host "Przeniesiono plik: $fileName"
    }
    catch {
        Write-Warning "Błąd podczas przenoszenia pliku $fileName"
    }
}

# Zarejestruj zdarzenie
Register-ObjectEvent -InputObject $watcher -EventName Created -Action $action | Out-Null

Write-Host "Monitorowanie folderu: $sourceFolder"
Write-Host "Naciśnij Ctrl + C, aby zakończyć"

# Zapobiega zamknięciu skryptu
while ($true) {
    Start-Sleep -Seconds 1
}
