#!/bin/env python

import os, sys
import json
import argparse
sys.path.append("/home/rwang/rtwcode/rnaseq_tools/scripts")
from star import *
from index import *
from sge import *

# Call variants from RNAseq using STAR aligner
# this is broad/gatk recommended workflow

def makeSTARVariantScripts(basedir, samples, reference):
	pass

	# assume genome index file already exists (1st pass)
	# align 
	STARIndex = Index(reference, "STAR")
	index = STARIndex.output()

	for samp in samples:
		read1 = os.path.join(basedir, samp, "00-raw", samp+"_1.fastq.gz")
		read2 = os.path.join(basedir, samp, "00-raw", samp+"_2.fastq.gz")

		# 1st pass alignment
		outputdir = os.path.join(basedir, samp, "07-variants", "step1align")
		if not os.path.exists(outputdir):
			os.makedirs(outputdir)
		outFileNamePrefix = os.path.join(outputdir, samp)
		sa = STARAligner( index, read1, read2, outFileNamePrefix, bamout=True, threads=48, mem='100G')
		cmdtxt = sa.makeCommand()

		#make 2nd index using SJ from 1st pass
		outputdir2 = os.path.join(basedir, samp, "07-variants", "step2reindex")
		if not os.path.exists(outputdir2):
			os.makedirs(outputdir2)
		hg19fasta = "/home/rwang/indexes/hg19/igenomes/Homo_sapiens/Ensembl/GRCh37/Sequence/WholeGenomeFasta/genome.fa"
		si = STARIndexCreator(outputdir2, hg19fasta,
						SJout= os.path.join(outputdir, samp+"SJ.out.tab"),
						SJoverhang = 75)
		cmdtxt = cmdtxt + "\n" + si.makeCommand()

		print cmdtxt

		# second alignment
		outputdir3 = os.path.join(basedir, samp, "07-variants", "step3align2")
		if not os.path.exists(outputdir3):
			os.makedirs(outputdir3)
		outFileNamePrefix2 = os.path.join(outputdir3, samp)
		sa = STARAligner( outputdir2, read1, read2, outFileNamePrefix2, bamout=True, threads=48, mem='100G')

		cmdtxt = cmdtxt + "\n" + sa.makeCommand()

		qsub = SGE(samp, "/home/rwang/rtwcode/rnaseq_tools/templates/qsub_tophat.tmpl")
		args = {'command':cmdtxt, 'jobname': str(samp)+str(reference), 'jobmem':'100G', 'logfilename': "_".join([str(samp), "STAR", str(reference)+".log"])}
		outscript = os.path.join(basedir,  samp, str(samp) + "_STAR2pass_" + str(reference) + ".sh")
		print outscript
		qsub.createJobScript(outscript, **args)
		


if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("configfile", help="config file with options: eg config_tophat2.json")
	args = parser.parse_args()

	config = json.loads(open(args.configfile).read())
	makeSTARVariantScripts(config['basedir'], config['samples'], config['reference'])
