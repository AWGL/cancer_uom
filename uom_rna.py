"""
Script to see whether or not variants supplied by known reference standards are called for the TSO500 RNA assay
during uncertainty of measurement runs
"""

import pandas as pd
import itertools
from glob import glob
import subprocess
import argparse
from datetime import datetime
from datetime import date
import yaml
import csv


###########################
###     Functions       ###
###########################

def parse_rna_config():
	"""
	Load uncertainty of measurement sample IDs and their corresponding reference standard into a dictionary
	"""

	# Load in the yaml file
	with open('/home/v.ni286029/UoM_project/config_files/rna_config.yaml') as config:

		config_file = yaml.load(config, Loader=yaml.FullLoader) 
		
	return config_file


def rna_sample_file_list(config_file): 
	"""
	Get all UOM crm sample filepaths from last year into list
        """
        
	filepath_list = []

	current_year = datetime.today().year
	last_year = [str(current_year -1)[2:]]
                
	# Getting the sample IDs
	for sample in config_file:
                
		# Keep the root path, all files from last year with the sample                
		filepaths = glob(f'/Output/results/{last_year}*/Gathered_Results/Database/{sample}*_fusion_check.csv')

		if len(filepaths) == 0:

			print(f'no files for sample {sample}')

		filepath_list = list(itertools.chain(filepath_list, filepaths))


	return filepath_list 


def get_variants_in_files_rna(filepaths):
	"""
	Put position and base change of each sample file into a dictionary
	"""

	samples_dict = {}

	for sample in filepaths:

		with open(sample) as file:

			# split the lines by tab
			sample_files = csv.reader(file, delimiter=',')
			
			for line in sample_files:
				
				
				v = line[0]

				# No vaf for rna
				samples_dict[v] = None

	return samples_dict


def get_variants_in_reference_file_rna():
	"""
	Create dictionary of fusion for the reference standard file
	"""

	# Open RNA reference standards
	reference_files = glob('/home/v.ni286029/UoM_project/reference_standards/RS_rna.txt')

	for file in reference_files:

		with open(file) as reference:

			reference_variants_dict = {}

			for line in reference:

				x = line.strip().split('\t')

				#0 is gene fusion
				reference_variants_dict[x[0]] = None  

	return reference_variants_dict


def compare_files(filepath_list, reference_variants_dict, samples_dict):
	"""
	# Comparing dictionaries with the reference standard dictionary
	"""

	# Splitting up path to get sample ID and run ID
	for path in filepath_list:

		split_sample_path = path.split("/")
		split_sample_id = split_sample_path[6].split("_")

		sample_id = split_sample_id[0]
		run_id = split_sample_path[3]

		# This is the fusions
		for variant, value in reference_variants_dict.items():

			#Worksheet that corresponds with that run
			worksheet = subprocess.run([f'grep {sample_id} /data/archive/*/{run_id}/SampleSheet.csv | cut -f 3 -d ","'], shell=True, capture_output=True)
                    
			if (variant, value) in samples_dict.items():
                    
				print(run_id, worksheet.stdout.rstrip(), sample_id, variant, "True")

			else:
                
				print(run_id, worksheet.stdout.rstrip(), sample_id, variant, "False")


###########################
###     Programme       ###
###########################

# if __name__ == '__main__':

# #       # Arguments
#         parser = argparse.ArgumentParser()
#         parser.add_argument('--config_file', 'config', help = 'yaml config file')
#         parser.add_argument('--reference_dict', 'r', help = 'dictionary of sample IDs with rs')   
#         parser.add_argument('--filepath_list', 'fl', help = 'list of sample filepaths')
#         parser.add_argument('--file', 'f', help = 'splitting the filepaths into run id and sample id')
#         parser.add_argument('--reference_variants', 'ref', help = 'dict of reference variants/vaf')
        
#         args = parser.parse_args()


# Load uncertainty of measurement sample IDs and their corresponding reference standard into a dictionary
config_file = parse_rna_config()

# Get all uom sample files into list
filepath_list = rna_sample_file_list(config_file)

# Get all variants and their corresponding vaf in a dictionary
samples_dict = get_variants_in_files_rna(filepath_list)  

# Get the reference variants and vaf into dictionaries
reference_variants_dict = get_variants_in_reference_file_rna()

#Final output 
compare_rna_files = compare_files(filepath_list, reference_variants_dict, samples_dict)
                       
