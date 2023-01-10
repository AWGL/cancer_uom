import pandas as pd
from glob import glob
import subprocess
import sigfig

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

	
		# Put RS file contents into dictionary
		hd730_dict = {}
		with open("TruQ1_RS_HD730_crm.txt") as hd730:
			for line in hd730:
				x = line.split('\t')
				#v = "chr" + x[3] + ":" + x[4] #concatenate position and base change
				hd730_dict[x[3]] = float(x[6])


			# Splitting paths of sample files  into sample ID and run ID
			split_sample_path = sample.split("/")
			split_sample_id = split_sample_path[6].split("_")


	# Comparing dictionaries with the reference standard dictionary
 		#with open("uom_crm_dna_hd730.txt", "a") as output_crm_dna_hd730:
		sample_id = split_sample_id[4]
		run_id = split_sample_path[3]
		for key, value in hd730_dict.items():
			worksheet = subprocess.run([f'grep {sample_id} /data/archive/*/{run_id}/SampleSheet.csv | cut -f 2 -d ","'], shell=True, capture_output=True)
			if key in hd730_samples_dict.keys():
				difference = float(hd730_samples_dict[key]) - value
			# Key is variant position, hd730_samples_dict[key] is sample vaf, difference is difference between expected and observed vaf, value is RS value, difference/value is % difference
				print(run_id, worksheet.stdout.rstrip(), sample_id, key, float(hd730_samples_dict[key]), value, (sigfig.round(difference, sigfigs=3)), (sigfig.round((difference/value)*100, sigfigs=3)), "True")# file = output_crm_dna_hd730)
			else:
				print(run_id, worksheet.stdout.rstrip(), sample_id, key, '', "n/a", "n/a", "n/a", "n/a", "False")# file = output_crm_dna_hd730)
