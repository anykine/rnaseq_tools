#!/bin/env python

import os
import sys
sys.path.append("/home/rtwang/rtwcode/rnaseq_tools/scripts")
from siteconfig import SiteconfigBase

class Gtf(SiteconfigBase):
    """This provides the GTF filer for featureCounts , etc.

       A basepath is defined for ease of migration if that becomes necessary.


    """

    def __init__(self, version, provider, species):
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

        self.version = version  #hg19, mm9, GRCh38
        self.gtfProvider = provider #ucsc, ensembl
        self.species = species # human, mouse
        #self.basepath = "/home/rtwang/projects/indexes"

    def output(self):
        """
        Provides the GTF file(s) required by an aligner
        """
        #
        # Ensembl 
        #
        if self.gtfProvider == "ensembl" and self.version=="GRCh37" and self.species == "human":
            # uses igenomes ensembl Grch37
            gtf = os.path.join(self.gtfBasePath,
                    "hg19/igenomes/Homo_sapiens/Ensembl/GRCh37/Annotation/Genes/genes.gtf")
            return (gtf)

        elif self.gtfProvider == "ncbi" and self.version=="build37.2" and self.species == "human":
            # uses igenomes NCBI 37.2
            gtf = os.path.join(self.gtfBasePath,
                    "hg19/igenomes/Homo_sapiens/NCBI/build37.2/Annotation/Genes/genes.gtf")
            return (gtf)

        elif self.gtfProvider == "ucsc" and self.version == "hg19" and self.species=="human":
            index = os.path.join(self.indexBasePath,
                    "hg19/igenomes/Homo_sapiens/UCSC/hg19/Annotation/Genes/genes.gtf")
            return(gtf)
        else:
            return None

