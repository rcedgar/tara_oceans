#!/bin/bash -e

mkdir -p tara_data
mkdir -p edgar_results

grep "^This study" tara_data/TableS6.tsv \
  | cut -f8 \
  | sort \
  | uniq -c \
  | sort -nr \
  | sed "-es/New_12at1.1/New_12at1.1  (Taraviricota)/" \
  | sed "-es/New_14at1.1/New_14at1.1  (Pomiviricota)/" \
  | sed "-es/New_16at1.1/New_16at1.1  (Paraxenoviricota)/" \
  | sed "-es/New_17at1.1/New_17at1.1  (Lenar-like)/" \
  | sed "-es/New_18at1.1/New_18at1.1  (Wamoviricota)/" \
  | sed "-es/New_19at1.1/New_19at1.1  (Arctiviricota)/" \
  | sed '-es/"//g' \
  | sed "-es/^  *//" \
  | sed "-es/  */	/" \
  > edgar_results/Edgar_Table1.tsv

./inf_clustercount.py \
  > edgar_results/inf_clustercount.tsv

./megacluster_summary.py \
  > edgar_results/megacluster_summary.tsv

./adjusted_rand_index.py \
  > edgar_results/adjusted_rand_index.tsv
