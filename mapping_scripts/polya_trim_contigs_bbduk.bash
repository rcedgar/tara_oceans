#!/bin/bash -e

infa=../ref/44779_RdRP_contigs.fna

input=`readlink -f $infa`
outname=contigs

if [ x$outname == x ] ; then
	echo Missing outname
	exit 1
fi

if [ ! -s $input ] ; then
	echo Not found input=$input
	exit 1
fi

outdir=$d/int/tara_geo2/polyatrimmed
mkdir -p $outdir
cd $outdir

rm -rf ../tmp
mkdir -p ../tmp
mkdir -p ../bblog
log=../bblog/$outname

export PATH=$PATH:$d/sw/bbtools/bbmap

/bin/ls -l $input > $log

bbduk.sh \
  in=$input \
  out=../tmp/bbout \
  trimpolya=3 \

/bin/ls -l ../tmp/bbout > $log

for n in 1 2 3
do
	rm -f ../tmp/bbin
	mv -v ../tmp/bbout ../tmp/bbin

	bbduk.sh \
	  in=../tmp/bbin \
	  out=../tmp/bbout \
	  literal=AAAAAAAAAA,TTTTTTTTTT \
	  hdist=2 \
	  k=10 \
	  ktrim=r \
	  restrictright=20
	/bin/ls -l ../tmp/bbout >> $log

	rm -f ../tmp/bbin
	mv -v ../tmp/bbout ../tmp/bbin
	bbduk.sh \
	  in=../tmp/bbin \
	  out=../tmp/bbout \
	  literal=AAAAAAAAAA,TTTTTTTTTT \
	  hdist=2 \
	  k=10 \
	  ktrim=l \
	  restrictright=20
	/bin/ls -l ../tmp/bbout >> $log
done

rm -f ../tmp/bbin
mv -v ../tmp/bbout ../tmp/bbin
bbduk.sh \
  in=../tmp/bbin \
  out=../tmp/bbout \
  trimpolya=3
/bin/ls -l ../tmp/bbout >> $log

mv -v ../tmp/bbout ../polyatrimmed/$outname
/bin/ls -l ../polyatrimmed/$outname >> $log
