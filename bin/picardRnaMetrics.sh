PICARD=/share/apps/richard/picard-tools-1.131/picard.jar
CMD=CollectRnaSeqMetrics

#GENEANNOT=/home/rwang/annot/hg19/knownGene.txt
REFFLAT=/home/rwang/indexes/hg19/refFlat/refFlat_ensembl.txt
RIBOSOMAL_INTERVALS=/home/rwang/indexes/hg19/rRNA/new/rRNA_ensembl_intervalList_header.txt

if [ "$#" -ne 2 ]; then
	echo "change to sample/04-qc directory and then run"
	echo "Usage $0 PATH_TO_BAMFILE OUTDIR"
	exit
fi
#INPUT=/scratch1/tmp/rwang/5017seq/
# input bam file
INPUT=$1
# outdir
OUTDIR=$2
OUTFILE=`/bin/basename $INPUT`
OUTFILE="${OUTFILE%.bam}_RNAmetrics.txt"
OUTPDF="${OUTFILE%.bam}_RNAmetrics.pdf"

OUTPUT=/scratch1/tmp/rwang/5017seq/04-qc/picard/$OUTFILE.txt
CHART_OUTPUT=/scratch1/tmp/rwang/5017seq/04-qc/picard/$OUTFILE.pdf

echo "java -jar $PICARD $CMD INPUT=$INPUT OUTPUT=$OUTDIR/$OUTFILE \
REF_FLAT=$REFFLAT \
RIBOSOMAL_INTERVALS=$RIBOSOMAL_INTERVALS \
STRAND_SPECIFICITY=FIRST_READ_TRANSCRIPTION_STRAND \
CHART_OUTPUT=$OUTDIR/$OUTPDF " \
 | qsub -cwd -V -o $OUTFILE.log -j Y -N $OUTFILE

#bam=/scratch0/tmp/rwang/gm5017/samp1/out1/accepted_hits.bam
#java -jar ${picarddir}CollectAlignmentSummaryMetrics.jar INPUT=$bam OUTPUT=samp1out1.metrics.txt
#echo "java -jar ${picarddir}CollectRnaSeqMetrics.jar INPUT=$bam OUTPUT=samp1out1.metrics.txt \
#REF_FLAT=refFlathg19.txt RIBOSOMAL_INTERVALS=/home/rwang/annot/human_grch37p3_rRNA_intervalList_header.txt \
# STRAND_SPECIFICITY=NONE" \
# | qsub -cwd -V -o log.err -j Y
