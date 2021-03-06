#!/bin/env python

import os, sys
import json
sys.path.append('/home/rwang/rtwcode/rnaseq_tools/scripts')
from index import *
from splicetrap import *
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

def makeSpliceTrapScripts(basedir, samples, reference, readsize, cutoff ):
	
	#transcriptIndex = '/share/apps/richard/kallisto/kallisto_linux-v0.42.5/index/ensembl_GRCh37_transcripts_index'
	transcriptIndex = reference
	numThreads = 4
	for samp in samples:
		# hack to decompress fastq.gz on the fly, does not work
		#read1 = "<(gunzip -c " + os.path.join(basedir, samp, "00-raw", samp + "_1.fastq.gz") + ")"
		#read2 = "<(gunzip -c " + os.path.join(basedir, samp, "00-raw", samp + "_2.fastq.gz") + ")"

		# need to check if fastq is GZIPPED and uncompress first if so
		read1 = os.path.join(basedir, samp, "00-raw", samp + "_1.fastq") 
		read2 = os.path.join(basedir, samp, "00-raw", samp + "_2.fastq") 

		if not os.path.isfile(read1):
			read1gz = os.path.join(basedir, samp, "00-raw", samp + "_1.fastq.gz") 
			read2gz = os.path.join(basedir, samp, "00-raw", samp + "_2.fastq.gz") 
			cmdtxt =  "gunzip -c " + read1gz + " > " + os.path.join(basedir, samp, "00-raw", samp + "_1.fastq") + "\n"
			cmdtxt += "gunzip -c " + read2gz + " > " + os.path.join(basedir, samp, "00-raw", samp + "_2.fastq") + "\n"

		outputdir = os.path.join(basedir, samp, "05-splicetrap")
		if not os.path.exists(outputdir):
			os.makedirs(outputdir)
		outputFilePrefix = samp

		nameOfJob = samp + "splicetrap"
		sj = SpliceTrap(readsize,
						cutoff,
						outputFilePrefix,
						outputdir,
						numThreads,
			 			read1,
			 			read2,
						nameOfJob,
						reference
			)
		cmdtxt += sj.makeCommand()
	
		print cmdtxt

		qsub = SGE(samp, "/home/rwang/rtwcode/rnaseq_tools/templates/qsub.tmpl")
		args = {'command':cmdtxt, 'jobname': str(samp)+"splicetrap", 'jobmem':'20G', 'logfilename': "_".join([str(samp), "splicetrap.log"])}
		outscript = os.path.join(basedir,  samp, str(samp) + "_splicetrap" + ".sh")
		print outscript
		qsub.createJobScript(outscript, **args)
		cmdtxt = ""

# generate all tophat scripts: 

#samples = [ "DDX7", "DDX8", "DDX9", "SH790"]
#basedir='/home/rwang/scratch1/rnaseq/human/Feb12/'
config = json.loads(open("config_splicetrap.json").read())
makeSpliceTrapScripts(config['basedir'], config['samples'], config['reference'], config['readsize'], config['cutoff']  )

