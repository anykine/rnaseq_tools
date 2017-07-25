#!/bin/env python

import os, sys
import json
import argparse
sys.path.append("/home/rwang/rtwcode/rnaseq_tools/scripts")
from fastqc import *
from sge import *


def makeFastQCscripts(basedir, samples):

	for samp in samples:
		read1 = os.path.join(basedir, samp, "00-raw", samp+"_1.fastq.gz")
		read2 = os.path.join(basedir, samp, "00-raw", samp+"_2.fastq.gz")

		outputdir = os.path.join(basedir, samp, "02-FastQC" )
		if not os.path.exists(outputdir):
			os.makedirs(outputdir)
		
		outFileNamePrefix = os.path.join(outputdir, samp)
		fileList = " ".join([read1, read2]) # read1.gz read2.gz
		FastQC_obj = FastQC( outputdir, fileList=fileList)
		cmdtxt = FastQC_obj.makeCommand()

		qsub = SGE(samp, "/home/rwang/rtwcode/rnaseq_tools/templates/qsub_tophat.tmpl")
		args = {'command':cmdtxt, 'jobname': str(samp)+"FastQC", 'jobmem':'4G', 'logfilename': "_".join([str(samp), "FastQC.log"])}
		outscript = os.path.join(basedir,  samp, str(samp) + "_FastQC" + ".sh")
		print outscript
		qsub.createJobScript(outscript, **args)
		


if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("configfile", help="config file with options: eg config_tophat2.json")
	args = parser.parse_args()

	config = json.loads(open(args.configfile).read())
	makeFastQCscripts(config['basedir'], config['samples'] )
