#!/bin/bash

# Dane logowania
REMOTE_USER="mamari"
REMOTE_HOST="KALI-LINUX"
REMOTE_PORT=22  # domyślnie 22, zmień jeśli trzeba
OUTPUT_FILE="wynik_zdalny.txt"

# Polecenia do wykonania na zdalnym serwerze
REMOTE_COMMANDS="echo '--- LISTA PLIKÓW ---'; ls -l; echo '--- PROCESY ---'; ps aux"

# Połączenie SSH i wykonanie poleceń
ssh -p $REMOTE_PORT ${REMOTE_USER}@${REMOTE_HOST} "$REMOTE_COMMANDS" > "$OUTPUT_FILE"

# Komunikat po zakończeniu
if [ $? -eq 0 ]; then
    echo "Polecenia zostały wykonane poprawnie. Wynik zapisano w $OUTPUT_FILE"
else
    echo "Wystąpił błąd podczas połączenia SSH lub wykonywania poleceń."
fi

