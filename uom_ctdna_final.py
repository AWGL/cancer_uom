#!/usr/bin/env python3
import pandas as pd
import numpy as np
import os
import re
import argparse


def build_file_path(run_id, sample_id):
    """Return correct variant file path for given run_id and sample_id."""
    run_str = str(run_id)
    try:
        numeric_part = int(run_str[:4])
    except ValueError:
        numeric_part = 0

    if "240718" in run_str:
        base_dir = f"/data/output/results/{run_str}/tso500_ctdna/post_processing/results/database"
    elif numeric_part > 2404:
        base_dir = f"/data/output/results/{run_str}/tso500_ctdna/post_processing/database"
    else:
        year = 2000 + int(run_str[:2])
        month = run_str[2:4]
        base_dir = f"/data/output/archive_results/{year}/{month}/{run_str}/tso500_ctdna/post_processing/database"
    
    variant_file = f"{base_dir}/{sample_id}_variants.tsv"
    fusion_file = f"{base_dir}/{sample_id}_fusion_check.csv"
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
    except Exception:
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
        print("⚠️ Warning: no AF% column found, using 0 for all VAFs")
        df["af_dummy"] = 0
        af_col = "af_dummy"

    ref_dict = {}
    for _, row in df.iterrows():
        variant = normalize_variant(row[vcf_col])
        try:
            vaf = float(row[af_col])
        except Exception:
            vaf = 0.0
        if variant:
            ref_dict[variant] = vaf
    return ref_dict


def load_sample_variants(variant_path):
    """Load one *_variants.tsv file → dict {variant: sample_vaf}."""
    
    if os.path.exists(variant_path):
        print(f"variant path exists         : {variant_path}")
    else:
        print(f"variant path does not exist : {variant_path}")
        return {}
    
    try:
        df = pd.read_csv(variant_path, sep="\t", dtype=str)
    except Exception:
        return {}

    if not {"chr", "pos", "ref", "alt", "vaf"}.issubset(df.columns):
        return {}

    df = df.dropna(subset=["chr", "pos", "ref", "alt", "vaf"])
    variants = {}
    for _, r in df.iterrows():
        variant = f"{r['chr']}:{r['pos']}{r['ref']}>{r['alt']}"
        try:
            vaf = np.round(float(r["vaf"]) * 100, 3)
        except Exception:
            continue
        variants[variant] = vaf
    return variants


def load_fusion_names(fusion_path):
    """Load all fusions from *_fusion_check.tsv as a list of strings."""

    if os.path.exists(fusion_path):
        print(f"fusion path exists          : {fusion_path}")
    else:
        print(f"fusion path does not exist  : {fusion_path}")
        return []



    try:
        df = pd.read_csv(fusion_path, sep=",", dtype=str)
    except:
        return []

    fusions = []
    for val in df['fusion'].dropna():
        if "--" in str(val):
            fusions.append(str(val).strip())
    return fusions


def main():
    default_rs_filepath = "/home/transfer/Ant_Analysis/cancer_uom/reference_standards/rs_ctDNA.csv"
    default_samples_filepath = "/home/transfer/Ant_Analysis/cancer_uom/reference_samples.csv"

    parser = argparse.ArgumentParser(description="Compare reference variants with sample variants.")
    parser.add_argument("--rs", default=default_rs_filepath, help="Reference variants CSV (rs_ctDNA.csv)")
    parser.add_argument("--samples", default=default_samples_filepath, help="Samples CSV (reference_standard_file.csv)")
    parser.add_argument("--out", default="uom_ctdna_output.csv", help="Output CSV")
    args = parser.parse_args()

    try:
        os.path.exists(args.samples)
        print(f"Reference standards file exists         : {args.samples}")
    except Exception:
        print(f"Reference standards file does not exist : {args.samples}")

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

        variant_path, fusion_path = build_file_path(run_id, sample_id)
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
            if sample_vaf is not None:
                diff = np.round(sample_vaf - ref_vaf, 3)
                pct_diff = np.round((diff / ref_vaf * 100) if ref_vaf != 0 else 0)
                in_sample = True
            else:
                diff = pct_diff = None
                in_sample = False

            results.append({
                "run_id": run_id,
                "worksheet": worksheet,
                "sample_id": sample_id,
                "variant": variant,
                "reference_vaf": ref_vaf,
                "sample_vaf": sample_vaf,
                "difference": diff,
                "percent_difference": pct_diff,
                "variant_in_sample": in_sample
            })

    out_df = pd.DataFrame(results)
    out_df.to_csv(args.out, index=False)
    print(f"✅ Wrote {len(out_df)} rows to {args.out}")


if __name__ == "__main__":
    main()
