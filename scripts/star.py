#!/bin/env python

import os
import sys
import subprocess
from siteconfig import Appconfig

class STARAligner(Appconfig):
    """
    Wrapper around STAR RNAseq aligner
    """
    def __init__(self, indexPath, reads1, reads2, outPrefix, bamout=True, threads=48, mem='100G', twopass=False,
            unmapped = False):
        """
        Args:
            indexPath (str): path to index
            reads1 (array): array of read1
            reads2 (array); array of read2
            outPrefix (str): output prefix
            bamout (bool): 
            threads (int): number of threads to use
            mem (int): RAM
            twopass (bool): run STAR in 2pass mode
            unmapped (str): what to do with unmapped reads
        """
        Appconfig.__init__(self, "STAR")
        self.twopass = twopass
        self.memory= mem
        self.bamout = bamout
        self.threads = threads
        self.unmapped = unmapped
        #self.exe = "/share/apps/richard/STAR_2.4.0j/bin/Linux_x86_64/STAR"
        # this version has a 2 pass mode
        #self.exe = "/share/apps/richard/STAR_2.5.3a/bin/Linux_x86_64/STAR"
        #self.exe = "/share/apps/star_2.5.0a/bin/STAR"
        self.genomeDir = indexPath
        self.outFileNamePrefix = outPrefix

        # reads1 is a list of 1st pair or SE reads, reads2 is list of 2nd pair
        # if single end, pass empty list for read2 []
        if len(reads2) > 0:
            self.paired = True
            self.reads1 = reads1
            self.reads2 = reads2
        else:
            self.paired = False
            self.reads1 = reads1

    def makeCommand(self):
        """generate STAR commandline"""
        arglist = ["%s" % self.exe ]
        arglist.extend([ "--runThreadN %s " % self.threads ])
        arglist.extend([ "--genomeDir %s" % self.genomeDir ])
        arglist.extend([ "--readFilesIn %s %s " % (self.reads1, self.reads2) ])
        arglist.extend([ "--outSAMtype BAM SortedByCoordinate" ])
        arglist.extend([ "--outFileNamePrefix %s" % self.outFileNamePrefix ])

        # optimization keep genome in shared memory to prevent reloading between runs
        # msut set RAM lmit for sorting, eg 10Gb
        arglist.extend([ "--genomeLoad LoadAndKeep "])
        arglist.extend([ "--limitBAMsortRAM 10737412742"])
        if self.unmapped == "Fastx":
            arglist.extend([ "--outReadsUnmapped %s" % self.unmapped ])

        # test if reads are gzipped, add this
        if os.path.splitext(self.reads1)[1] ==".gz":
            arglist.extend([ "--readFilesCommand zcat "])

        if self.twopass == True:
            arglist.extend([ "--twopassMode Basic "])
        else:
            arglist.extend([ "--twopassMode None "])

        cmd =  " ".join(arglist)

        return cmd


class STARIndexCreator(Appconfig):
    """
    Wrapper around  START index creator code 
    """
    def __init__(self, outputDir, inputFastaFile, threads=48, SJout=None, SJoverhang=None):
        """ gatk example uses SJoverhang 75 """
        Appconfig.__init__(self, "STAR")
        #self.exe = "/share/apps/richard/STAR_2.4.0j/bin/Linux_x86_64/STAR"
        #self.exe = "/share/apps/richard/STAR_2.5.3a/bin/Linux_x86_64/STAR"
        self.runMode = "genomeGenerate"
        self.genomeOutputDir = outputDir
        self.genomeFastaFiles = inputFastaFile
        self.threads = threads
        if SJout is not None:
            self.sjdbFileChrStartEnd = SJout
        if SJoverhang is not None:
            self.sjdbOverhang = 75
 
    def makeCommand(self):

        arglist = ["%s" % self.exe ]
        arglist.extend([ "--runMode %s" % self.runMode ])
        arglist.extend([ "--genomeDir %s" % self.genomeOutputDir ])
        arglist.extend([ "--genomeFastaFiles %s " % self.genomeFastaFiles ])
        if self.sjdbFileChrStartEnd is not None:
            arglist.extend([ "--sjdbFileChrStartEnd %s " % self.sjdbFileChrStartEnd])
            arglist.extend([ "--sjdbOverhang %s " % self.sjdbOverhang])
        arglist.extend([ "--runThreadN %s " % self.threads ])

        cmd =  " ".join(arglist)

        return cmd


