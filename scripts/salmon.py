#!/bin/env python

import os
import sys
import subprocess

class SalmonAligner(object):
	"""Wrapper around Salmon aligner"""
	def __init__(self, transcriptIndex, nameOfJob, reads1, reads2, outputDir, libType, command="quant"):
		self.exe = "/share/apps/richard/Salmon/SalmonBeta-0.6.1_DebianSqueeze/bin/salmon"
		# specify the bowtie2 index file (reference genome index base)
		self.transcriptIndex = transcriptIndex 
		self.name = nameOfJob 
		self.command = command
		self.libType = libType

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
		arglist.extend([ "%s " % self.command ])
		arglist.extend([ "-i %s " % self.transcriptIndex])
		arglist.extend([ "-l %s " % self.libType])

		if self.paired == False:
			arglist.extend([ " -r %s " % ",".join(self.reads1 ) ])
		else:
			# salmon can't handle gzipped files directly, so use process substitution
			arglist.extend([ "-1 %s " % "<(zcat " + ",".join(self.reads1 ) + ") " ])
			arglist.extend([ "-2 %s " % "<(zcat " + ",".join(self.reads2 ) + ") " ])

		arglist.extend([ "-o %s " % self.outputDir  ])
		cmd =  " ".join(arglist)


		# else return command line
		return cmd

