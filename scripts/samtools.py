#!/bin/env python

import os
import sys
import subprocess

# only handles index
class Samtools(object):
	"""Wrapper around Samtool"""
	def __init__(self, cmd, bamfilePath, mem='4G'):
		self.cmd = cmd
		self.bamfilePath = bamfilePath
		self.exe = "/share/apps/samtools-current/samtools"

	def makeCommand(self):
		
		arglist = ["%s" % self.exe ]
		arglist.extend([ "%s" % self.cmd ])

		if self.cmd == "index":
			arglist.extend([ "%s" % self.bamfilePath ])

		cmd =  " ".join(arglist)

		return cmd


