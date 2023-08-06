"""
Plots the distribution of reads in a BAM file around a given set of features
in a BED file. The user can specify which end (5' or 3') of the reads and the
features will be used as reference for the comparison. For example: We assume
that the user selects the 5' end of the reads and the 5' end of the features
as reference. Then a read that maps at position 10 of chr1 will be at a
relative position of -5 nt compared to a feature aligning at position 15 of
chr1. The same concept is applied for all reads against all features and a
distribution of relative positions is constructed.
"""

import pysam
import argparse
import numpy as np
import matplotlib.pyplot as plt

def find_pos(start, end, strand, pos):
	if pos != '5p' and pos != '3p':
		raise ValueError('Incorrectly specified position')
	if strand != '+' and strand != '-':
		raise ValueError('Incorrectly specified strand')
	final_pos = start
	if strand == '-' and pos == '5p' or strand == '+' and pos == '3p':
		final_pos = end
	return final_pos

def relative_pos(bed, read, fpos, rpos):
	"""
	rel_pos calculates the relative position between the two reference
	positions of a bed and a reads entry.
	"""
	# NOTE: the relative position is supposed to indicate if one is upstream
	# or downstream of the other. Pay attention to the strand.
	fstart, fend, fstrand = bed[0], bed[1], bed[2]
	feat_pos = find_pos(fstart, fend, fstrand, fpos)
	read_strand = '+' if read.is_forward else '-'
	read_pos = find_pos(read.reference_start, read.reference_end - 1, read_strand, rpos)
	rel_pos = read_pos - feat_pos
	if fstrand == '-':
		rel_pos *= -1
	return rel_pos

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-m","--bam",
                    help = "BAM file with reads. Must be indexed.")
	parser.add_argument("-b","--bed",
                    help = "BED file with features.")
	parser.add_argument("-u","--up", type = int, default = 100,
                    help = "Number of nts to plot upstream of pos. (default: %(default)s)")
	parser.add_argument("-d","--down", type = int, default = 100,
                    help = "Number of nts to plot downstream of pos. (default: %(default)s)")
	parser.add_argument("-f","--fpos", default='5p',
                    help = "Reference point for features; one of 5p or 3p (default: %(default)s)")
	parser.add_argument("-r","--rpos", default='5p',
                    help = "Reference point for reads; one of 5p or 3p (default: %(default)s)")
	parser.add_argument("-o", "--pdf",
                    help = "Output pdf file with plot")
	args = parser.parse_args()


	# Initialize a histogram
	hist = {i : 0 for i in range(-1 * args.up, args.down + 1)}

	# Open the bam file
	bamfile = pysam.AlignmentFile(args.bam, "rb")


	# Open and loop on the BED file line by line. For each line query the BAM file
	# to get overlapping reads. Calculate relative positions and add in the
	# histogram. NOTE: BED files are 0 based files.
	feature_count = 0
	total_counts = 0
	allowed_counts = 0
	with open(args.bed) as bed:
		for line in bed:
			feature_count += 1
			cols = line.strip().split('\t')
			chr = cols[0]
			start = int(cols[1])
			end = int(cols[2]) - 1 # BED files are zero based i.e. [coord,coord)
			strand = str(cols[5])  # Can be + or -
			feat = [start, end, strand]
			# Fetch overlapping BAM entries
			reads = bamfile.fetch(chr, start, end)
			#reads_counts.append(bamfile.count(chr, start, end))
			# Calculate relative positions and append to histogram
			for read in reads:
				total_counts += 1
				rel_pos = relative_pos(feat, read, args.fpos, args.rpos)
				if rel_pos > -1 * args.up and rel_pos < args.down:
					allowed_counts += 1
					hist[rel_pos] += 1

	k = list(hist.keys())
	v = [hist[i] for i in k]
	print('Total features: ' + str(feature_count))
	print('Total reads overlap: ' + str(sum(total_counts)))
	print('Total reads allowed: ' + str(allowed_counts))
	fig = plt.figure()
	plt.hist(k, np.histogram_bin_edges(range(-1 * args.up, args.down + 1)), weights=v, edgecolor=(0, 0, 0))
	plt.title('Histogram of Relative Read Positions')
	plt.xlabel('Relative Position')
	plt.ylabel('Count')
	plt.savefig(args.pdf)
	plt.close(fig)

