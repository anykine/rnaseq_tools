#!//usr/bin/perl -w
#
use strict;
use File::Find;

# NOTE about File::Find
#  it chdirs to the directory you specify unless you pass
#  a parameter to disable that

unless (@ARGV==1){
	print "$0 <directory> \n";
	print " eg $0 "." \n\n";
	print "Display number of reads and percent mapped for tophat runs\n";
	exit(1);
}

my @dirs = @ARGV;
#my @dirs = ( "./");
find(\&process_file, @dirs);

sub process_file{
		# dir
		#print $File::Find::dir, "\n";
		# file
		#print $_, "\n";
		# full file path
		#print $File::Find::name, "\n";
		#
		# Only look in 03-align/ directory
		if ($_ eq "align_summary.txt" && $File::Find::dir =~ /E\d+_.*\/03-align$/) {
				#print $File::Find::name, "\n";
			#get_tophat_align_stats($File::Find::name)
			get_tophat_align_stats($_, $File::Find::dir)
		}
}

### process the alignment_summary files from Tophat2
sub get_tophat_align_stats {
	# get the sample name from directory 
	my ($sample) = $_[1] =~ /(E\d+_.*)\//;
	#print $sample, "\n";
	$/ = "concordant";
	open(INPUT, $_[0]) || die "cannot open file\n\n";
	my $line = <INPUT>;
	
	my($lreads,$lmapped) = $line=~ /Left reads:\n\s+Input\s*:\s*(\d+)\n\s+Mapped\s*:\s*(\d+)/;
	my($rreads,$rmapped) = $line=~ /Right reads:\n\s+Input\s*:\s*(\d+)\n\s+Mapped\s*:\s*(\d+)/;

	my $lpct = sprintf("%.2f", $lmapped/$lreads *100);
	my $rpct = sprintf("%.2f", $rmapped/$rreads *100);
	print "$sample\tLEFT: \t $lreads \t" .  $lpct, "% mapped\t" .  "RIGHT:\t $rreads \t" .  $rpct . "% mapped\n";
}	

