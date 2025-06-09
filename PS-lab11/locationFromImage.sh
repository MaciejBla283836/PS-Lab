#!/bin/bash
read -p "Podaj ścieżke do zdjęcia" file
exiftool $file | grep GPS
