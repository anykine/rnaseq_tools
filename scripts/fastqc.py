#!/bin/env python

import os
import sys

class FastQC(object):
	"""Wrapper around FastQC"""
	def __init__(self, outdir, fileList, extract=False):
		self.threads = 8 
		self.exe = "/share/apps/richard/FastQC-current/fastqc"
		self.outdir = outdir
		self.fileList = fileList
		self.extract = extract
	
	def makeCommand(self):
		arglist = ["%s" % self.exe ]
		arglist.extend([ "--outdir %s" % self.outdir ])
		if self.extract == False:
			arglist.extend([ "--noextract"])
		#arglist.extend([ " ".join(self.fileList) ])
		arglist.extend([ self.fileList ])

		cmd = " ".join(arglist)
		return cmd
