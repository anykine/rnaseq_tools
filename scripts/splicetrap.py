import os,sys

# splicetrap
# bowtie must be on path
# R must be on path
class SpliceTrap(object):
	def __init__(self, readsize, cutoff, prefix, outdir, numThreads, reads1, reads2, nameOfJob, database='hg19'):
		self.exe = '/share/apps/richard/SpliceTrap.0.90.5/SpliceTrap'
		self.mapper = 'bowtie'
		self.database = database
		self.readsize = readsize
		self.cutoff = cutoff
		self.outputFilePrefix = prefix
		self.outdir = outdir
		self.bowtieThreads = numThreads
		self.name = nameOfJob

		self.reads1 = reads1
		self.reads2 = reads2

	def makeCommand(self):
		arglist = [ "%s" % self.exe ]
		arglist.extend([ "-m %s " % self.mapper])
		arglist.extend([ "-d %s " % self.database])
		arglist.extend([ "-s %s " % self.readsize])

		arglist.extend([ "-1 %s " % self.reads1])
		arglist.extend([ "-2 %s " % self.reads2])
		arglist.extend([ "-c %s " % self.cutoff])

		arglist.extend([ "-o %s " % self.outputFilePrefix ])
		arglist.extend([ "-outdir %s " % self.outdir])

		cmd = " ".join(arglist)
		return cmd
