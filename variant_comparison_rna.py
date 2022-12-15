import pandas as pd
from glob import glob


# Create dictionary of gene and position for the reference standard file
with open("RS_rna.txt") as rna:
        rna_dict = {}
        for line in rna:
                x = line.strip().split('\t')
                rna_dict[x[0]] = None  #0 is gene fusion
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


# Comparing dictionaries with the reference standard dictionary
        with open("rna.txt", "a") as output_rna:
            for key, value in rna_dict.items():
                if (key, value) in sample_dict.items():
                    print(sample, key, "True", file = output_rna)
                else:
                    print(sample, key, "False", file = output_rna)
                                         

