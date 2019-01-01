#!/bin/sh
#
# make_dirs.sh
#
#
# generate the persample directories (00-raw)
# for rnaseq/exome analysis
#
# Richard T Wang (rtwang@mednet.ucla.edu)

# Usage
# 1. create the directories
# you can call in a loop like this
# for i in *_1.fastq.gz; do make_dirs /basedir/path/ ${i%%_1.fastq.gz}; done
#
# 2. mv FASTQ files to the 00-raw directory
# for i in *_1.fastq.gz; do bname=${i%%_1.fastq.gz}; echo $bname; mv $bname*.fastq.gz $bname/00-raw ; done
#

# base directory eg projects/DMDmodifier/180101/
basedir=$1
# sample: CDMD1001
sample=$2

if [[ $sample =~ ^CDMD ]]
then
	echo $sample
	fullsamplename=$sample
else
	echo "adding CDMD to $sample"
	fullsamplename="CDMD$sample"
fi


# make the directories

echo "creating directory  $basedir/$fullsamplename/00-raw"
mkdir -p $basedir/$fullsamplename/00-raw

