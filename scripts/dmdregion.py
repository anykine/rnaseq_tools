#!/bin/env python

import os
import sys
import subprocess

class DMDregion(object):
	"""Wrapper around Tophat aligner"""
	def __init__(self, bamfile, name="job1", format="ucsc", build="hg19"):
		self.exe = 'samtools view -b'
		self.bamfile = bamfile
		self.name = name
		self.build = build
		self.dmdregion = self.getCoords(format, build)
		self.outfilesuffix = "DMDonly.bam"

	def getCoords(self, format, build):
		if build=="hg19":
			self.coordinates = '31137345-33229673'
		elif build=="mm9":
			self.coordinates = '80194209-82450389'

		if format=="ucsc":
			self.chrom = "chrX"
		elif format=="ensembl":
			self.chrom = "X"

		return( ":".join([self.chrom, self.coordinates]))
			

	def makeCommand(self):
		"""generate commandline"""
		arglist = ["%s" % self.exe ]
		arglist.extend([ "%s " % self.bamfile])
		arglist.extend([ "%s " % self.dmdregion])
		arglist.extend([ "%s" % ">"])

		bamfilebase = os.path.splitext(self.bamfile)[0]
		arglist.extend([ "%s " % ".".join( [bamfilebase, self.outfilesuffix]) ])

		cmd =  " ".join(arglist)

		# else return command line
		return cmd

