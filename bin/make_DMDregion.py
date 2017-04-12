#!/bin/env python

import os, sys
import glob
sys.path.append('/home/rwang/rtwcode/rnaseq_tools/scripts/')
from dmdregion import *
from sge import *

files = glob.glob("*.bam")
print files

names = [ n.split(".")[0] for n in files ]

for i in xrange(len(files)):
	obj = DMDregion(files[i], name=names[i], format="ensembl")
	cmdtxt = obj.makeCommand()
	print cmdtxt

	qsub = SGE(names[i], "/home/rwang/rtwcode/rnaseq_tools/templates/qsub_tophat.tmpl")
	args = {'command':cmdtxt, 'jobname': names[i], 'jobmem':'1G', 'logfilename': "_".join([ str(names[i]), "DMDextract.log"])}
	outscript = str(names[i]) + "_DMDextract.sh"
	qsub.createJobScript(outscript, **args)
