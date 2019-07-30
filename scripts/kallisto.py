#!/bin/env python

import os
import sys
import subprocess
from siteconfig import Appconfig
import json

class KallistoAligner(Appconfig):
    """
    Wrapper around Kallisto aligner
    """
    def __init__(self, transcriptIndex, nameOfJob, reads1, reads2, outputDir, 
            bootstrapSamples=False,
            command="quant"):
        """
        Constructor
         transcriptIndex (obj): reference index
         nameOfJob (str):  qsub job name
         reads1 (array): fastq read1 array
         reads2 (array): fastq read2 array
         outputDir (str): path to output folder

         This aligner is derived from Appconfig
        """
        Appconfig.__init__(self, "kallisto")
        #self.exe = "/share/apps/richard/kallisto_linux-v0.42.5/kallisto"
        #self.exe = "/home/rtwang/bin/kallisto_linux-v0.44.0/kallisto"
        #self.exe = self.kallistoExe
        # specify the bowtie2 index file (reference genome index base)
        self.transcriptIndex = transcriptIndex 
        self.name = nameOfJob 
        self.threads = 8
        self.command = command
        self.bootstrapSamples = bootstrapSamples

        #reads1 is a list of 1st pair or SE reads, reads2 is list of 2nd pair
        #    if single end, pass empty list for read2 []    
        if len(reads2) > 0:
            self.paired = True
            self.reads1 = reads1
            self.reads2 = reads2
        else:
            self.paired = False
            self.reads1 = reads1

        self.outputDir = outputDir

    def makeCommand(self):
        """generate commandline"""
        arglist = ["%s" % self.exe ]
        arglist.extend([ "%s " % self.command ])
        arglist.extend([ "-i %s " % self.transcriptIndex])
        arglist.extend([ "-o %s " % self.outputDir  ])
        arglist.extend([ "-t %s " % self.threads ])

        if self.bootstrapSamples is not False:
            arglist.extend([ "-b %d " % self.bootstrapSamples ])

        if self.paired == False:
            arglist.extend([ " --single %s " % ",".join(self.reads1 ) ])
        else:
            arglist.extend([ "%s " % ",".join(self.reads1 ) ])
            arglist.extend([ "%s " % ",".join(self.reads2 ) ])

        cmd =  " ".join(arglist)

        #sys.stderr.write("LOG index: %s \n" % self.transcriptIndex)
        # else return command line
        return cmd

