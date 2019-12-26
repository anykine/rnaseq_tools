#!/bin/env python

import os
import sys
import subprocess
from siteconfig import Appconfig
import json

# This use of featureCount is set for counting reads in EXONS only!

# using info from biostars https://www.biostars.org/p/150037/

# -t exon  sets coord range (is your read in this range?)
# -g exon_id sets the bins (eg bin my reads by exon)
# -s 1 strand specific counting
# -f count at feature level (exon)
# -O assign reads to their overlapping meta-features (or features of -f specified)
# --primary  count primary alignemnts only (specified in SAM flag)
# --ignoreDup ignore duplicates flagged in SAM (controversial whehter we should do this)
# -p count fragments instead of reads
# -R use this for debugging

# this should count overlap exons, assign all exons
# /share/apps/richard/subread-1.5.0-p1-Linux-x86_64/bin/featureCounts -T 5  \
# -a /home/rwang/indexes/hg19/igenomes/Homo_sapiens/Ensembl/GRCh37/Annotation/Genes/genes.gtf  \
# -t exon  -g exon_id  \
# -f  \
# -O \
# -o /home/rwang/scratch1/rnaseq/datasets/bodymap2/ERR030887/05-featureCount1/ERR030887_featureCount.txt  \
# /home/rwang/scratch1/rnaseq/datasets/bodymap2/ERR030887/03-star/ERR030887Aligned.sortedByCoord.out.bam  

class FeatureCount (Appconfig):
    """Wrapper around featurecount (subread)"""
    def __init__(self, gtf, nameOfJob, bamfile, outputDir ):
        """
        Constructor

         gtf (str): GTF annotation file
         nameOfJob (str): job name
         bamfile (str): name of aligned BAM file
         outputDir (str): path to output dir

        This code looks at exons, so both featureTYpe and
        and attributeType are exon/exon_id
        """

        Appconfig.__init__(self, "featureCounts")
        #self.exe = "/share/apps/richard/subread-1.5.0-p1-Linux-x86_64/bin/featureCounts"
        # specify the bowtie2 index file (reference genome index base)
        self.annotation = gtf
        self.name = nameOfJob 
        self.threads = 5
        self.featureType = "exon"
        self.attributeType = "exon_id"

        self.bamfile = bamfile

        self.outputDir = outputDir

    def makeCommand(self):
        """generate commandline"""
        arglist = ["%s" % self.exe ]
        arglist.extend([ "-T %s " % self.threads])
        arglist.extend([ "-a %s " % self.annotation])
        arglist.extend([ "-t %s " % self.featureType])  # count by exon
        arglist.extend([ "-g %s " % self.attributeType]) # use exon_id 
        arglist.extend([ "-f " ])  # count readsat the feature level (ie exon)
        arglist.extend([ "-p " ])  # count fragments instead of reads

        #arglist.extend([ "-R " ])
        arglist.extend([ "-O  " ]) # count all overlapping features of a read
        #arglist.extend([ "-M  " ])   # multimapping
        arglist.extend([ "-o %s " % os.path.join(self.outputDir, self.name+"_featureCount.txt")  ])
        arglist.extend([ "%s " % self.bamfile])


        cmd =  " ".join(arglist)


        # else return command line
        return cmd

