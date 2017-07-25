#!/bin/env python

import os, sys
import json
import argparse
sys.path.append("/home/rwang/rtwcode/rnaseq_tools/scripts")
from star import *
from index import *
from sge import *

# follow macarthur lab 2pass alignment of muscle dystrophy samples
# this is specifcally for the 2nd pass where we use
# a merged and filtered index that was generated previously

def makeSTAR2passMendelianSeq(basedir, samples, mergedReference, outdir):
	pass

	# assume genome index file already exists (1st pass)
	# align 
	#STARIndex = Index(reference, "STAR")
	#index = STARIndex.output()

	index = mergedReference
	reference = "MendelianSeq"

	for samp in samples:
		read1 = os.path.join(basedir, samp, "00-raw", samp+"_1.fastq.gz")
		read2 = os.path.join(basedir, samp, "00-raw", samp+"_2.fastq.gz")

		# 1st pass alignment
		outputdir = os.path.join(basedir, samp, outdir)
		if not os.path.exists(outputdir):
			os.makedirs(outputdir)
		outFileNamePrefix = os.path.join(outputdir, samp)
		sa = STARAligner( index, read1, read2, outFileNamePrefix, bamout=True, threads=48, mem='100G')
		cmdtxt = sa.makeCommand()

		qsub = SGE(samp, "/home/rwang/rtwcode/rnaseq_tools/templates/qsub_tophat.tmpl")
		args = {'command':cmdtxt, 'jobname': str(samp)+str(reference), 'jobmem':'100G', 'logfilename': "_".join([str(samp), "STAR2passMendelianSeq", str(reference)+".log"])}
		outscript = os.path.join(basedir,  samp, str(samp) + "_STAR2passMendelianSeq_" + str(reference) + ".sh")
		print outscript
		qsub.createJobScript(outscript, **args)
		


if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("configfile", help="config file with options: eg config_STAR2passMendelian.json")
	args = parser.parse_args()

	config = json.loads(open(args.configfile).read())
	makeSTAR2passMendelianSeq(config['basedir'], config['samples'], config['mergedReference'], config['outdir'])
