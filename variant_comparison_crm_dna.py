import pandas as pd
from glob import glob

# Create dictionary of gene and position for the reference standard file
hd730_dict = {}
with open("TruQ1_RS_HD730_crm.txt") as hd730:
        for line in hd730:
                x = line.split('\t')
                hd730_dict[x[3]] = None		#3 is variant, 0 is gene
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

# Comparing dictionaries with the reference standard dictionary
			# Comparing keys and values
        #with open("crm_dna_hd730.txt", "a") as output_crm_dna_hd730:       
                for key in hd730_dict.keys():
                    if key in hd730_samples_dict.keys():
                        print(sample, key, hd730_samples_dict[key], "True") # file = output_crm_dna_hd730)
                    else:
                        print(sample, key, '', "False")# file = output_crm_dna_hd730)
                        #final_matches = {key: value for key, value in hd730_dict.items() if (key, value) in hd730_samples_dict.items()}
                        #print(sample, final_matches)

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

                        # Comparing both keys and values
       # with open("crm_dna_hd728.txt", "a") as output_crm_dna_hd728:     
                for key in hd728_dict.keys():
                    if key in hd728_samples_dict.keys():
                        print(sample, key, hd728_samples_dict[key], "True")# file = output_crm_dna_hd728)
                    else:
                        print(sample, key, '', "False")# file = output_crm_dna_hd728)
                       #final_matches = {key: value for key, value in hd728_dict.items() if (key, value) in hd728_samples_dict.items()}
                      #print(sample, final_matches)

