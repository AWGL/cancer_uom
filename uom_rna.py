"""
Script to see whether or not variants supplied by known reference standards are called for the TSO500 RNA assay
during uncertainty of measurement runs
"""

import pandas as pd
from glob import glob
import subprocess
import argparse
from datetime import datetime
from datetime import date
import yaml


###########################
###     Functions       ###
###########################

def parse_rna_samples(rna_config_list):
        """
        Load uncertainty of measurement sample IDs and their corresponding reference standard into a dictionary
        """
        # This is the uncertainty of measurment sample ID:reference standard files
        config_file = open(sample_type, 'r')
         
        config_list = {}

        for config in config_list:

                        # Yaml file containing sample IDs and their reference standard
                        sampleid_dict = yaml.load(config file, Loader=yaml.FullLoader)

                        # Convert contents of yaml file into a dictionary                        
                        for key in sampleid_dict:
                        
                                config_dict[key] = sampleid_dict[key]
                        
        return config_dict


def rna_sample_file_list(reference_dict): 
        """
        Get all UOM crm sample filepaths from last year into list
        """
        
        reference_dict = parse_rna_samples([rna_config_list])

        filepath_list = []

        current_year = datetime.today().year
        last_year = [str(current_year -1)[2:]]
        
        # Getting the sample IDs
        for sample in reference_dict:

                # Getting all files ran last year
                for year in last_year:

                # Keep the root path, all files from last year with the sample
                filepaths += glob(f'/Output/results/{year}*/Gathered_Results/Database/{sample}_fusion_check.csv')

                if len(filepaths) == 0:

                        print(f'no files for sample {sample}')

                filepath_list = filepath_list + filepaths

        return filepath_list #loops dont work with this command?

        ##tsv_files_to_analyse = rna_sample_file_list(reference_dict)


def get_variants_in_files_rna(filepaths):
        """
        Put position and base change of each sample file into a dictionary
        """

        filepath_list = rna_sample_file_list(reference_dict)

        samples_dict = {}

        for sample in filepaths:

                sample_name = sample.split(',')[-1].strip('_fusion_check.csv') 

                samples_dict[sample_name] = {}

                with open(sample) as file:

                        # split the lines by tab
                        file = csv.reader(file, delimeter=',')

                        for line in file:

                                # No vaf for rna
                                samples_dict[x[0]] = None      

        return samples_dict

        ##get_variants_in_files(tsv_files_to_analyse)



def split_sample_filepaths_rna(filepaths):
        """
        #Split up the filepaths to get the samples ID and run ID
        """

        file_list = rna_sample_file_list(reference_dict, sample_path)

        # Splitting up path to get sample ID and run ID
        for tsv in tsvs_to_analyse:

                split_sample_path = tsv.split("/")
                split_sample_id = split_sample_path[6].split("_")

        # with open("UoM_results/uom_rna.txt", "a") as output_rna:      # Creates output file (HOW TO SPECIFY WHICH RS!!)
                sample_id = split_sample_id[0]
                run_id = split_sample_path[3]

        return sample_id, run_id

        #split_sample_filepaths(tsvs_to_analyse)



def get_variants_in_reference_file_rna(reference_variants):
        """
        # Create dictionary of fusion for the reference standard file
        """

        # Open RNA reference standards
        reference_files = glob("reference_standards/RS_rna.txt")

        for file in reference_files:

                with open(file) as reference:

                reference_variants_dict = {}

                        for line in rna:

                                x = line.strip().split('\t')

                                #0 is gene fusion
                                reference_variants_dict[x[0]] = None  

                return reference_variants_dict

        #get_variants_in_reference_files(reference_files)



def compare_rna_files(filepaths, reference_files, split_sample_filepaths)
        """
        # Comparing dictionaries with the reference standard dictionary
        """
                # This is the fusions
                for key, value in reference_variants_dict.items():

                #Worksheet that corresponds with that run
                    worksheet = subprocess.run([f'grep {sample_id} /data/archive/*/{run_id}/SampleSheet.csv | cut -f 3 -d ","'], shell=True, capture_output=True)
                    
                    if (key, value) in samples_dict.items():
                    
                        print(run_id, worksheet.stdout.rstrip(), sample_id, key, "True")

                    else:
                    
                        print(run_id, worksheet.stdout.rstrip(), sample_id, key, "False")
                                         

###########################
###     Programme       ###
###########################

if __name__ == '__main__':

#       # Arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('--config_file', 'config', help = 'yaml config file')
        parser.add_argument('--reference_dict', 'r', help = 'dictionary of sample IDs with rs')   
        parser.add_argument('--filepath_list', 'fl', help = 'list of sample filepaths')
        parser.add_argument('--file', 'f', help = 'splitting the filepaths into run id and sample id')
        parser.add_argument('--reference_variants', 'ref', help = 'dict of reference variants/vaf')
        
        args = parser.parse_args()

##THESE SHOULD BE SAME NAME AS IN RETURN COMMANDS?? 

# Load uncertainty of measurement sample IDs and their corresponding reference standard into a dictionary
config_dict = parse_rna_samples(args.[config_file])

# Get all uom sample files into list
filepath_list = rna_sample_file_list(args.reference_dict)

# Get all variants and their corresponding vaf in a dictionary
sample_variant_dict = get_variants_in_files_rna(args.filepath_list) #OR# get_variants_in_file(args.tsvs_to_analyse)     

# Split the sample filepaths into sample id and run id
split_paths = split_sample_filepaths_rna(args.file) #OR# split_sample_filepaths(args.tsvs_to_analyse)

# Get the reference variants and vaf into dictionaries
reference_variants_dict = get_variants_in_rna_reference_file(args.reference_files #OR# (args.reference_files)

                       
