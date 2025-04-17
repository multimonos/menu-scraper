#!/usr/bin/env bash

python -u src/main.py \
  merge-batch \
  --find="data/*.csv" \
  --group-by=".+locations-(.+?)-menu-.+"

# check header rowcount
# for x in $(ls data/merged*.csv); do
#   echo $x
#   cat $x |grep 'action' |wc -l
# done

