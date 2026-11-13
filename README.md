# Cancer Uncertainty of Measurement
Uncertainty of measurement calculations for cancer NGS assays

### Run
   ```
  python <script_name>
   ```

## Instructions for yearly update
   For ctDNA, run 'python uom_ctdna.py -h' for instructions

## Sera seq control variant list
   https://www.seracare.com/globalassets/seracare-resources/tpr-0710-0672-seraseq-ctdna-complete-rm-af0.5-10690580.pdf

   In practise, the ERBB2 variant 17:37880986A>ACGTGATGGCCTC is called as 17:37880981A>AGCATACGTGATG

### Find which samples correspond to which reference standard in shire 
   HD728, HD730 or RNA

### Hardcoded filepaths
   Currently, filepaths for the config file, reference files and worksheet are hardcoded into the code. Ensure these filepaths are correct for your local file locations.
   
### Reference standard (RS) and uncertainty of measurement sample run files are not in the same build 
   As of Dec 2022, RS files are in build 38 and the uncertainty of measurement sample files are in build 37. tso500_automation_reference_controls file has the conversion.
  
  The base changes recorded may differ between the reference standard and the sample run files. E.g. position_del in RS may be position_basechanges in sample.
  
### Splitting sample path to get sample ID and run ID
  Ensure you're splitting the path at the correct places, the sample and run IDs are not always at the same place in the paths.
  
### Inserting worksheet ID into output
  Check in the sample sheet manually that where you 'cut' is the correct column that will extract the worksheet ID.
  These differ in TSO500 and CRM sample sheets