#!/bin/env python

### -----------------------------------------
# Free for academic and nonprofit use
# Please keep this notice intact
# Copyright 2016 Richard T Wang (rtwang@mednet.ucla.edu)
### -----------------------------------------

import os, sys
import json
import argparse
sys.path.append('/home/rwang/rtwcode/rnaseq_tools/scripts')
from index import *
from tophat import *
from sge import *

# assumptions
# fastq file in 00-raw/ directory
# read pairs are _1.fastq.gz and _2.fastq.gz
# output script in scripts dir
# 
# inputs is json file called config_tophat2.json)

def makeTophat2Scripts(basedir, samples, reference='dmd427m'):
	Tophat2Index= Index(reference, "tophat2")
	(bowtieIndex, prebuiltIndex) = Tophat2Index.output()
	
	for samp in samples:
		read1 = os.path.join(basedir, samp, "00-raw", samp + "_1.fastq.gz")
		read2 = os.path.join(basedir, samp, "00-raw", samp + "_2.fastq.gz")
		if reference in ("dmd427m", "dmd427m_mm9"):
			outputdir = os.path.join(basedir, samp, "03-alignDMD")
		elif reference =="dmdgenomic":
			outputdir = os.path.join(basedir, samp, "03-alignDMDgenomic")
		else:
			outputdir = os.path.join(basedir, samp, "03-align")

		if not os.path.exists(outputdir):
			os.makedirs(outputdir)

		th = TophatAligner(bowtieIndex, samp,
			[ read1],
			[ read2],
			outputdir)
		th.prebuiltIndex = prebuiltIndex 
		cmdtxt = th.makeCommand()

		# TODO: rename accepted_hits.bam to <sample>_transcriptome.bam

		qsub = SGE(samp, "/home/rwang/rtwcode/rnaseq_tools/templates/qsub_tophat.tmpl")
		args = {'command':cmdtxt, 'jobname': str(samp)+str(reference), 'jobmem':'20G', 'logfilename': "_".join([str(samp), "tophat", str(reference)+".log"])}
		outscript = os.path.join(basedir,  samp, str(samp) + "_tophat_" + str(reference) + ".sh")
		print outscript
		qsub.createJobScript(outscript, **args)

if __name__=="__main__":
		parser = argparse.ArgumentParser()
		parser.add_argument("configfile", help="config file with options: eg config_tophat2.json")
		args = parser.parse_args()

		config = json.loads(open(args.configfile).read())
		# test if samples, basedir, reference are specified in JSON file
		if all(k in config for k in ('samples', 'basedir', 'reference')) :
			print config['samples']
			makeTophat2Scripts(config['basedir'], config['samples'], reference=config['reference'])

# generate all tophat scripts: 
# place config file in basedir and call this script
# eg ( scratch1/rnaseq/human/Feb12/config_tophat2.json)
# and call this dir

#config = json.loads(open("config_tophat2.json").read())
#print config['samples']
#makeTophat2Scripts(config['basedir'], config['samples'], reference=config['reference'])

#samples = [ "DDX8", "DDX9", "SH790"]
#basedir='/home/rwang/scratch1/rnaseq/human/Feb12/'
#makeTophat2Scripts(samples, reference='hg19')


