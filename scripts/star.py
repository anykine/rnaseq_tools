#!/bin/env python

import os
import sys
import subprocess
from siteconfig import Appconfig

class STARAligner(Appconfig):
    """
    Wrapper around STAR RNAseq aligner. It will generate the qsub run script.

    This assumes that FASTQs are gzipped.

    2pass mode not currently implemented. Needs to build genome index at
    runtime.
    """
    def __init__(self, **kwargs):
        """
        Defaults are preassigned. Other options can be assigned in the
        config.json file provided to make_STAR.py and will be overriden.

        Args:
            indexPath (str): path to index
            reads (tuple): (/path/file_1.gz, /path/file_2.gz)
            outPrefix (str): output prefix
            bamout (bool): 
            threads (int): number of threads to use
            mem (int): RAM
            twopass (bool): run STAR in 2pass mode
            unmapped (str): None, Within (adds unmapped to BAM), File (creates Unmapped.out.mate1/2)
            genomeLoad (str):  LoadAndKeep, LoadAndRemove, LoadAndExit, NoSharedMemory 
        """
        Appconfig.__init__(self, "STAR")

        # Default values for these fields
        self.twopass = False
        self.memory= '60G'
        self.bamout = True
        self.threads = 8
        self.unmapped = None
        self.genomeDir = None
        self.outFileNamePrefix = None
        self.limitBAMsortRAM = 10737412742
        self.genomeLoad = 'LoadAndKeep'

        # reads is a tuple of 2 PE reads or 1 SE read
        self.reads = (None, None)

        # get predefined values from __dict__
        allowed_keys = list(self.__dict__.keys())

        #update using kwargs only for allowed keys
        #these are passed from make_STAR.py and controlled by the config.json
        #file
        self.__dict__.update((key, value) for key, value in kwargs.items() if
                key in allowed_keys)

        # output rejected keys
        rejected_keys = set(kwargs.keys()) - set(allowed_keys)
        if rejected_keys:
            print "these keys not updated %s" %  ",".join(rejected_keys)
            #raise ValueError("Invalid arguments provided to constructor %s" %
            #        rejected_keys)

    def makeCommand(self):
        """generate STAR commandline"""
        arglist = ["%s" % self.exe ]
        arglist.extend([ "--runThreadN %s" % self.threads ])
        arglist.extend([ "--genomeDir %s" % self.genomeDir ])
        if len(self.reads) == 2:
            arglist.extend([ "--readFilesIn %s %s " % (self.reads[0], self.reads[1]) ])
        else:
            arglist.extend([ "--readFilesIn %s " % self.reads[0] ])

        arglist.extend([ "--outSAMtype BAM SortedByCoordinate" ])
        arglist.extend([ "--outFileNamePrefix %s" % self.outFileNamePrefix ])

        # optimization keep genome in shared memory to prevent reloading between runs
        # msut set RAM lmit for sorting, eg 10Gb
        arglist.extend([ "--genomeLoad %s" % self.genomeLoad ])
        arglist.extend([ "--limitBAMsortRAM %s" % self.limitBAMsortRAM ])

        if self.unmapped == "Within":
            arglist.extend([ "--outSAMunmapped %s" % self.unmapped ])
        elif self.unmapped == "Fastx":
            arglist.extend([ "--outReadsUnmapped Fastx"])
        else:
            arglist.extend([ "--outReadsUnmapped None" ])

        # test if reads are gzipped, add this
        if os.path.splitext(self.reads[0])[1] ==".gz":
            arglist.extend([ "--readFilesCommand zcat "])

        if self.twopass == True:
            arglist.extend([ "--twopassMode Basic "])
        else:
            arglist.extend([ "--twopassMode None "])

        cmd =  " ".join(arglist)

        return cmd


class STARIndexCreator(Appconfig):
    """
    Wrapper around  STAR index creator code 
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


