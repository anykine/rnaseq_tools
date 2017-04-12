#!/bin/env python

import os
import sys
from mako.template import Template

class SGE(object):
	"""wrapper around SGE"""

	def __init__(self, nameOfJob, template):
		self.name = nameOfJob
		#self.template = "/home/rwang/rtwcode/rnaseq_tools/tophat_pipe/qsub_tophat.tmpl"
		self.template = template

	def createJobScript(self, outfile, **kw):
		"""uses mako templates; fill out template to generate bash file for qsub submission
		 Required fields: command, jobname, jobmem, logfilename
		 these two are equivalent
			kw={'command':cmd, 'jobname':"STAR", 'jobmem':"1G", 'logfilename':"log.log"}
			qsub.createJobScript("example.sh", **kw)

			qsub.createJobScript("example.sh", command=cmd, jobname="STAR", jobmem="100G", logfilename="log.log")
		"""	

		templ = Template(filename=self.template)
		res = templ.render(**kw)
		outfile = open(outfile, "w")
		outfile.write(res)
		outfile.close()

		#print res
		
#qsub = SGE()
#kw={'command':cmd, 'jobname':"STAR", 'jobmem':"1G"}
#qsub.createJobScript("test.sh", **kw)
##qsub.createJobScript("test.sh", 'command':cmd, 'jobname':"STAR", 'jobmem':"1G"})
