# RNA-Seq tools

A collection of scripts to generate bash scripts on an SGE cluster for the following tools:

* STAR
* kallisto
* Tophat2
* Cufflinks/Cuffquant
* featureCount (subread)
* salmon
* SpliceTrap
* indexes (aligner index files)


## Code

  + scripts/ - python classes that wrap RNA-Seq tools/programs
  + bin/ - scripts that use python classes to create qsub scripts
  + templates/ - mako template for the qsub script

## Dependencies

  + Python 2
  + mako template class
  + Sun Grid Engine

## Data organization

I assume the raw data (paired end FASTQs) has this layout:

```
runDirectory
|
|
└───sampleA
│   │
│   └───00-raw
│       │   sampleA_1.fastq.gz
│       │   sampleA_2.fastq.gz
│   
└───sampleB
│   │
│   └───00-raw
│       │   sampleB_1.fastq.gz
│       │   sampleB_2.fastq.gz
    
```

The data for each tool (STAR, kallisto, ...) will be output in its own subdirectory (eg 03-alignSTAR).

All rnaseq runs are assumed to be demultiplexed.


## Config

appconfig.json - specify the path to the various software
siteconfig.json - specify the base path for apps and indexes

## Usage

To run a tool such as the STAR aligner, we create a JSON file in the run directory.

```
# config_STAR.json
{
"samples": [ "sampleA", "sampleB"],
"basedir": "/data/ranseq/run1/",
"reference": "ensembl_hg19",
"date": "2019-03-31"
}

```

To generate the scripts:
```
python make_STAR.py config_STAR.json
```

which will create files:
```
sampleA/sampleA_STAR_ensembl_hg19.sh
sampleB/sampleB_STAR_ensembl_hg19.sh

```

We can qsub all the files like this (from the run directory) `find -type f -name *STAR*.sh -exec qsub {} \;`

