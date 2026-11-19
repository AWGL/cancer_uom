# Cancer Uncertainty of Measurement
Uncertainty of measurement calculations for cancer NGS assays

### Setup
   Log into wren. If you have SSH set up you can clone the repo as follows:
   ```
   git clone git@github.com:AWGL/cancer_uom.git
   cd cancer_uom
   ```
   Otherwise use:
   ```
   cd /home/transfer/Ant_Analysis/cancer_uom
   ```
   Activate the conda environment
   ```
   conda activate somatic_enrichment_nextflow
   ```

### Run
   While in the repository directory, run as follows:
   ```
   python uom.py <assay>
   ```
   Where assay is one of ctdna, dna, rna

### Instructions for yearly update
   Run the following for instructions
   ```
   python uom.py -h
   ```

### Sera seq ctDNA control variant list
   - See reference table here https://www.seracare.com/globalassets/seracare-resources/tpr-0710-0672-seraseq-ctdna-complete-rm-af0.5-10690580.pdf
   - In practise, the ERBB2 variant 17:37880986A>ACGTGATGGCCTC is called as 17:37880981A>AGCATACGTGATG. The ctDNA reference standard has been changed to reflect this.
   - BRCA1 chr17:41245586CT>C is sometimes called as a variant, sometimes filtered out as noise as it falls in a 'noisy' region. Scientists perform a manual check for this in any panels with BRCA1. So that may be artificially inflating the 'False' count - consider reporting without this variant.

### Find which samples correspond to which reference standard in shire 
   HD728, HD730 or RNA

### Filepaths
   - By default, filepaths for the reference standards, reference samples and output are set in config_wren.yaml
   - These can be overriden using the relevant optional argument (see help)
   
### Reference standard (RS) and uncertainty of measurement sample run files are not in the same build 
   - As of Dec 2022, RS files are in build 38 and the uncertainty of measurement sample files are in build 37. tso500_automation_reference_controls file has the conversion.
   - The base changes recorded may differ between the reference standard and the sample run files. E.g. position_del in RS may be position_basechanges in sample.
  
### Troubleshooting missing paths
   - Check the information in the reference samples file is correct.
   - ```ls``` the filepath printed to the terminal. If no file is found:
      - find the true path and add a corresponding entry to the relevant config section
      - and add an elif rule to the build_file_path function following the existing assay_config.get() convention 
  
### Inserting worksheet ID into output
  Check in the sample sheet manually that where you 'cut' is the correct column that will extract the worksheet ID.