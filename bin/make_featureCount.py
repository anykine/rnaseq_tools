#!/bin/env python

import os, sys
import json
import argparse
sys.path.append('/home/rtwang/rtwcode/rnaseq_tools/scripts')
from featureCount import *
from sge import *
from gtf import *

# assumptions
# fastq file in 00-raw/ directory
# read pairs are _1.fastq.gz and _2.fastq.gz
# output script in scripts dir
# 
# inputs:
# samplename: DDX7
# tophat output dir
# script output dir
# basedir
# reference (hg19, dmd transcript)

# TODO
#  FC needs to search the correct directory for the BAM file
#  abstract GTF file location
#  

def makeFeatureCountScripts( samples, basedir, annot, bamtype='STAR',
        bamdir="03-alignSTAR"):

    #ANNOT='/home/rwang/scratch1/rnaseq/datasets/gencode/release24/gencode.v24lift37.basic.annotation.gtf'
    #ANNOT='/home/rwang/indexes/hg19/igenomes/Homo_sapiens/Ensembl/GRCh37/Annotation/Genes/genes.gtf'
    annotParams= annot.split("-")
    #gtf = Gtf("GRCh37", "ensembl", "human").output()
    gtf = Gtf(annotParams[0], annotParams[1], annotParams[2]).output()

    for samp in samples:
        if bamtype=="tophat2":
            bamfile = os.path.join(basedir, samp, "03-align", samp+"_transcriptome.bam")
        elif bamtype=="STAR":
            if bamdir:
                bamfile = os.path.join(basedir, samp, bamdir,
                        samp+"Aligned.sortedByCoord.out.bam")
            else:
                bamfile = os.path.join(basedir, samp, "03-alignSTAR", samp+"Aligned.sortedByCoord.out.bam")
        else: 
            sys.exit("bamtype paramter must be 'tophat' or 'STAR'")

        outputdir = os.path.join(basedir, samp, "05-featureCount")
        if not os.path.exists(outputdir):
            os.makedirs(outputdir)

        fc = FeatureCount(gtf, samp,
            bamfile,
            outputdir
            )
        cmdtxt = fc.makeCommand()
        print cmdtxt

        qsub = SGE(samp, "/home/rtwang/rtwcode/rnaseq_tools/templates/qsub.tmpl")
        args = {'command':cmdtxt, 'jobname': str(samp)+"featurecounts", 'jobmem':'20G', 'logfilename': "_".join([str(samp), "featurecounts.log"])}
        outscript = os.path.join(basedir,  samp, str(samp) + "_featurecounts" + ".sh")
        print outscript
        qsub.createJobScript(outscript, **args)
#
# generate all tophat scripts: 
# iterate over all all samples: ddx7/8/9/sh790
# iterate over index hg19, dmd427m (human)
#samples = [ "DDX7", "DDX8", "DDX9", "SH790"]
#samples = [ "DDX7" ]
#bams = [ "DDX7_transcriptome.bam", "accepted_hits.bam", "accepted_hits.bam", "accepted_hits.bam"]
#samplesAndBams = zip(samples, bams)
##samples = ["D1", "D2"]
#basedir='/home/rwang/scratch1/rnaseq/human/Feb12/'
#makeFeatureCountScripts(samplesAndBams )

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("configfile", help="config file with options: eg config_featureCounts.json")
    args = parser.parse_args()

    config = json.loads(open(args.configfile).read())
    # test if samples, basedir, reference are specified in JSON file
    if all(k in config for k in ('samples', 'basedir', 'annotation')) :
        if 'bamtype' in config.keys():
            bamtype=config['bamtype']
        else:
            bamtype='STAR'
        print "samples are " + " ".join(config['samples'])
        print "bamtype is " + str(bamtype)
        makeFeatureCountScripts(config['samples'], config['basedir'], annot=config['annotation'], bamtype=bamtype)

