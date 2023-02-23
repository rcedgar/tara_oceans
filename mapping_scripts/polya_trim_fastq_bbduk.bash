#!/bin/bash -e

input=`readlink -f $1`
outname=$2

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
  out=../tmp/bbout.fq \
  trimpolya=3 \
  minlength=30

/bin/ls -l ../tmp/bbout.fq > $log

for n in 1 2 3
do
	rm -f ../tmp/bbin.fq
	mv -v ../tmp/bbout.fq ../tmp/bbin.fq

	bbduk.sh \
	  in=../tmp/bbin.fq \
	  out=../tmp/bbout.fq \
	  literal=AAAAAAAAAA,TTTTTTTTTT \
	  hdist=2 \
	  k=10 \
	  minlength=30 \
	  ktrim=r \
	  restrictright=20

	echo >> $log
	/bin/ls -l ../tmp/bbin.fq >> $log
	/bin/ls -l ../tmp/bbout.fq >> $log

	rm -f ../tmp/bbin.fq
	mv -v ../tmp/bbout.fq ../tmp/bbin.fq
	bbduk.sh \
	  in=../tmp/bbin.fq \
	  out=../tmp/bbout.fq \
	  literal=AAAAAAAAAA,TTTTTTTTTT \
	  hdist=2 \
	  k=10 \
	  minlength=30 \
	  ktrim=l \
	  restrictright=20

	echo >> $log
	/bin/ls -l ../tmp/bbin.fq >> $log
	/bin/ls -l ../tmp/bbout.fq >> $log
done

rm -f ../tmp/bbin.fq
mv -v ../tmp/bbout.fq ../tmp/bbin.fq
bbduk.sh \
  in=../tmp/bbin.fq \
  out=../tmp/bbout.fq \
  trimpolya=3 \
  minlength=30

echo >> $log
/bin/ls -l ../tmp/bbin.fq >> $log
/bin/ls -l ../tmp/bbout.fq >> $log

mv -v ../tmp/bbout.fq ../polyatrimmed/$outname
/bin/ls -l ../polyatrimmed/$outname >> $log
