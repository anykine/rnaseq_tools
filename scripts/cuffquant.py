#cuffquant
class CuffQuant(object):
	def __init__(self, annotationFile=None, bamfile=None, genomeFile=None, outputDir="./"):
		self.exe = '/share/apps/cufflinks-2.2.1.Linux_x86_64/cuffquant' 
		self.annotationFile = annotationFile
		self.bamFile = bamfile
		self.genomeFile = genomeFile
		self.outputDir = outputDir
		self.threads = 8

	def makeCommand(self):
		arglist = [ "%s" % self.exe ]
		arglist.extend([ "-p %s " % self.threads ])
		arglist.extend([ "-o %s " % self.outputDir  ])
		if self.genomeFile is not None:
			# bias correction
			arglist.extend([ "-b %s " % self.genomeFile ])
		# rescue multireads
		arglist.extend([ "-u " ])
		# GTF file
		arglist.extend([ "%s" % self.annotationFile])
		arglist.extend([ "%s" % self.bamFile])

		cmd = " ".join(arglist)
		return cmd
