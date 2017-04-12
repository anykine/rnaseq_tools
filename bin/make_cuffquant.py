#!/bin/env python

import os, sys
import json
import argparse
import re
import shutil
sys.path.append("/home/rwang/rtwcode/rnaseq_tools/scripts/")
from cuffquant import CuffQuant 
from sge import SGE

def makeCuffQuantScripts(samples, basedir, reference):

	for samp in samples:
		outputDir=os.path.join(basedir, samp, '05-cuffquant')
		if not os.path.exists(outputDir):
			os.makedirs(outputDir)

		if reference in ("hg19", "mm9"):
			# rename file 
			bamfile=os.path.join(basedir, samp, "03-align", "accepted_hits.bam")
			newbamfile=os.path.join(basedir, samp, "03-align", samp + "_transcriptome.bam")
			if os.path.isfile(bamfile) and not os.path.isfile(newbamfile):
				#newbamfile=os.path.join(basedir, samp, "03-align", samp + "_transcriptome.bam")
				print bamfile
				print newbamfile
				#shutil.copy(bamfile, newbamfile)
				shutil.move(bamfile, newbamfile)
			else:
				print "does exist"

		#bampath=os.path.join(basedir, samp, "03-align"
		"""name bam file is always <SAMPLENAME>_transcriptome.bam"""
		cq = CuffQuant(annotationFile='/home/rwang/indexes/hg19/igenomes/Homo_sapiens/Ensembl/GRCh37/Annotation/Genes/genes.gtf', 
			bamfile=os.path.join(basedir,  samp, "03-align", str(samp)+"_transcriptome.bam"),
			outputDir=outputDir)

		cmdtxt = cq.makeCommand()
		print cmdtxt

		qsub = SGE(samp, '/home/rwang/rtwcode/rnaseq_tools/templates/qsub_tophat.tmpl')
		args = {'command':cmdtxt, 'jobname': str(samp)+"_cuffquant", 'jobmem':'20G', 'logfilename': "_".join([str(samp), "cuffquant.log"])}
		outscript = os.path.join(basedir, samp, str(samp)+"_cuffquant.sh")
		print outscript
		qsub.createJobScript(outscript, **args)


if __name__=="__main__":
		parser = argparse.ArgumentParser()
		parser.add_argument("configfile", help="config file with options: eg config_tophat2.json")
		args = parser.parse_args()

		config = json.loads(open(args.configfile).read())
		# test if samples, basedir, reference specified in JSON file
		if all(k in config for k in ('samples', 'basedir', 'reference')):
			print config['samples']
			makeCuffQuantScripts(config['samples'], config['basedir'], config['reference'])
		else:
			print "JSON file is missing samples, basedir or reference section"

#samples = ["DDX7",  "DDX8", "DDX9", "SH790"]
#basedir='/home/rwang/scratch1/rnaseq/human/Feb12/'
#config = json.loads(open("config_tophat2.json").read())
#makeCuffQuantScripts(config['samples'], config['basedir'], config['reference'])

