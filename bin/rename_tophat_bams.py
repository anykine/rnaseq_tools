# rename the tophat bam file which
# is always 'accepted_hits.bam' to match
# the config file so that it is :
#    sample_transcriptome.bam OR sample_427m

import os, sys
import json
import argparse
import shutil

def renameTophatBamToSample(samples, basedir, reference):
	for samp in samples:
		if reference in ("hg19", "mm9"):
			bamfile = os.path.join(basedir, samp, "03-align", "accepted_hits.bam")
			newbamfile=os.path.join(basedir, samp, "03-align", samp + "_transcriptome.bam")
		elif reference in ("dmd427m"):
			bamfile = os.path.join(basedir, samp, "03-alignDMD", "accepted_hits.bam")
			newbamfile=os.path.join(basedir, samp, "03-alignDMD", samp + "_427m.bam")
		else:
			print "Bam file doesn't exist or reference not specified"
	
		if os.path.isfile(bamfile) and not os.path.isfile(newbamfile):
			print "renaming " + str(bamfile) + " to " + str(newbamfile)
			shutil.move(bamfile, newbamfile)

if __name__=="__main__":
			
	parser = argparse.ArgumentParser()
	parser.add_argument("configfile", help="config file with options: eg config_tophat2.json")
	args = parser.parse_args()

	config = json.loads(open(args.configfile).read())
	print config['samples']
	renameTophatBamToSample(config['samples'], config['basedir'], config['reference'])

