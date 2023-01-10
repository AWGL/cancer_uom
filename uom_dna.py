from glob import glob
import subprocess
import sigfig
import yaml
import argparse 
import datetime
from dateutil.relativedelta import relativedelta


##EXAMPLE FUNCTION##
def display_discounted_price(instrument, discount):
  full_price = instrument_prices[instrument]
  discount_percentage = discount / 100
  discounted_price = full_price - (full_price * discount_percentage)
  print("The instrument's discounted price is: " + str(discounted_price))

instrument = 'Clarinet' #this could be the dictionary or a list, arguments need to be specified!!
discount = '20'

# Load uncertainty of measurement sample IDs and their corresponding reference standard into a dictionary


##ORIGINAL CODE##
with open("config_files/hd730_samples.yaml") as files:
	hd730_samples = yaml.load(files, Loader=yaml.FullLoader)


# Get all sample filepaths into list

	filepaths = []
	for sample in hd730_samples:
		filepaths += glob(f'/Output/results/*/Gathered_Results/Database/{sample}_variants.tsv')
	


# Put contents of each file into separate dictionaries 
#def files(comparison):

	for sample in filepaths:
		with open(sample) as file:
			hd730_samples_dict = {}
			for line in file:
				x = line.split('\t') 				# Split the columns based on tabs
				v = x[1] + ":" + x[2] + x[3] + ">" +  x[4] 	# Concatenate position and base change
				hd730_samples_dict[v] = x[5]               	#5 is vaf 
	 	
			hd730_dict = {}
			with open("reference_standards/TruQ1_RS_HD730.txt") as hd730:	# path where reference standard file is (for comparison)
				for line in hd730:
					x = line.split('\t')
					v = "chr" + x[3] + ":" + x[4]		# Concatenate position and base change
					hd730_dict[v] = float(x[7])
					# print(hd730_dict)
			
					# Splitting path into sample ID and run ID
					split_sample_path = sample.split("/") 
					split_sample_id = split_sample_path[6].split("_")

				# Comparing sample files to reference standard files to find matches
	 			#with open("UoM_results/uom_dna_hd730.txt", "a") as output_dna_hd730:	# Creates output of analyis as text file
				sample_id = split_sample_id[0]
				run_id = split_sample_path[3]
				for key, value in hd730_dict.items():
					worksheet = subprocess.run([f'grep {sample_id} /data/archive/*/{run_id}/SampleSheet.csv | cut -f 3 -d ","'], shell=True, capture_output=True)
					if key in hd730_samples_dict.keys():
						difference = float(hd730_samples_dict[key]) - value
						# Key is variant position, hd730_samples_dict[key] is sample vaf, difference is difference between expected and observed vaf, value is RS value, difference/value is % difference
						print(run_id, worksheet.stdout.rstrip(), sample_id, key, float(hd730_samples_dict[key]), value, (sigfig.round(difference, sigfigs=3)), (sigfig.round((difference/value)*100, sigfigs=3)), "True")# file = output_dna_hd730
					else:
 						print(run_id, worksheet.stdout.rstrip(), sample_id, key, '', "n/a", "n/a", "n/a", "n/a", "False")# file = output_dna_hd730)
	


## HD728
# Load uncertainty of measurement sample IDs and their reference standard into a dictionary
with open("config_files/hd728_samples.yaml") as files:
        hd728_samples = yaml.load(files, Loader=yaml.FullLoader)

# Get all sample filepaths into list
filepaths = []
for sample in hd728_samples:
        filepaths += glob(f'/Output/results/*/Gathered_Results/Database/{sample}_variants.tsv')


# Put contents of each file into separate dictionaries
for sample in filepaths:
	with open(sample) as file:
		hd728_samples_dict = {}
		for line in file:
			x = line.split('\t')                          # Split the columns based on tabs
			v = x[1] + ":" + x[2] + x[3] + ">" +  x[4]	# Concatenate position and base change
			hd728_samples_dict[v] = x[5]                  # 5 is vaf
			#print(sample, hd728_samples_dict)

	hd728_dict = {}
	with open("reference_standards/TruQ1_RS_HD728.txt") as hd728:
		for line in hd728:
			x = line.split('\t')
			v = "chr" + x[3] + ":" + x[4]
			hd728_dict[v] = float(x[7])           #7 is vaf
 			#print(hd728_dict)
                        
                        # Splitting up path to get sample ID and run ID
			split_sample_path = sample.split("/")
			split_sample_id = split_sample_path[6].split("_")

                       
	# with open("UoM_results/uom_dna_hd28.txt", "a") as output_dna_hd728:
		sample_id = split_sample_id[0]
		run_id = split_sample_path[3]
		for (key, value) in hd728_dict.items():
			worksheet = subprocess.run([f'grep {sample_id} /data/archive/*/{run_id}/SampleSheet.csv | cut -f 3 -d ","'], shell=True, capture_output=True)
			if key in hd728_samples_dict.keys():
				difference = float(hd728_samples_dict[key]) - value
				# Key is variant position, hd730_samples_dict[key] is sample vaf, difference is difference between expected and observed vaf, value is RS value, difference/value is % difference
				print(run_id, worksheet.stdout.rstrip(), sample_id, key, float(hd728_samples_dict[key]), value, (sigfig.round(difference, sigfigs=3)), (sigfig.round((difference/value)*100, sigfigs=3)), "True")# file = output_dna_hd728)
			else:
				print(run_id, worksheet.stdout.rstrip(),  sample_id, key, '', "n/a", "n/a", "n/a", "n/a", "False")# file = output_dna_hd728)


# Outputting runs with only last years date
# Need to add something different here to the function
def valid_date(s):
	
	parser.add_argument("-s", "--start date", dest="start_date", default=datetime.now() - relativedelta(years=1), type=valid_date, required=True, d: datetime.strptime(d, '%Y%m%d').date(), help="Date in the format yyyymmdd")

