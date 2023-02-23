#!/bin/bash -e

bowtie2 \
  --very-sensitive-local \
  --non-deterministic \
  --no-hd \
  -1 $FASTQ_R1 \
  -2 $FASTQ_R2 \
  -D 20 \
  -R 3 \
  -N 0 \
  -L 16 \
  -i S,1,0.50 \
  -I 0 \
  -X 2000 \
  -x $BOW_REF \
  -p 10 \
  -S $BOW_OUT
