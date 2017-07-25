#!/bin/env python

import os, sys
import json
import argparse
sys.path.append("/home/rwang/rtwcode/rnaseq_tools/scripts")
from samtools import *
from sge import *

# Index all bam files 

def makeBamfileIndex(basedir, samples ):

	for samp in samples:
		fullcmdtxt = ""
		for subdir in ["03-align", "03-alignDMD", "03-alignSTAR"]:
			if subdir=="03-alignSTAR":
				bamfilePath = os.path.join(basedir, samp, subdir, samp+"Aligned.sortedByCoord.out.bam")
				sa = Samtools( "index", bamfilePath)
				cmdtxt = sa.makeCommand()
			elif subdir=="03-align": 
				bamfilePath = os.path.join(basedir, samp, subdir, samp+"_transcriptome.bam")
				sa = Samtools( "index", bamfilePath)
				cmdtxt = sa.makeCommand()
			elif subdir=="03-alignDMD":
				bamfilePath = os.path.join(basedir, samp, subdir, samp+"_427m.bam")
				sa = Samtools( "index", bamfilePath)
				cmdtxt = sa.makeCommand()

			fullcmdtxt = fullcmdtxt +  cmdtxt + "\n"
		print fullcmdtxt

		qsub = SGE(samp, "/home/rwang/rtwcode/rnaseq_tools/templates/qsub_tophat.tmpl")
		args = {'command':fullcmdtxt, 'jobname': str(samp)+"index", 'jobmem':'10G', 'logfilename': "_".join([str(samp), "index.log"])}
		outscript = os.path.join(basedir,  samp, str(samp) + "_bamindex.sh")
		print outscript
		qsub.createJobScript(outscript, **args)
		

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("configfile", help="config file with options: eg config_tophat2.json")
	args = parser.parse_args()

	config = json.loads(open(args.configfile).read())
	makeBamfileIndex(config['basedir'], config['samples'])
