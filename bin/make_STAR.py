#!/bin/env python

import os, sys
import json
import argparse
sys.path.append("/home/rtwang/rtwcode/rnaseq_tools/scripts")
from star import *
from index import *
from sge import *

# Call variants from RNAseq using STAR aligner
# this is broad/gatk recommended workflow

def makeSTARScripts(**config):
    """
    Generate the STAR aligner qsub scripts. At a minimum, config (**kwargs) 
    is a dictionary that has these defined: 
        basedir
        samples(list)
        reference 
    """

    # assume genome index file already exists 
    STARIndex = Index(config["reference"], "STAR")
    index = STARIndex.output()
    # add reference genome to the config dictionary
    config["genomeDir"] = index

    for samp in config["samples"]:
        # add to the dictionary
        config["reads"] = (os.path.join(config["basedir"], samp, "00-raw",
            samp+"_1.fastq.gz"), os.path.join(config["basedir"], samp,
                "00-raw", samp+"_2.fastq.gz"))

        outputdir = os.path.join(config["basedir"], samp,
                "03-alignSTAR"+config["reference"] )

        if not os.path.exists(outputdir):
            os.makedirs(outputdir)

        config["outFileNamePrefix"] = os.path.join(outputdir, samp)

        # lowered the number of threads from 24 to 8 to prevent "cannot create output file,
        # check ulimit ERROR

        sa = STARAligner(**config)
        cmdtxt = sa.makeCommand()

        # Fill in the qsub template
        qsub = SGE(samp, "/home/rtwang/rtwcode/rnaseq_tools/templates/qsub.tmpl")
        args = {'command':cmdtxt, 
                'jobname': str(samp)+str(config["reference"]),
                'jobmem': sa.memory, 
                'logfilename': "_".join([str(samp), "STAR",
                str(config["reference"])+".log"])}

        outscript = os.path.join(config["basedir"],  
                samp, 
                str(samp) + "_STAR_" + str(config["reference"]) + ".sh")
        print outscript
        qsub.createJobScript(outscript, **args)


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("configfile", help="config file with options: eg config_STAR.json")
    args = parser.parse_args()

    config = json.loads(open(args.configfile).read())
    #makeSTARScripts(config['basedir'], config['samples'], config['reference'])
    makeSTARScripts( **config)
