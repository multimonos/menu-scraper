#!/usr/bin/env bash

rm -f ./data/*.csv

for src in $(ls data/*.html); do 
  dst=${src/.html/.csv}
  python -u src/main.py parse $src --output=$dst 
  #python -u src/main.py parse $src --output=$dst --validate-output
done
