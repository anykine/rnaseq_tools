#!/bin/env python

import os
import sys
import subprocess

class TophatAligner(object):
	"""Wrapper around Tophat aligner"""
	def __init__(self, bowtieIndexPath, nameOfJob, reads1, reads2, outputDir):
		self.threads = 8
		self.exe = "/share/apps/tophat-2.0.14.Linux_x86_64/tophat"
		# specify the bowtie2 index file (reference genome index base)
		self.bowtieIndex = bowtieIndexPath
		self.name = nameOfJob 
		self.prebuiltIndex = None
		self.noNovelJuncs = False
		self.CoverageSearch = True

		#reads1 is a list of 1st pair or SE reads, reads2 is list of 2nd pair
		#	if single end, pass empty list for read2 []	
		if len(reads2) > 0:
			self.paired = True
			self.reads1 = reads1
			self.reads2 = reads2
		else:
			self.paired = False
			self.reads1 = reads1

		self.outputDir = outputDir

	def makeCommand(self):
		"""generate commandline"""
		arglist = ["%s" % self.exe ]
		arglist.extend([ "-p %s " % self.threads ])
		arglist.extend([ "-o %s " % self.outputDir  ])
		if self.prebuiltIndex is not None:
			arglist.extend([ "--transcriptome-index=%s" % self.prebuiltIndex ])

		if self.noNovelJuncs == True:
			arglist.extend([ "--no-novel-juncs" ])

		#if self.CoverageSearch == False:
		arglist.extend([ "--no-coverage-search"])

		arglist.extend([ "%s" % self.bowtieIndex])
		arglist.extend([ "%s " % ",".join(self.reads1 ) ])

		if self.paired == True:
			arglist.extend([ "%s " % ",".join(self.reads2 ) ])

		cmd =  " ".join(arglist)

		#kw={'exe':'testexe', 'jobresource':"excl=true", 'joboutdir':"/home/rwang", "jobname":'test'}
		#templ = Template(filename='qsub_star.tmpl')
		#res = templ.render(**kw)
		#print res
		
		# to run qsub immediately, use this
		#commandexe = "echo \"%s \" | qsub -cwd -V -l vf=20G,excl=true -N %s -o %s -j Y " % (cmd, "tophat", "run" + self.barcode + ".log")
		#print commandexe
		#subprocess.Popen(commandexe, shell=True)

		# else return command line
		return cmd


#z = StarAligner()
#z.setGenomeDir("/home/rwang/scratch1/rnaseq/star_res/hg19")
#z.setFastaFiles("/home/rwang/scratch1/rnaseq/datasets/bodymap2/00-raw/ERR030872_1.fastq", "/home/rwang/scratch1/rnaseq/datasets/bodymap2/00-raw/ERR030872_2.fastq")
#cmd = z.makeCommand()
#print cmd
#
#qsub = SGE()
#kw={'command':cmd, 'jobname':"STAR", 'jobmem':"1G"}
#qsub.createJobScript("test.sh", **kw)
##qsub.createJobScript("test.sh", 'command':cmd, 'jobname':"STAR", 'jobmem':"1G"})
