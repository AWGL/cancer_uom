import pandas as pd
from glob import glob
import subprocess

# Create dictionary of gene and position for the reference standard file
with open("RS_rna.txt") as rna:
        rna_dict = {}
        for line in rna:
                x = line.strip().split('\t')       # Remove any spaces and split lines by tab
                rna_dict[x[0]] = None              # 0 is gene fusion
                #print(rna_dict)


# Get all files into list 
all_samples = glob('/Output/results/*/Gathered_Results/Database/22M81471_fusion_check.csv') + glob('/Output/results/*/Gathered_Results/Database/22M81472_fusion_check.csv') + glob('/Output/results/*/Gathered_Results/Database/22M82583_fusion_check.csv')
#print(all_samples)


# Put contents of each file into separate dictionaries
for sample in all_samples:
        with open(sample) as file:
                sample_dict = {}
                for line in file: 
                        x = line.split(',')
               	        sample_dict[x[0]] = None        #0 is gene fusion 
                        #print(sample_dict)

                        # Splitting up path to get sample ID and run ID
                        split_sample_path = sample.split("/")
                        split_sample_id = split_sample_path[6].split("_")

        # Comparing dictionaries with the reference standard dictionary
        with open("rna.txt", "a") as output_rna:        # Creates output into text file
                sample_id = split_sample_id[0]
                run_id = split_sample_path[3]
                for key, value in rna_dict.items():     # Key is gene fusion
                    # Adding in worksheet ID
                    worksheet = subprocess.run([f'grep {sample_id} /data/archive/*/{run_id}/SampleSheet.csv | cut -f 3 -d ","'], shell=True, capture_output=True)
                    if (key, value) in sample_dict.items():
                        print(run_id, worksheet.stdout.rstrip(), sample_id, key, "True")# file = output_rna)
                    else:
                        print(run_id, worksheet.stdout.rstrip(), sample_id key, "False")# file = output_rna)
                                         

