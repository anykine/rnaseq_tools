#!/bin/env python

import os
import sys
import subprocess

class KallistoAligner(object):
	"""Wrapper around Kallisto aligner"""
	def __init__(self, transcriptIndex, nameOfJob, reads1, reads2, outputDir, command="quant"):
		self.exe = "/share/apps/richard/kallisto_linux-v0.42.5/kallisto"
		# specify the bowtie2 index file (reference genome index base)
		self.transcriptIndex = transcriptIndex 
		self.name = nameOfJob 
		self.threads = 8
		self.command = command

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
		arglist.extend([ "-o %s " % self.outputDir  ])
		arglist.extend([ "-t %s " % self.threads ])
		arglist.extend([ "-b 100 " ])

		if self.paired == False:
			arglist.extend([ " --single %s " % ",".join(self.reads1 ) ])
		else:
			arglist.extend([ "%s " % ",".join(self.reads1 ) ])
			arglist.extend([ "%s " % ",".join(self.reads2 ) ])

		cmd =  " ".join(arglist)


		# else return command line
		return cmd

