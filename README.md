# Python scripts to generate run files for RNA-seq

A collection of script genereators for various rnaseq tools

scripts/ - python classes that wrap RNAseq tools/programs
bin/ - scripts that use python classes to create qsub scripts
templates/ - mako template for the qsub script

So far, I have classes that will handle these aligners

* Tophat2
* Cufflinks/Cuffquant
* featureCount (subread)
* kallisto
* salmon
* STAR
* SpliceTrap
* indexes (aligner index files)


