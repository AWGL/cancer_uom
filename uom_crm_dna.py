"""
Script to see whether or not variants supplied by known reference standards are called for the CRM assay
during uncertainty of measurement runs
"""


from glob import glob
import subprocess
import sigfig
import argparse
from datetime import datetime
from datetime import date
import yaml
import csv


###########################
###	Functions	###
###########################

def parse_crm_samples(crm_config_list):
        """
        Load uncertainty of measurement sample IDs and their corresponding reference standard into a dictionary
        """
	# This is the uncertainty of measurment sample ID:reference standard files
        config_file = open(sample_type, 'r')
 
        config_dict = {}

        for config in crm_config_list:

        		# Loading in the yaml file
                	sampleid_dict = yaml.load(config_file, Loader=yaml.FullLoader)
        	
        		# Convert contents of yaml file into a dictionary
        		for key in sampleid_dict:
               		
               			config_dict[key] = sampleid_dict[key]
                        
        return config_dict



def crm_sample_file_list(reference_dict, sample_path): 
	"""
	Get all UOM crm sample filepaths from last year into list
	"""
	
	reference_dict = parse_crm_samples([crm_config_list])

	filepath_list = []

	current_year = datetime.today().year
	last_year = [str(current_year -1)[2:]]
	
	# Getting the sample IDs
	for sample in reference_dict:

		# Getting all files ran last year
		for year in last_year:

		# Keep the root path, all files from last year with the sample
		filepaths += glob(f'/Output/results/{year}*/NGHS-101X/{sample}/{year}*_VariantReport.txt')

		if len(filepaths) == 0:

			print(f'no files for sample {sample}')

		filepath_list = filepath_list + filepaths

	return filepath_list #loops dont work with this command?

	##tsv_files_to_analyse = sample_file_list(reference_dict)



def get_variants_in_crm_files(filepaths):
	"""
	Put position and base change of each sample file into a dictionary
	"""

	samples_dict = {}

	for sample in filepaths:

		sample_name = sample.split('/')[-1].strip('_VariantReport.txt') #not sure if this will do what i want (just get sample ID)

		samples_dict[sample_name] = {} # MAYBE MOVE THIS TO GET SAMPLES IN SEPARATE DICTIONARIES?

		with open(sample) as file:

			# split the lines by tab
			file = csv.reader(file, delimeter='\t')

			for line in file:

				# Remove the header line
				if line[1] != 'Variant':

				# Position and base change already concatenated in txt file
      	                	v = line[1]     

      	                	# 2 is vaf
                        	samples_dict[samples_name][v] = line[2]                  	

        return samples_dict

        ##get_variants_in_files(tsv_files_to_analyse)


		
def split_sample_filepaths_crm(filepaths):
	"""
	Split up the filepaths to get the samples ID and run ID
	"""

        # Splitting up path to get sample ID and run ID
        for tsv in tsvs_to_analyse:

		split_sample_path = tsv.split("/")
		split_sample_id = split_sample_path[6].split("_")

		sample_id = split_sample_id[4]
		run_id = split_sample_path[3]

	return sample_id, run_id

	#split_sample_filepaths(tsvs_to_analyse)



def get_variants_in_reference_files_crm(reference_variants):
	""" 
	Put position and base change of each reference file into a dictionary
	"""

	# This is the reference standard dictionaries
	reference_variants_dict = {} 

	# All reference files in a list
	reference_files = glob(f'reference_standards/TruQ1_RS_*.txt')

	for file in reference_files:

		with open(file) as reference:

			for line in reference:

				x = line.split('\t')

				# Concatenate position and base change
				v = x[3] + ":" + x[4]	

				# 7 is vaf			
				reference_variants_dict[v] = float(x[7])  

			##THIS PUTS BOTH REFERENCE FILES IN 1 DICT NOT 2 WHICH IS NEEDED!!
			return reference_variants_dict 

	#get_variants_in_reference_files(reference_files)    		



def compare_files(filepaths, reference_variants, split_sample_filepaths):
	"""
	Comparing dictionaries with the reference standard dictionary
 	"""	
 
		# Key is chr and pos, value is vaf	
		for key, value in reference_variants_dict.items():

		# Worksheet that corresponds to that run
		worksheet = subprocess.run([f'grep {sample_id} /data/archive/*/{run_id}/SampleSheet.csv | cut -f 2 -d ","'], shell=True, capture_output=True)
		
			if key in samples_dict.keys():

				difference = float(samples_dict[key]) - value

			# Key is variant position, samples_dict[key] is sample vaf, difference is difference between expected and observed vaf, value is RS value, difference/value is % difference
				print(run_id\
					, worksheet.stdout.rstrip()\
					, sample_id, key\
					, float(samples_dict[key])\
					, value\
					, (sigfig.round(difference, sigfigs=3))\
					, (sigfig.round((difference/value)*100, sigfigs=3))\
					, "True")

			else:

				print(run_id\
					, worksheet.stdout.rstrip()\
					, sample_id, key\
					, ''\
					, "n/a"\
					, "n/a"\
					, "n/a"\
					, "n/a"\
					, "False")


###########################
###	     Programme	    ###
###########################

if __name__ == '__main__':

#	# Arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('--config_file', 'config', help = 'yaml config file')
	parser.add_argument('--reference_dict', 'r', help = 'dictionary of sample IDs with rs')   
	parser.add_argument('--filepath_list', 'fl', help = 'list of sample filepaths')
	parser.add_argument('--file', 'f', help = 'splitting the filepaths into run id and sample id')
	parser.add_argument('--reference_variants', 'ref', help = 'dict of reference variants/vaf')
	
	args = parser.parse_args()

##THESE SHOULD BE SAME NAME AS IN RETURN COMMANDS?? 

# Load uncertainty of measurement sample IDs and their corresponding reference standard into a dictionary
config_dict = parse_crm_samples(args.[config_file])

# Get all uom sample files into list
filepath_list = crm_sample_file_list(args.reference_dict)

# Get all variants and their corresponding vaf in a dictionary
sample_variant_dict = get_variants_in_files_crm(args.filepath_list) #OR# get_variants_in_file(args.tsvs_to_analyse)	

# Split the sample filepaths into sample id and run id
split_paths = split_sample_filepaths_crm(args.file) #OR# split_sample_filepaths(args.tsvs_to_analyse)

# Get the reference variants and vaf into dictionaries
reference_variants_dict = get_variants_in_crm_reference_file(args.reference_files #OR# (args.reference_files)

                       