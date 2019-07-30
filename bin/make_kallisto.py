#!/bin/env python

import os, sys
import json
sys.path.append('/home/rtwang/rtwcode/rnaseq_tools/scripts')
from index import *
from kallisto import *
from sge import *
from siteconfig import *

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

def makeKallistoScripts(basedir, samples, reference, bootstrapSamples=False ):
	
	#transcriptIndex = '/share/apps/richard/kallisto/kallisto_linux-v0.42.5/index/ensembl_GRCh37_transcripts_index'
	transcriptIndex= Index(reference, "kallisto").output()

	for samp in samples:
		read1 = os.path.join(basedir, samp, "00-raw", samp + "_1.fastq.gz")
		read2 = os.path.join(basedir, samp, "00-raw", samp + "_2.fastq.gz")
		outputdir = os.path.join(basedir, samp, "05-kallisto")
		if not os.path.exists(outputdir):
			os.makedirs(outputdir)

		ka = KallistoAligner(transcriptIndex, samp,
			[ read1],
			[ read2],
			outputdir,
            bootstrapSamples,
			"quant")
		cmdtxt = ka.makeCommand()
		print cmdtxt

		qsub = SGE(samp, "/home/rtwang/rtwcode/rnaseq_tools/templates/qsub.tmpl")
		args = {'command':cmdtxt, 'jobname': str(samp)+"kallisto", 'jobmem':'20G', 'logfilename': "_".join([str(samp), "kallisto.log"])}
		outscript = os.path.join(basedir,  samp, str(samp) + "_kallisto" + ".sh")
		print outscript
		qsub.createJobScript(outscript, **args)


# TODO - need to add bootstrapSamples as default
config = json.loads(open("config_kallisto.json").read())
if 'bootstrapSamples' not in  config:
    config['bootstrapSamples'] = False
print config
makeKallistoScripts(config['basedir'], config['samples'],
        reference=config['reference'] ,
        bootstrapSamples=config['bootstrapSamples'])

