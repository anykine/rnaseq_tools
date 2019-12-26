#!/bin/env python

import os, sys
import json
import argparse
sys.path.append("/home/rtwang/rtwcode/rnaseq_tools/scripts")
from star import *
from index import *
from sge import *

# Call variants from RNAseq using STAR aligner
# this is broad/gatk recommended workflow

def makeSTARScripts(basedir, samples, reference):

	# assume genome index file already exists (1st pass)
	# align 
	STARIndex = Index(reference, "STAR")
	index = STARIndex.output()

	for samp in samples:
		read1 = os.path.join(basedir, samp, "00-raw", samp+"_1.fastq.gz")
		read2 = os.path.join(basedir, samp, "00-raw", samp+"_2.fastq.gz")

		outputdir = os.path.join(basedir, samp, "03-alignSTAR"+reference )
		if not os.path.exists(outputdir):
			os.makedirs(outputdir)
		outFileNamePrefix = os.path.join(outputdir, samp)

        # lowered the number of threads from 24 to 8 to prevent "cannot create output file,
        # check ulimit ERROR
		sa = STARAligner( index, read1, read2, outFileNamePrefix, bamout=True,
                threads=8, mem='50G')
		cmdtxt = sa.makeCommand()

		qsub = SGE(samp, "/home/rtwang/rtwcode/rnaseq_tools/templates/qsub.tmpl")
		args = {'command':cmdtxt, 'jobname': str(samp)+str(reference),
                'jobmem':'50G', 'logfilename': "_".join([str(samp), "STAR", str(reference)+".log"])}
		outscript = os.path.join(basedir,  samp, str(samp) + "_STAR_" + str(reference) + ".sh")
		print outscript
		qsub.createJobScript(outscript, **args)
		


if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("configfile", help="config file with options: eg config_tophat2.json")
	args = parser.parse_args()

	config = json.loads(open(args.configfile).read())
	makeSTARScripts(config['basedir'], config['samples'], config['reference'])
