#!/bin/bash -e

if [ x$DIA_INPUT == x ] ; then
	echo "Must export DIA_INPUT=input fastq(s)"
	exit 1
fi

if [ x$DIA_REF == x ] ; then
	echo "Must export DIA_REF=mapping reference (.dmnd)"
	exit 1
fi

if [ x$DIA_OUT == x ] ; then
	echo "Must export DIA_OUT=output tsv filename"
	exit 1
fi


diamond blastx \
  --query $DIA_INPUT \
  --db $DIA_REF \
  --quiet \
  --mid-sensitive \
  --threads 10 \
  --max-target-seqs 1 \
  --outfmt 6 \
  --out $DIA_OUT
