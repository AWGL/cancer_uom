import pandas as pd
from glob import glob
import subprocess
import os
import sigfig
import argparse
import datetime 

# Automatically give last years runs 

###########################
###	Functions	###
###########################

def parse_samples(sampleid_list):
        """
        #Load uncertainty of measurement sample IDs and their corresponding reference standard into a dictionary
        """

        sampleid = [sampleid_list] #[f'config_files/*_samples.yaml']

        for sample in sampleid:
                with open(sample) as s:
                        sampleid_list = yaml.load(s, Loader=yaml.FullLoader)

        return(sampleid_list)


def sample_file_list(sample_filepaths):	#NEED TO GET THIS TO DO BOTH HD728/30!!!
	"""
	#Get all UOM sample filepaths into list
	"""
	
	filepaths = []
	
	for sample in reference_dict:
		filepaths += glob(f'/Output/results/*/Gathered_Results/Database/{sample}_variants.tsv')

	return(filepaths)


#SPLIT THIS INTO MORE FUNCTIONS
def sample_files(filepaths):
	"""
	#Put position and base change of each sample file into a dictionary
	"""

	for sample in filepaths:
		with open(sample) as file:

			# This is the uom sample ID files dictionaries
			samples_dict = {}
			for line in file:
                        	x = line.split('\t')				# Split the columns based on tabs
       	                	v = x[1] + ":" + x[2] + x[3] + ">" +  x[4]      # Concatenate position and base change
                        	samples_dict[v] = x[5]                  	# 5 is vaf


def reference_files(reference_variants):
	""" 
	#Put position and base change of each reference file into a dictionary
	"""

	# This is the reference standard dictionaries
	reference_variants = {} 
	with open("reference_standards/TruQ1_RS_*.txt") as reference:	#pass in specific reference standard	Path where reference standard file is (for comparison)
		for line in reference:
			x = line.split('\t')
			v = "chr" + x[3] + ":" + x[4]				# Concatenate position and base change
			reference_variants[v] = float(x[7])           		# 7 is vaf


def split_filepaths(filepaths, reference_variants):
	"""
	#Split up the filepaths to get the samples ID and run ID
	"""

                        # Splitting up path to get sample ID and run ID
			split_sample_path = sample.split("/")
			split_sample_id = split_sample_path[6].split("_")

        # with open("UoM_results/uom_dna.txt", "a") as output_dna:	# Creates output file (HOW TO SPECIFY WHICH RS!!)
		sample_id = split_sample_id[0]
		run_id = split_sample_path[3]


def compare_files(filepaths, reference_variants, split_filepaths):	##ARE THESE THE RIGHT ARGUMENTS??
	"""
	#Compare the reference standard files to the sample files to determine matches
	"""

		for (key, value) in reference_variants.items():
			
			# Worksheet that corresponds with that run
			worksheet = subprocess.run([f'grep {sample_id} /data/archive/*/{run_id}/SampleSheet.csv | cut -f 3 -d ","'], shell=True, capture_output=True)
			if key in samples_dict.keys():

			# Key is variant position, samples_dict[key] is sample vaf, difference is difference between expected and observed vaf, value is RS value, difference/value is % difference
				difference = float(samples_dict[key]) - value
				print(run_id, worksheet.stdout.rstrip(), sample_id, key, float(samples_dict[key]), value, (sigfig.round(difference, sigfigs=3)), (sigfig.round((difference/value)*100, sigfigs=3)), "True")# file = output_dna
			else:				
				print(run_id, worksheet.stdout.rstrip(), sample_id, key, '', "n/a", "n/a", "n/a", "n/a", "False")# file = output_dna)

	##return(WHAT TO RETURN HERE  DOES THIS WORK WITH A PRINT STATEMENTS 

###########################
###	Programme	###
###########################

#if __name__ == '__main__':

#	# Arguments *dont need*
#	parser = argparse.ArgumentParser()
#	parser.add_argument('--config_files/hd728_samples.yaml', '-hd730', help = 'dictionary of sample IDs with hd728 rs')
#	parser.add_argument('--config_files/hd730_samples.yaml', '-hd728', help = 'dictionary of sample IDs with hd730 rs')
#	parser.add_argument('-- **variable name here** ##DO I NEED TO DO THIS FOR ALL SAMPLE IDS??
#	parser.add_argument('--reference_dict', 'r', help = '???	THIS NEEDS TO DO BOTH RS SOMEHOW
#	parser.add_argument('--filepaths', 'f', help = 'list of filepaths') ##????
#	args = parser.parse_args()

# Load uncertainty of measurement sample IDs and their corresponding reference standard into a dictionary
#reference_dict = parse_samples(*filepath*)

# Get all uom sample files into list
#file_list = list(args./Output/results/*/Gathered_Results/Database/{sample}_variants.tsv) THIS IS WRONG
	
#for files in files list function that makes it go sample by sample might call all functions call functions in a loop here 

#output = files(reference_dict, filepaths) 

#for smaple in ref dict, call files function but make sample specific

