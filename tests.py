import unittest
import yaml
import pathlib as pl
from uom_crm_dna.py import *
from uom_dna.py import *
from uom_rna.py import *

dna_config_file = '/home/niamh/Documents/Niamh_uom/config_files/dna_config.yaml'

rna_config_file = 'home/niamh/Documents/Niamh_uom/config_files/rna_config.yaml'

dna_path_file = '/home/niamh/Documents/Niamh_uom/cancer_uom/cancer_uom/filepaths/dna_filepaths.txt'

rna_path_file = '/home/niamh/Documents/Niamh_uom/cancer_uom/cancer_uom/filepaths/rna_filepaths.txt'

crm_path_file = '/home/niamh/Documents/Niamh_uom/cancer_uom/cancer_uom/filepaths/crm_filepaths.txt'

class test_uom_dna(unittest.TestCase):

	def test_dna_config(self):
		"""
		Test that config files gives sample and corresponding reference
		standard in a dictionary

		Output:
			Sample ID: Corresponding reference standard
		"""

		with open(dna_config_file) as config:
			
			sample, reference = open_config_file(config)

			self.assertEqual(sample, reference)


	def if_dna_file_exist(self):
		"""
		Gives all filepaths containing samples ID present in config files
		Only 2022 runs
		"""

		# Open file with known paths in
		with open(path_file) as path_file:

			for path in path_file:

				find_paths = pl.Path(path)

				# Check whether all paths have been found
				self.assertEqual((str(find_paths), find_paths.is_file()), (str(find_paths), True))


	def test_positions_basechange_dna(self, samples_dict):
		"""
		Position, base change and vaf of each sample is in a dictionary
		Test one known genomic coordinates and vaf
		"""

		# Known variant and vaf from example path below:
		# '/Output/results/220725_A00748_0282_AH7GL5DRK2/Gathered_Results/Database/22M12181_variants.tsv'
		known_variant_dict = {'chr9:133589309AG': '0.0957'}

		if known_variant_dict in samples_dict:

			self.assertTrue()

			#OR

		self.assertIn(known_variant_dict, samples_dict)


	def test_reference_dict_dna(self, reference_variants_dict):
		"""
		Position and base change in reference standard are in dictionary
		For both HD728 and HD730 standard
		"""

		# Known reference standard file
		HD728_reference_file = 'reference_standards/TruQ1_RS_HD728.txt'
		HD730_reference_file = 'reference_standards/TruQ1_RS_HD730.txt'

		# Known variant in reference standards
		HD728_variant = {'chr13:28502634CATG>C': '0.05'}
		HD730_variant = {'chr55241707G>A': '0.167'}

		if HD728_variant in HD728_reference_file:

				self.assertTrue()

		if HD730_variant in HD730_reference_file:

				self.assertTrue()

				#OR

		self.assertIn(HD728_variant, HD728_reference_file)
		self.assertIn(HD730_variant, HD730_reference_file)


	def split_dna_path_correct(self):
		"""
		Test sample ID and run ID have separated
		"""

		# Known file_path
		path_to_split = 'Output/results/220725_A00748_0282_AH7GL5DRK2/Gathered_Results/Database/22M12181_variants.tsv'

		# Known sample and run ID
		example_sample_id = '22M12181'
		example_run_id = '220725_A00748_0282_AH7GL5DRK2'

		# Deployed code used
		split_path = path_to_split.split('/')
		split_sample_id = split_path[6].split('_')

		sample_id = split_sample_id[0]
		run_id = split_path[3]

		# Check if the IDs from the known and test are equal
		self.assertEqual(example_sample_id, sample_id, msg = 'Samples are equal')
		self.assertEqual(example_run_id, run_id, msg = 'Runs are equal')



class test_uom_crm(unittest.TestCase):

	def if_crm_file_exist(self):
		"""
		Gives all filepaths containing samples ID present in config files
		Only 2022 runs
		"""

		# Open file with known paths in
		with open(path_file) as path_file:

			for path in path_file:

				find_paths = pl.Path(path)

				# Check whether all paths have been found
				self.assertEqual((str(find_paths), find_paths.is_file()), (str(find_paths), True))


	def test_positions_basechange_crm(self, samples_dict):
		"""
		Position, base change and vaf of each sample is in a dictionary
		Test one known genomic coordinates and vaf
		"""

		# Known variant and vaf from example path below:
		# /Output/results/220624_M00766_0490_000000000-KG36M/NGHS-101X/21M70050/220707_M00766_0493_000000000-KG36J_21M70050_VariantReport.txt
		known_variant_dict = {'ch1:162724865T>C': '0.252'}

		if known_variant_dict in samples_dict:

			self.assertTrue()

			#OR

			self.assertIn(known_variant_dict, samples_dict)


	def split_crm_path_correct(self):
		"""
		Test sample ID and run ID have separated
		"""

		# Known file_path
		path_to_split = '/Output/results/220624_M00766_0490_000000000-KG36M/NGHS-101X/21M70050/220707_M00766_0493_000000000-KG36J_22M70050_VariantReport.txt'

		# Known sample and run ID
		example_sample_id = '21M70050'
		example_run_id = '220624_M00766_0490_000000000-KG36M'

		# Deployed code used
		split_path = path_to_split.split('/')
		split_sample_id = split_path[6].split('_')

		sample_id = split_sample_id[4]
		run_id = split_path[3]

		# Check if the IDs from the known and test are equal
		self.assertEqual(example_sample_id, sample_id, msg = 'Samples are equal')
		self.assertEqual(example_run_id, run_id, msg = 'Runs are equal')



class test_uom_rna(unittest.TestCase):

	def test_rna_config(self):
		"""
		Test that config files gives sample and corresponding reference
		standard in a dictionary

		Output:
			Sample ID: Corresponding reference standard
		"""

		with open(rna_config_file) as config:
			
			sample, reference = open_config_file(config)

			self.assertEqual(sample, reference)


	def if_rna_file_exist(self):
		"""
		Gives all filepaths containing samples ID present in config files
		Only 2022 runs
		"""

		# Open file with known paths in
		with open(rna_path_file) as path_file:

			for path in path_file:

				find_paths = pl.Path(path)

				# Check whether all paths have been found
				self.assertEqual((str(find_paths), find_paths.is_file()), (str(find_paths), True))


	def test_positions_basechange_rna(self, samples_dict):
		"""
		Fusion of each sample is in a dictionary
		Test one known fusion
		"""

		# Known variant and vaf from example path below:
		# /Output/results/220620_A01771_0050_AH7K37DRX2/Gathered_Results/Database/22M81471_fusion_check.csv
		known_fusion = 'EGFR-SEPT14'

		if known_fusion in samples_dict:

			self.assertTrue()

			#OR

			self.assertIn(known_variant_dict, samples_dict)


	def test_reference_dict_crm(self, reference_variants_dict):
		"""
		Fusion in reference standard are in dictionary
		For both HD728 and HD730 standard
		"""

		# Known reference standard file
		with open('RS_rna.txt') as rna_reference_file:

			# Known fusion in reference standards
			rna_fusion = 'ETV6-NTRK3'

			if rna_fusion in rna_reference_file:

				self.assertTrue()
		
				#OR

				self.assertIn(rna_fusion, rna_reference_file)


	def split_rna_path_correct(self):
		"""
		Test sample ID and run ID have separated
		"""

		# Known file_path
		path_to_split = '/Output/results/220620_A01771_0050_AH7K37DRX2/Gathered_Results/Database/22M81471_fusion_check.csv'

		# Known sample and run ID
		example_sample_id = '22M81471'
		example_run_id = '220620_A01771_0050_AH7K37DRX2'

		# Deployed code used
		split_path = path_to_split.split('/')
		split_sample_id = split_path[6].split('_')

		sample_id = split_sample_id[0]
		run_id = split_path[3]

		# Check if the IDs from the known and test are equal
		self.assertEqual(example_sample_id, sample_id, msg = 'Samples are equal')
		self.assertEqual(example_run_id, run_id, msg = 'Runs are equal')


if __name__ == '__main__':
	unittest.main()
