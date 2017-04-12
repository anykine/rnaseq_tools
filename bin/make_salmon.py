#!/bin/env python

import os, sys
import json
sys.path.append('/home/rwang/rtwcode/rnaseq_tools/scripts')
from index import *
from salmon import *
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

def makeSalmonScripts(basedir, samples, reference, libtype ):
	
	#transcriptIndex = '/share/apps/richard/Salmon/SalmonBeta-0.6.1_DebianSqueeze/index/ensembl_GRCh37_transcripts_salmon_index'
	transcriptIndex = reference
	for samp in samples:
		read1 = os.path.join(basedir, samp, "00-raw", samp + "_1.fastq.gz")
		read2 = os.path.join(basedir, samp, "00-raw", samp + "_2.fastq.gz")
		outputdir = os.path.join(basedir, samp, "05-salmon")
		if not os.path.exists(outputdir):
			os.makedirs(outputdir)
		libType = "ISF"

		sa = SalmonAligner(transcriptIndex, samp,
			[ read1],
			[ read2],
			outputdir,
			libType,
			"quant")
		cmdtxt = sa.makeCommand()
		print cmdtxt

		qsub = SGE(samp, "/home/rwang/rtwcode/rnaseq_tools/templates/qsub_tophat.tmpl")
		args = {'command':cmdtxt, 'jobname': str(samp)+"salmon", 'jobmem':'4G', 'logfilename': "_".join([str(samp), "salmon.log"])}
		outscript = os.path.join(basedir,  samp, str(samp) + "_salmon" + ".sh")
		print outscript
		qsub.createJobScript(outscript, **args)

# generate all tophat scripts: 

#samples = [ "DDX7", "DDX8", "DDX9", "SH790"]
#basedir='/home/rwang/scratch1/rnaseq/human/Feb12/'
config=json.loads(open("config_salmon.json").read())
makeSalmonScripts(config['basedir'], config['samples'], config['reference'], config['libtype'] )

