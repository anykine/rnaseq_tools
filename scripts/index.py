#!/bin/env python

import os
import sys
sys.path.append("/home/rtwang/rtwcode/rnaseq_tools/scripts")
from siteconfig import SiteconfigBase

class Index(SiteconfigBase):
    """This provides the aligner reference file(s) for STAR, BWA, etc.

       Specify (a) the aligner and (b) the reference index version 
       (whole transcript/dmd 427m/etc) 

       A basepath is defined for ease of migration if that becomes necessary.


    """

    def __init__(self, version, program):
        """
        Constructor
         version (str): reference index version (hg19, ensembl)
         program (str): name of aligner

        Sets
          self.appBasePath: base dir for applications
          self.indexBasePath: base dir for indexes

        """
        # call superclass to get appBasePath and indexBasePath
        SiteconfigBase.__init__(self, "siteconfig.json")

        self.version = version  #hg19, mm9
        self.program = program  #tophat2, STAR
        #self.basepath = "/home/rtwang/projects/indexes"

    def output(self):
        """
        Provides the reference file(s) required by an aligner
        """
        #
        # hg19 transcriptome (ensembl, ucsc)
        #
        if self.version == "hg19" and self.program=="tophat2":
            # uses igenomes ensembl Grch37
            #bowtie2Index = "/home/rwang/indexes/hg19/igenomes/Homo_sapiens/Ensembl/GRCh37/Sequence/Bowtie2Index/genome"
            bowtie2Index = os.path.join(self.indexBasePath, "hg19/igenomes/Homo_sapiens/Ensembl/GRCh37/Sequence/Bowtie2Index/genome")
            prebuiltIndex = os.path.join(self.indexBasePath,
                    "/rnaseq/tophat_prebuilt_index/hg19/ensembl/ensembl")
            return (bowtie2Index, prebuiltIndex)

        elif self.version == "ensembl_hg19" and self.program=="STAR":
            #STARIndex = "/home/rwang/scratch1/rnaseq/star_res/hg19"
            STARIndex = os.path.join(self.indexBasePath, "star_res/hg19")
            #STARIndex = "/home/rtwang/projects/indexes/STAR/ENSEMBL.homo_sapiens.release-83"
            return(STARIndex)

        elif self.version == "pacbiominfl10hg19" and self.program=="STAR":
            STARIndex = os.path.join(self.indexBasePath, "star_res/pacbio/index/minfl10hg19")
            return(STARIndex)

        elif self.version == "ensembl37" and self.program=="bwa":
            index = os.path.join(self.indexBasePath,
                    "/hg19/igenomes/Homo_sapiens/Ensembl/GRCh37/Sequence/BWAIndex/genome.fa")
            return(index)

        elif self.version == "ensembl_hg19" and self.program=="subjunc":
            index = os.path.join(self.indexBasePath,
                    "/hg19/subjunc/ensembl_hg19")
            return(index)

        elif self.version == "ensembl_GRCh37" and self.program=="kallisto":
            index = os.path.join(self.indexBasePath, "hg19/kallisto/ensembl_GRCh37_transcripts_index")
            return(index)
        #
        # DMD 427m transcript only
        #
        elif self.version == "dmd427m" and self.program=="tophat2":
            bowtie2Index = "/home/rwang/indexes/dmd_transcript/dmd"
            return(bowtie2Index, None)
        #
        # DMD geme only (hg19)
        #
        elif self.version == "dmdgenomic" and self.program=="tophat2":
            bowtie2Index = '/home/rwang/indexes/dmd_genomic/dmd_genomic_hg19'
            return(bowtie2Index, None)

        elif self.version == "ensembl_mm9" and self.program=="STAR":
            STARIndex = "/home/rwang/scratch1/rnaseq/star_res/ensembl_mm9"
            return(STARIndex)

        elif self.version == "ensembl_mm9" and self.program=="subjunc":
            index = "/home/rwang/indexes/mm9/subjunc/ensembl_mm9"
            return(index)
        #
        # Mouse mm9 transcriptome
        #
        elif self.version == "mm9" and self.program=="tophat2":
            bowtie2Index = "/scratch1/tmp/rwang/indexes/Mus_Musculus/Ensembl/NCBIM37/Sequence/Bowtie2Index/genome"
            prebuiltIndex = "/scratch1/tmp/rwang/rnaseq/tophat_prebuilt_index/mouse/tx"
            return(bowtie2Index, prebuiltIndex)

        #
        # Mouse 427m transcript only
        #
        elif self.version =="dmd427m_mm9" and self.program=="tophat2":
            bowtie2Index = "/home/rwang/indexes/dmd_transcript/mouse/dmd_transcript_427m_mm9"
            #prebuiltIndex = "/scratch1/tmp/rwang/rnaseq/tophat_prebuilt_index/mouse/tx"
            return(bowtie2Index, None)


        else:
            return None

