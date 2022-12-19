# Cancer Uncertainty of Measurement
Uncertainty of measurement calculations for cancer NGS assays


## Instructions for yearly update

### Find which samples correspond to which reference standard in shire 

### Reference standard (RS) and uncertainty of measurement sample run files are not in the same build 
   As of Dec 2022, RS files are in build 38 and the uncertainty of measurement sample files are in build 37. tso500_automation_reference_controls file has the conversion.
   
### Listing all uncertainty of measurement files for this years corresponding sample IDs:
  In section that states 'Get all files into a list' replace sample IDs in _path/sample_id_variants.tsv_ .

### Ensuring that variant position formatting are the same in both the sample and reference standard (RS) files
  Ensure that the variant position contains the chromosome, position on the chromosome and base change in the same formats. chr:positionbase>base. For RNA this is just the fusion, however fusions may be formatted differently, manually check and change reference standard format to match.
  
  The base changes recorded may differ between the reference standard and the sample run files. E.g. position_del in RS may be position_basechanges in sample.
  
### Splitting sample path to get sample ID and run ID
  Ensure you're splitting the path at the correct places, the sample and run IDs are not always at the same place in the paths.
  
### Inserting worksheet ID into output
  Check in the sample sheet manually that where you 'cut' is the correct column that will extract the worksheet ID.
  These differ in TSO500 and CRM sample sheets.
