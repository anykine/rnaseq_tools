#!/bin/env python

import os
import sys
import subprocess
import re

class BWA(object):
	"""Wrapper around BWA aligner"""
	def __init__(self, indexPath, nameOfJob, reads1, reads2, outputSAM, mode="mem", bamout=True):
		self.threads = 8
		self.exe = "/home/rtwang/nelsonlabshare/share/apps/bwa-0.7.17/bwa"
		# specify the bowtie2 index file (reference genome index base)
		self.index = indexPath
		self.name = nameOfJob 
		self.threads = 8
		self.mode = mode  # bwa mem (70bp-1M), bwasw (orig), bwasase/aln/sampe (backtrack)
		self.bamout = bamout

		#reads1 is a list of 1st pair or SE reads, reads2 is list of 2nd pair
		#	if single end, pass empty list for read2 []	
		if len(reads2) > 0:
			self.paired = True
			self.reads1 = reads1
			self.reads2 = reads2
		else:
			self.paired = False
			self.reads1 = reads1

		self.outputSAM = outputSAM

	def makeCommand(self):
		"""generate commandline"""
		arglist = ["%s" % self.exe ]
		arglist.extend([ "%s " % self.mode ])
		arglist.extend([ "-t %s " % self.threads ])

		arglist.extend([ "%s" % self.index])
		arglist.extend([ "%s " % ",".join(self.reads1 ) ])

		if self.paired == True:
			arglist.extend([ "%s " % ",".join(self.reads2 ) ])


		# this will output either SAM file or
		# a sorted BAM file
		if self.bamout == True:
			# replace .sam with .bam
			outputBAM = re.sub(r"\.sam", r".sorted.bam", self.outputSAM)
			#arglist.extend([ " | samtools view -bS - > %s" % outputBAM])

			# Samtools ver 1.9 (htlib) syntax for sorting
			arglist.extend([ "| /labshares/nelsonlab1/share/apps/bin/bin/samtools sort -@8 -o %s -" % 
				outputBAM ])
		else:
			# output SAM file
			arglist.extend([ " >  %s " % self.outputSAM  ])

		# output a COMPLETE file
		basepath = os.path.dirname(self.outputSAM)

		cmd =  " ".join(arglist)
		cmd += "\n touch " + basepath + "/COMPLETE"

		return cmd

