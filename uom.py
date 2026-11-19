#!/usr/bin/env python3

import argparse
from itertools import count
import os

import numpy as np
import pandas as pd
import yaml
from scipy.stats import binomtest

"""
usage: python uom_ctdna.py [-h] [--config CONFIG] [--rs RS] [--samples SAMPLES] [--out OUT]
use help flag for more info
"""

def build_file_path(assay_config, run_id, sample_id):
	"""Return correct variant file path for given run_id and sample_id."""
	assay_name = assay_config.get("name")
	run_str = str(run_id)
	try:
		numeric_part = int(run_str[:4])
	except ValueError:
		numeric_part = 0

	if "240718" in run_str and assay_name == "ctdna":
		base_dir = assay_config.get("240718_database_dir").format(run_str=run_str)
	elif numeric_part > 2404:
		base_dir = assay_config.get("newer_run_database_dir").format(run_str=run_str)
	else:
		year = 2000 + int(run_str[:2])
		month = run_str[2:4]
		base_dir = assay_config.get("archive_run_database_dir").format(year=year, month=month, run_str=run_str)
	
	variant_file = assay_config.get("variant_file_path").format(base_dir=base_dir, sample_id=sample_id)
	fusion_file = assay_config.get("fusion_file_path").format(base_dir=base_dir, sample_id=sample_id)
	return variant_file, fusion_file


def normalize_variant(variant_str):
	"""Normalize variant like '14:105246551C>T' -> 'chr14:105246551C>T'."""
	if pd.isna(variant_str):
		return None
	variant_str = str(variant_str).strip()
	if "--" in variant_str:
		# fusion, return as-is
		return variant_str
	if not variant_str.startswith("chr"):
		variant_str = "chr" + variant_str
	return variant_str


def load_reference_variants(rs_path):
	"""Load rs_ctDNA.csv → dict of {variant: ref_vaf}, tolerant of column name variations."""
	
	try:
		os.path.exists(rs_path)
		print(f"Reference file exists        : {rs_path}")
	except FileNotFoundError:
		print(f"Reference file does not exist: {rs_path}")

	df = pd.read_csv(rs_path)
	# Normalize column names for easy matching
	df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

	# find VCF_description (variant) column
	vcf_col = next((c for c in df.columns if "vcf" in c and "desc" in c), None)
	# find AF% column
	af_col = next((c for c in df.columns if "af" in c), None)

	if vcf_col is None:
		raise ValueError(f"Couldn't find 'VCF_description'-like column in {rs_path}")
	if af_col is None:
		print("⚠️ Warning: no AF column found, using 0 for all VAFs")
		df["af_dummy"] = None
		af_col = "af_dummy"

	ref_dict = {}
	for _, row in df.iterrows():
		variant = normalize_variant(row[vcf_col])
		try:
			vaf = np.round(float(row[af_col]) / 100, 5)
		except (ValueError, TypeError):
			vaf = None
		if variant:
			ref_dict[variant] = vaf
	return ref_dict


def load_sample_variants(variant_path):
	"""Load one *_variants.tsv file → dict {variant: sample_vaf}."""
	
	if not os.path.exists(variant_path):
		print(f"variant path does not exist : {variant_path}")
		return {}
	
	try:
		df = pd.read_csv(variant_path, sep="\t", dtype=str)
	except (FileNotFoundError, pd.errors.EmptyDataError):
		return {}

	if not {"chr", "pos", "ref", "alt", "vaf"}.issubset(df.columns):
		return {}

	df = df.dropna(subset=["chr", "pos", "ref", "alt", "vaf"])
	variants = {}
	for _, r in df.iterrows():
		variant = f"{r['chr']}:{r['pos']}{r['ref']}>{r['alt']}"
		try:
			vaf = np.round(float(r["vaf"]), 5)
		except (ValueError, TypeError):
			continue
		variants[variant] = vaf
	return variants


def load_fusion_names(fusion_path):
	"""Load all fusions from *_fusion_check.tsv as a list of strings."""

	if not os.path.exists(fusion_path):
		print(f"fusion path does not exist  : {fusion_path}")
		return []

	try:
		df = pd.read_csv(fusion_path, sep=",", dtype=str)
	except (FileNotFoundError, pd.errors.EmptyDataError):
		return []

	fusions = []
	for val in df['fusion'].dropna():
		if "--" in str(val):
			fusions.append(str(val).strip())
	return fusions


def main():
	# Arguments
	parser = argparse.ArgumentParser(
		description=
		"Compare reference variants with sample variants. \n\n"
		"- Reference variants csv must have columns 'AF%' and 'VCF_description' - see reference_standards/rs_ctDNA.csv\n"
		"- Samples csv must have columns 'sample_id', 'worksheet' and 'run_id' - see reference_samples/ctdna.csv\n\n"
		"Sensitivity summary stats printed to terminal, full variants table saved to /output/<year>/<year>_<assay>_uom.csv",
		formatter_class=argparse.RawTextHelpFormatter
		)
	parser.add_argument("assay", choices=["ctdna", "dna", "rna"], help="Assay type, required")
	parser.add_argument("--config", default="config/config_wren.yaml", help="YAML config file")
	parser.add_argument("--rs", help="Reference variants CSV (rs_ctDNA.csv)")
	parser.add_argument("--samples", help="Samples CSV (reference_samples.csv)")
	parser.add_argument("--out", help="Output directory")
	args = parser.parse_args()

	with open(args.config, "r") as f:
		config = yaml.safe_load(f)

	year = pd.Timestamp.now().year

	# get the part of the config for the chosen assay
	assay_config = config.get("assays").get(args.assay)

	if args.rs is None:
		args.rs = assay_config.get("reference_standards")
	if args.samples is None:
		args.samples = assay_config.get("reference_samples")
	if args.out is None:
		output_dir = config.get("output_dir").format(year=year, assay=args.assay)
		# make year subdirectory if it doesn't exist
		os.makedirs(output_dir, exist_ok=True)
		args.out = os.path.join(output_dir)

	if not os.path.exists(args.config):
		return FileNotFoundError(f"Config file does not exist: {args.config}")
	if not os.path.exists(args.samples):
		return FileNotFoundError(f"Reference samples file does not exist: {args.samples}")
	if not os.path.exists(args.rs):
		return FileNotFoundError(f"Reference standards file does not exist: {args.rs}")

	# Load data
	ref_variants = load_reference_variants(args.rs)
	samples_df = pd.read_csv(args.samples)

	if not {"run_id", "sample_id"}.issubset(samples_df.columns):
		raise ValueError(f"{args.samples} must contain 'run_id' and 'sample_id' columns")

	worksheet_col = "worksheet" if "worksheet" in samples_df.columns else None

	results = []

	for _, srow in samples_df.iterrows():
		run_id = str(srow["run_id"])
		sample_id = str(srow["sample_id"])
		worksheet = srow[worksheet_col] if worksheet_col else ""
		
		fusion_path_list = []

		variant_path, fusion_path = build_file_path(assay_config, run_id, sample_id)
		sample_variants = load_sample_variants(variant_path)
		sample_fusions = load_fusion_names(fusion_path)

		for variant, ref_vaf in ref_variants.items():
			# Handle fusion differently
			if "--" in variant:
				variant_in_sample = any(part in f for f in sample_fusions for part in variant.split("--"))
				results.append({
					"run_id": run_id,
					"worksheet": worksheet,
					"sample_id": sample_id,
					"variant": variant,
					"reference_vaf": ref_vaf,
					"sample_vaf": None,
					"difference": None,
					"percent_difference": None,
					"variant_in_sample": variant_in_sample
				})
				continue
			
			# SNV/indel path
			sample_vaf = sample_variants.get(variant)
			if sample_vaf is not None and ref_vaf is not None:
				diff = np.round(sample_vaf - ref_vaf, 5)
				pct_diff = np.round((diff / ref_vaf * 100) if ref_vaf != 0 else 0, 3)
			else:
				diff = pct_diff = None

			variant_in_sample = any(variant in f for f in sample_variants)
			results.append({
				"run_id": run_id,
				"worksheet": worksheet,
				"sample_id": sample_id,
				"variant": variant,
				"reference_vaf": ref_vaf,
				"sample_vaf": sample_vaf,
				"difference": diff,
				"percent_difference": pct_diff,
				"variant_in_sample": variant_in_sample
			})

	out_df = pd.DataFrame(results)
	filename = f"{year}_{args.assay}_uom_results.csv"
	filepath = os.path.join(args.out, filename)
	out_df.to_csv(filepath, index=False)
	print(f"✅ Wrote {len(out_df)} rows to {filepath}")
	
	# Group by Assay and calculate stats
	out_df['Assay'] = args.assay
	summary = out_df.groupby('Assay').agg(
		Difference_Average=('difference', 'mean'),
		Difference_Maximum=('difference', 'max'),
		Difference_Minimum=('difference', 'min'),
		Pct_Difference_Average=('percent_difference', 'mean'),
		Pct_Difference_Maximum=('percent_difference', 'max'),
		Pct_Difference_Minimum=('percent_difference', 'min')
	).reset_index()

	# Optional: format numbers
	summary = summary.round({
		'Difference_Average': 5,
		'Difference_Maximum': 4,
		'Difference_Minimum': 4,
		'Pct_Difference_Average': 3,
		'Pct_Difference_Maximum': 2,
		'Pct_Difference_Minimum': 2
	})

	# Display the summary table
	print(summary)
	
	# Summary of boolean column
	sensitivity_summary = out_df['variant_in_sample'].value_counts(normalize=False)
	test = binomtest(
		sensitivity_summary.get(True, 0),
		sensitivity_summary.sum(),
		)
	print(f"Summary of Clopper-Pearson exact test:\n{test}")
	print(f"95% CI for Sensitivity: {test.proportion_ci(confidence_level=0.95, method='exact')}")

if __name__ == "__main__":
	main()
