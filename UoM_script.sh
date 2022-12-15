#!/bin/bash

#SBATCH --partition=dev
#SBATCH --time=24:00:00
#SBATCH --mem=4G


#finding TSO500 DNA and RNA UoM sample files
#dna_rna_list=$(find /Output/results/*/Gathered_Results/ -type f \( -name "21M70050_variants.tsv" -o -name "22M12180_variants.tsv" -o -name "22M12181_variants.tsv" -o -name "22M06893_variants.tsv" -o -name "22M06894_variants.tsv" -o -name "22M06896_variants.tsv" -o -name "22M81471_fusion_check.csv" -o -name "22M81472_fusion_check.csv" -o -name "22M82583_fusion_check.csv" \))

#finding CRM UoM sample files
CRM_50=$(find /Output/results/*/NGHS-101X/21M70050 -name "*_21M70050_VariantReport.txt")
CRM_80=$(find /Output/results/*/NGHS-101X/22M12180 -name "*_22M12180_VariantReport.txt")
CRM_81=$(find /Output/results/*/NGHS-101X/22M12181 -name "*_22M12181_VariantReport.txt")
CRM_93=$(find /Output/results/*/NGHS-101X/22M06893 -name "*_22M06893_VariantReport.txt")
CRM_94=$(find /Output/results/*/NGHS-101X/22M06894 -name "*_22M06894_VariantReport.txt")
CRM_96=$(find /Output/results/*/NGHS-101X/22M06896 -name "*_22M06896_VariantReport.txt")

echo $dna_rna_list
echo $CRM_50
echo $CRM_80
echo $CRM_81
echo $CRM_93
echo $CRM_94
echo $CRM_96

