
import pandas as pd
from glob import glob
import subprocess
import os

# Create dictionary of gene and position for the reference standard file hd730
hd730_dict = {}
with open("TruQ1_HD730.txt") as hd730:
	for line in hd730:
		x = line.split('\t')
		v = "chr" + x[3] + ":" + x[4] #concatenate position and base change
		hd730_dict[v] = None
		#print(hd730_dict)


# Get all files into list  
hd730_samples = glob('/Output/results/*/Gathered_Results/Database/21M70050_variants.tsv') + glob('/Output/results/*/Gathered_Results/Database/22M12181_variants.tsv') + glob('/Output/results/*/Gathered_Results/Database/22M06894_variants.tsv')
#print(hd730_samples)


# List all files in dictionary 
#def convert_dict(a):
#	init = iter(hd730_samples)
#	res_dct = dict(zip(init,init))
#	return res_dct
#print(convert_dict(hd730_samples))


# Put contents of each file into separate dictionaries
for sample in hd730_samples:
	with open(sample) as file:
		hd730_samples_dict = {}
		for line in file:
			x = line.split('\t') 				# Split the columns based on tabs
			v = x[1] + ":" + x[2] + x[3] + ">" +  x[4] 	# Concatenate position and base change
			hd730_samples_dict[v] = x[5]               	#5 is vaf 
			#print(hd730_samples_dict)
			
			# Splitting path into sample ID and run ID
			split_sample_path = sample.split("/") 
			split_sample_id = split_sample_path[6].split("_")

	# Comparing dictionaries with the reference standard dictionary
	#with open("dna_hd730.txt", "a") as output_dna_hd730:
	sample_id = split_sample_id[0]
	run_id = split_sample_path[3]	
	for key in hd730_dict.keys():
		worksheet = subprocess.run([f'grep {sample_id} /data/archive/*/{run_id}/SampleSheet.csv | cut -f 3 -d ","'], shell=True, capture_output=True)
		if key in hd730_samples_dict.keys():
			print(run_id, worksheet.stdout.rstrip(), sample_id, key, hd730_samples_dict[key], "True")# file = output_dna_hd730)
		else:
			print(run_id, worksheet.stdout.rstrip(), sample_id, key, '', "False")# file = output_dna_hd730)

	


# Create dictionary of gene and position for the reference standard file hd728
hd728_dict = {}
with open("TruQ1_RS_HD728.txt") as hd728:
        for line in hd728:
                x = line.split('\t')
                v = "chr" + x[3] + ":" + x[4]
                hd728_dict[v] = x[0]         	#0 is gene
                #print(hd728_dict)


# Combine list of sample paths for hd728
hd728_samples =  glob('/Output/results/*/Gathered_Results/Database/22M12180_variants.tsv') + glob('/Output/results/*/Gathered_Results/Database/22M06893_variants.tsv') + glob('/Output/results/*/Gathered_Results/Database/22M06896_variants.tsv')
#print(hd728_samples)


# Put contents of each file into separate dictionaries
for sample in hd728_samples:
        with open(sample) as file:
                hd728_samples_dict = {}
                for line in file:
                        x = line.split('\t')                          # Split the columns based on tabs
                        v = x[1] + ":" + x[2] + x[3] + ">" +  x[4]    # Concatenate position and base change
                        hd728_samples_dict[v] = x[5]                  # 5 is vaf
                        #print(sample, hd728_samples_dict)
                        
                        # Splitting up path to get sample ID and run ID
                        split_sample_path = sample.split("/")
                        split_sample_id = split_sample_path[6].split("_")

                       
        #with open("dna_hd28.txt", "a") as output_dna_hd728:
        sample_id = split_sample_id[0]
        run_id = split_sample_path[3]
        for key in hd728_dict.keys():
            worksheet = subprocess.run([f'grep {sample_id} /data/archive/*/{run_id}/SampleSheet.csv | cut -f 3 -d ","'], shell=True, capture_output=True)
            if key in hd728_samples_dict.keys():
               print(run_id, worksheet.stdout.rstrip(), sample_id, key, hd728_samples_dict[key], "True")# file = output_dna_hd728)
            else:
                print(run_id, worksheet.stdout.rstrip(),  sample_id, key, '', "False")# file = output_dna_hd728)

