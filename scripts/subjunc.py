import os,sys

# subjunc
class SubjuncAligner(object):
	def __init__(self, genomeIndexFile, reads1, reads2, outputFile, nameOfJob, phreadFormat=6 ):
		self.exe = '/share/apps/richard/subread-1.5.0-p1-Linux-x86_64/bin/subjunc'
		self.threads = 4
		self.phreadFormat = phreadFormat
		self.genomeIndexFile = genomeIndexFile
		self.outputFile = outputFile
		self.name = nameOfJob

		#reads1 is a list of 1st pair or SE reads, reads2 is list of 2nd pair
		#	if single end, pass empty list for read2 []	
		if len(reads2) > 0:
			self.paired = True
			self.reads1 = reads1
			self.reads2 = reads2
		else:
			self.paired = False
			self.reads1 = reads1

	def makeCommand(self):
		arglist = [ "%s" % self.exe ]
		arglist.extend([ "-P %s " % self.phreadFormat ])
		arglist.extend([ "-T %s " % self.threads ])
		arglist.extend([ "-i %s " % self.genomeIndexFile ])

		if self.paired == True:
			arglist.extend([ "-r %s " % ",".join(self.reads1)])
			arglist.extend([ "-R %s " % ",".join(self.reads2)])
		else :
			arglist.extend([ "-r %s " % ",".join(self.reads1)])

		arglist.extend([ "-o %s " % self.outputFile ])

		cmd = " ".join(arglist)
		return cmd
