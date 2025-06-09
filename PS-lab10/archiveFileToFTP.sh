#!/bin/bash

# Co archiwizować
SOURCE_DIRS="/home/mamari/Documents/Studia/Semestr_II/Programowanie_Skryptowe/Lab2/ /home/mamari/Documents/Studia/Semestr_II/Programowanie_Skryptowe/Lab4/"

# Ścieżka lokalna do zapisu kopii
BACKUP_DIR="/home/mamari/Documents/Backup"

# Nazwa pliku backupu
BACKUP_NAME="backup_$(date +%F_%H-%M-%S).tar.gz"
ARCHIVE_PATH="${BACKUP_DIR}/${BACKUP_NAME}"

# Dane logowania FTP
FTP_HOST="KALI-LINUX"
FTP_USER="mamari"
FTP_TARGET_DIR="/kopie_zapasowe"

# Upewnij się, że katalog na backupy istnieje
mkdir -p "$BACKUP_DIR"

# Tworzenie archiwum
echo "Tworzę archiwum: $ARCHIVE_PATH"
tar -czf "$ARCHIVE_PATH" $SOURCE_DIRS

if [ $? -ne 0 ]; then
    echo "[!] Błąd podczas archiwizacji. Przerywam."
    exit 1
fi

echo "Wysyłam archiwum na serwer FTP..."

# Wysyłka pliku przy użyciu ftp (non-interactive)
ftp -inv "$FTP_HOST" <<EOF
user $FTP_USER
cd $FTP_TARGET_DIR
put "$ARCHIVE_PATH"
bye
EOF

if [ $? -eq 0 ]; then
    echo "Backup został wysłany na serwer FTP pomyślnie."
else
    echo "Wystąpił błąd podczas wysyłania pliku na FTP."
fi

