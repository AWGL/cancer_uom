"""
Script to see whether or not variants supplied by known reference standards are called for the TSO500 DNA assay
during uncertainty of measurement runs
"""

import pandas as pd
import itertools
from glob import glob
import subprocess
import os
import sigfig
import argparse
from datetime import datetime
from datetime import date
import yaml
import csv


###########################
###	Functions	###
###########################

def parse_dna_config():
	"""
	Load uncertainty of measurement sample IDs and their corresponding reference standard into a dictionary
	"""

	# Load in the yaml file - This will need to change for local location of config file
	with open('/home/v.ni286029/UoM_project/config_files/dna_config.yaml') as config:

		config_file = yaml.load(config, Loader=yaml.FullLoader)	

	return config_file


def dna_sample_file_list(config_file): 
	"""
	Get all UOM dna sample filepaths from last year into list
	"""

	filepath_list = []

	current_year = datetime.today().year
	last_year = [str(current_year -1)[2:]]

	# Getting the sample IDs
	for sample in config_file:
		
		# Keep the root path, all files from last year with the sample
		filepaths = glob(f'/Output/results/{last_year}*/Gathered_Results/Database/{sample}_variants.tsv')
		
		if len(filepaths) == 0:

			print(f'no files for sample {sample}')

		filepath_list = list(itertools.chain(filepath_list, filepaths))


	return filepath_list 


def get_variants_in_dna_files(filepaths):
	"""
	Put position and base change of each sample file into a dictionary
	"""

	samples_dict = {}

	for sample in filepaths:
		
		with open(sample) as file:

			# split the lines by tab
			sample_files = csv.reader(file, delimiter='\t')

			for line in sample_files:
			
				# Remove the header line
				if line[1] != 'Variant':

					# Position and base change already concatenated in txt file     
					v = line[1] + ":" + line[2] + line[3] + ">" +  line[4]

					# 2 is vaf
					samples_dict[v] = line[5]

	return samples_dict


def get_variants_in_reference_files_dna():
	"""
	Put position and base change of each reference file into a dictionary
	"""

	# This is the reference standard dictionaries
	reference_variants_dict = {}

	# All reference files in a list - This will need to change to suit reference standard file location

	reference_files = glob(f'/home/v.ni286029/UoM_project/reference_standards/TruQ1_RS*.txt')

	for file in reference_files:

		with open(file) as reference:

			for line in reference:

				x = line.split('\t')

				# Concatenate position and base change
				v = "chr" + x[3] + ":" + x[4]

				# 7 is vaf
				reference_variants_dict[v] = float(x[7])
				
	return reference_variants_dict


def compare_files(filepath_list, reference_variants_dict, samples_dict):
	"""
	Splitting up filepaths to get sample and run IDs separately
	Compare the reference standard files to the sample files to determine matches
	"""

	# Splitting up filepaths
	for file in filepath_list:

		split_sample_path = file.split("/")
		split_sample_id = split_sample_path[6].split("_")

		sample_id = split_sample_id[0]
		run_id = split_sample_path[3]
	
		for variant, vaf in reference_variants_dict.items():

			# Worksheet that corresponds to that run
			worksheet = subprocess.run([f'grep {sample_id} /data/archive/*/{run_id}/SampleSheet.csv | cut -f 3 -d ","'], shell=True, capture_output=True)
			if variant in samples_dict.keys():

				difference = float(samples_dict[variant]) - vaf

				# Key is variant position, samples_dict[key] is sample vaf, difference is difference between expected and observed vaf, value is RS value, difference/value is % difference
				print(run_id\
					, worksheet.stdout.rstrip()\
					, sample_id\
					, variant\
					, float(samples_dict[variant])\
					, vaf\
					, (sigfig.round(difference, sigfigs=3))\
					, (sigfig.round((difference/vaf)*100, sigfigs=3))\
					, "True")

			else:

				print(run_id\
					, worksheet.stdout.rstrip()\
					, sample_id\
					, variant\
					, ''\
					, "n/a"\
					, "n/a"\
					, "n/a"\
					, "n/a"\
					, "False")



###########################
###	Programme	###
###########################

# if __name__ == '__main__':

# #	# Arguments
# 	parser = argparse.ArgumentParser()
# 	parser.add_argument('--config_file', 'config', help = 'yaml config file')
# 	parser.add_argument('--reference_dict', 'r', help = 'dictionary of sample IDs with rs')
# 	parser.add_argument('--filepath_list', 'fl', help = 'list of sample filepaths')
# 	parser.add_argument('--file', 'f', help = 'splitting the filepaths into run id and sample id')
# 	parser.add_argument('--reference_variants', 'ref', help = 'dict of reference variants/vaf')

# 	args = parser.parse_args()


# Load uncertainty of measurement sample IDs and their corresponding reference standard into a dictionary
config_file = parse_dna_config()

# Get all uom sample files into list
filepath_list = dna_sample_file_list(config_file)

# Get all variants and their corresponding vaf in a dictionary
sample_variant_dict = get_variants_in_dna_files(filepath_list)	

# Get the reference variants and vaf into dictionaries
reference_variants_dict = get_variants_in_reference_files_dna()

#Final output
compare_files = compare_files(filepath_list, reference_variants_dict, sample_variant_dict)
