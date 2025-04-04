#!/usr/bin/env bash

python -u src/main.py \
  merge-batch \
  --find="data/*.csv" \
  --group-by=".+locations-(.+?)-menu-.+"

