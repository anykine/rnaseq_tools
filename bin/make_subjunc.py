#!/bin/env python

import os, sys
import json
sys.path.append('/home/rwang/rtwcode/rnaseq_tools/scripts')
from index import *
from subjunc import *
from sge import *

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

def makeSubjuncScripts(basedir, samples, reference ):
	
	#transcriptIndex = '/share/apps/richard/kallisto/kallisto_linux-v0.42.5/index/ensembl_GRCh37_transcripts_index'
	transcriptIndex = reference
	for samp in samples:
		read1 = os.path.join(basedir, samp, "00-raw", samp + "_1.fastq.gz")
		read2 = os.path.join(basedir, samp, "00-raw", samp + "_2.fastq.gz")
		outputdir = os.path.join(basedir, samp, "05-subjunc")
		if not os.path.exists(outputdir):
			os.makedirs(outputdir)

		outputFile = samp + "_subjunc.bam"
		nameOfJob = samp + "subjunc"
		sj = SubjuncAligner(transcriptIndex, 
			[ read1],
			[ read2],
			outputFile,
			nameOfJob
			)
		cmdtxt = sj.makeCommand()
		print cmdtxt

		qsub = SGE(samp, "/home/rwang/rtwcode/rnaseq_tools/templates/qsub.tmpl")
		args = {'command':cmdtxt, 'jobname': str(samp)+"subjunc", 'jobmem':'20G', 'logfilename': "_".join([str(samp), "subjunc.log"])}
		outscript = os.path.join(basedir,  samp, str(samp) + "_subjunc" + ".sh")
		print outscript
		qsub.createJobScript(outscript, **args)

# generate all tophat scripts: 

#samples = [ "DDX7", "DDX8", "DDX9", "SH790"]
#basedir='/home/rwang/scratch1/rnaseq/human/Feb12/'
config = json.loads(open("config_subjunc.json").read())
makeKallistoScripts(config['basedir'], config['samples'], reference=config['reference'] )

