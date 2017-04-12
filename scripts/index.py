#!/bin/env python

class Index(object):
	"""create reference genome sequence index object"""

	def __init__(self, version, program):
		self.version = version  #hg19, mm9
		self.program = program  #tophat2, start

	def output(self):
		if self.version == "hg19" and self.program=="tophat2":
			"""uses igenomes ensembl Grch37"""
			bowtie2Index = "/home/rwang/indexes/hg19/igenomes/Homo_sapiens/Ensembl/GRCh37/Sequence/Bowtie2Index/genome"
			prebuiltIndex = "/scratch1/tmp/rwang/rnaseq/tophat_prebuilt_index/hg19/ensembl/ensembl"
			return (bowtie2Index, prebuiltIndex)

		elif self.version == "dmd427m" and self.program=="tophat2":
			bowtie2Index = "/home/rwang/indexes/dmd_transcript/dmd"
			return(bowtie2Index, None)

		elif self.version == "dmdgenomic" and self.program=="tophat2":
			bowtie2Index = '/home/rwang/indexes/dmd_genomic/dmd_genomic_hg19'
			return(bowtie2Index, None)

		elif self.version == "mm9" and self.program=="tophat2":
			bowtie2Index = "/scratch1/tmp/rwang/indexes/Mus_Musculus/Ensembl/NCBIM37/Sequence/Bowtie2Index/genome"
			prebuiltIndex = "/scratch1/tmp/rwang/rnaseq/tophat_prebuilt_index/mouse/tx"
			return(bowtie2Index, prebuiltIndex)

		elif self.version =="dmd427m_mm9" and self.program=="tophat2":
			bowtie2Index = "/home/rwang/indexes/dmd_transcript/mouse/dmd_transcript_427m_mm9"
			#prebuiltIndex = "/scratch1/tmp/rwang/rnaseq/tophat_prebuilt_index/mouse/tx"
			return(bowtie2Index, None)

		elif self.version == "ensembl_hg19" and self.program=="STAR":
			STARIndex = "/home/rwang/scratch1/rnaseq/star_res/hg19"
			return(STARIndex)

		elif self.version == "ensembl_mm9" and self.program=="STAR":
			STARIndex = "/home/rwang/scratch1/rnaseq/star_res/ensembl_mm9"
			return(STARIndex)

		elif self.version == "ensembl_mm9" and self.program=="subjunc":
			index = "/home/rwang/indexes/mm9/subjunc/ensembl_mm9"
			return(index)

		elif self.version == "ensembl_hg19" and self.program=="subjunc":
			index = "/home/rwang/indexes/hg19/subjunc/ensembl_hg19"
			return(index)

		else:
			return None

