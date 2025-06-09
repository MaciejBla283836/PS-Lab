#!/bin/bash

# Plik, do którego zostanie zapisany raport
REPORT_FILE="./raport_ssh_$(date +%F_%H-%M-%S).log"

# Czas trwania
CZAS="--since $(date -d 'yesterday' '+%Y-%m-%d')"

# Generowanie raportu
echo "Generowanie raportu z logów systemd-journald (SSH)"
echo "Czas wygenerowania: $(date)" > "$REPORT_FILE"
echo "----------------------------------------" >> "$REPORT_FILE"

# Nieudane logowania
echo -e "\n[!] Nieudane logowania:" >> "$REPORT_FILE"
journalctl $CZAS -u ssh.service | grep "Failed password" >> "$REPORT_FILE"

# Próby logowania na nieistniejących użytkowników
echo -e "\n[!] Próby logowania na nieistniejących użytkowników:" >> "$REPORT_FILE"
journalctl $CZAS -u ssh.service | grep "Invalid user" >> "$REPORT_FILE"

# Udane logowania
echo -e "\n[!] Udane logowania:" >> "$REPORT_FILE"
journalctl $CZAS -u ssh.service | grep "Accepted password" >> "$REPORT_FILE"

# Inne potencjalne błędy uwierzytelniania
echo -e "\n[!] Inne ostrzeżenia związane z uwierzytelnianiem:" >> "$REPORT_FILE"
journalctl $CZAS -u ssh.service | grep "authentication failure" >> "$REPORT_FILE"

# Zakończenie
echo -e "\nRaport został zapisany do: $REPORT_FILE"
