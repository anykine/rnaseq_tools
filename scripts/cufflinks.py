#cufflinks
class Cufflinks(object):
	def __init__(self, annotationFile=None, bamfile=None, outputDir="./", genomeFile=None):
		self.exe = '/share/apps/cufflinks-2.2.1.Linux_x86_64/cufflinks' 
		self.annotationFile = annotationFile
		self.bamFile = bamfile
		self.genomeFile = genomeFile
		self.outputDir = outputDir
		self.threads = 8

	def makeCommand(self):
		arglist = [ "%s" % self.exe ]
		arglist.extend([ "-u " ])
		arglist.extend([ "-g %s " % self.annotationFile ])
		if self.genomeFile is not None:
			arglist.extend([ "-b %s " % self.genomeFile])
		arglist.extend([ "-o %s " % self.outputDir ])
		arglist.extend([ "-p 8 "])
		arglist.extend([ "%s" % self.bamFile])

		cmd = " ".join(arglist)
		return cmd
