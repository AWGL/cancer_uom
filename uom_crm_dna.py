import pandas as pd
from glob import glob

# Create dictionary of gene and position for the reference standard file
hd730_dict = {}
with open("TruQ1_RS_HD730_crm.txt") as hd730:
        for line in hd730:
                x = line.split('\t')
                hd730_dict[x[3]] = None		#3 is variant
                #print(hd730_dict)


#Get all files into a list 
hd730_samples = glob('/Output/results/*/NGHS-101X/21M70050/*_21M70050_VariantReport.txt') + glob('/Output/results/*/NGHS-101X/22M12181/*_22M12181_VariantReport.txt') + glob('/Output/results/*/NGHS-101X/22M06894/*_22M06894_VariantReport.txt')
#print(hd730_samples)


# Put contents of each file into separate dictionaries
for sample in hd730_samples:
        with open(sample) as file:
                hd730_samples_dict = {}
                for line in file:
                        x = line.split('\t') # Split the columns based on tabs
                        hd730_samples_dict[x[1]] = x[2]   # 1 is variant, 2 is vaf
                        #print(hd730_samples_dict)

			# Splitting path into sample ID and run ID
                        split_sample_path = sample.split("/")
                        split_sample_id = split_sample_path[6].split("_")

	# Comparing dictionaries with the reference standard dictionary
        #with open("crm_dna_hd730.txt", "a") as output_crm_dna_hd730:
                sample_id = split_sample_id[4]
                run_id = split_sample_path[3]
                for key in hd730_dict.keys():
                    #worksheet = subprocess.run([f'grep {sample_id} /data/archive/*/{run_id}/SampleSheet.csv | cut -f  -d ","'], shell=True, capture_output=True)		
                    if key in hd730_samples_dict.keys():
                        print(run_id, sample_id, key, hd730_samples_dict[key], "True") # file = output_crm_dna_hd730)
                    else:
                        print(run_id, sample_id, key, '', "False")# file = output_crm_dna_hd730)


# HD728 samples were not run
# Create dictionary of gene and position for the hd728 reference standard file
hd728_dict = {}
with open("TruQ1_RS_HD728_crm.txt") as hd728:
        for line in hd728:
                x = line.split('\t')
                hd728_dict[x[3]] = x[0]         #3 is variant, 0 is gene
                #print(hd728_dict)


#Get all files into a list
hd728_samples = glob('/Output/results/*/NGHS-101X/22M12180/*_22M12180_VariantReport.txt') + glob('/Output/results/*/NGHS-101X/22M06893/*_22M06893_VariantReport.txt')+ glob('/Output/results/*/NGHS-101X/22M06896/*_22M06896_VariantReport.tsv')
print(hd728_samples)


# Put contents of each file into separate dictionaries
for sample in hd728_samples:
        with open(sample) as file:
                hd728_samples_dict = {}
                for line in file:
                        x = line.split('\t')    # Split the columns based on tabs
                        hd728_samples_dict[x[1]] = x[5]         # 2 is variant, 5 is vaf
                        #print(sample, hd728_samples_dict)

                        # Splitting up path to get sample ID and run ID
                        split_sample_path = sample.split("/")
                        split_sample_id = split_sample_path[6].split("_")

                        # Comparing both keys and values
       # with open("crm_dna_hd728.txt", "a") as output_crm_dna_hd728:     
                        sample_id = split_sample_id[4]
                        run_id = split_sample_path[3]
                for key in hd728_dict.keys():
                    if key in hd728_samples_dict.keys():
                        print(run_id, sample_id, key, hd728_samples_dict[key], "True")# file = output_crm_dna_hd728)
                    else:
                        print(run_id, sample_id, key, '', "False")# file = output_crm_dna_hd728)

