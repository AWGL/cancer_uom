# Cancer Uncertainty of Measurement
Uncertainty of measurement calculations for cancer NGS assays


### Instructions for yearly update:
#### Listing all uncertainty of measurement files for this years corresponding sample IDs:
  In section that states 'Get all files into a list' replace sample IDs in _path/sample_id_variants.tsv_ 

#### Ensuring that variant position formatting are the same in both the sample and reference standard (RS) files
  Ensure that the variant position contains the chromosome, position on the chromosome and base change in the same formats
  The base changes recorded may differ between the reference standard and the sample run files. E.g. position_del in RS may be position_basechanges in sample 
  
#### Splitting sample path to get sample ID and run ID
  Ensure you're splitting the path at the correct places, the sample and run IDs are not always at the same place in the paths.
  
#### Inserting worksheet ID into output
  Check in the sample sheet manually that where you 'cut' is the correct column that will extract the worksheet ID
  These differ between TSO500 and CRM sample sheets
