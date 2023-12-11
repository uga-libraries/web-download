# Testing the Script, December 2023

## Overview

Use these instructions to test that the script is working correctly.

## Script Overall
Select a few CSVs to use for regular testing.

Also test the inputs:
- input_folder blank ["Folder with CSVs can't be blank"]
- input_folder not a valid path ["Folder with CSVs path is not correct."]
- ait_collection blank ["Archive-It Collection cannot be blank"]
- ait_collection not expected value ["Archive-It Collection is not one of the permitted values"]

Using Georgia Politics instead of GGP to get more variations. Now that GGP has crawled more, replace with theirs.

Testing (CSVs) - Georgia Politics (checked all reports for non-social media and no /download) 

- 940298: one seed, no duplicates 
- 1010708: two seeds, duplicate, 2 files with same name 
- 1436714: one seed with middle slash, no duplicates [removed – seed fine, URLS not] 

 
Testing (expected results) 

- gagop.org 
   - GAGOP-State-Party-Rules-Adoped-6-16-19.pdf 
   - GAGOP-State-Party-Rules-Adoped-6-16-19_1.pdf 
- votedeborahgonzalez.com 
   - SB336-MEMO-GOV.pdf 
- www.georgiademocrat.org 
   - DPGcharter1.pdf 
   - VotingGuide_korean.pdf 

## Specific Functions

These tests cover variations and error handling for individual functions, 
beyond what the tests for the script overall accomplish.

Each test includes what to use as the input directory or Archive-It file type CSV 
and what the results should be after using that as input in the download GUI.

### get_download_urls()

1. Input folder is empty
   - Input directory: Make any empty folder  
   - Expected result: GUI has "No URLs were found to be downloaded."
   

2. Input folder has unexpected (not CSV) content
   - Input directory: a folder that contains another folder, a text file, and a file type report
   - Expected result:
        - It does nothing (not in logs, nothing downloaded, no error messages) for the folder or text file
        - Downloads everything in the Archive-It CSV, and the log has no errors


3. Input folder has unexpected CSV
   - Input directory: a folder that contains a CSV file that is not a file type report, and a CSV file that is
   - Expected result:
        - GUI has "This CSV is not formatted correctly and will be skipped" for the non-file type report
        - Downloads everything in the Archive-It CSV, and the log has no errors
   
 
4. Duplicate PDFs
    - Input CSV: a file type report that includes "1" in the is_duplicate column for some PDFs
    - Expected result: Downloads everything in the report except for the PDFs with "1", and the log has no errors


5. PDF per seed variation
    - Input CSV: a file type report with 1 PDF per seed and another with multiple PDFs per seed
    - Expected result: Downloads everything in both reports, and the log has no errors
    
### make_seed_folder() 

1. Seed regex failure: logs and doesn’t to download [doesn't start with http, error in GUI is Could not make the seed folder: new URL pattern]


2. Folder already exists: adds PDFs to it [make folder before running the script] 


3. Characters that aren’t permitted: logs and doesn’t download [slashes are replaced, so what else causes a problem? Error in GUI is Couldn't make the seed folder: unpermitted character(s).]

 
### get_file_name() 

1. Doesn’t have a slash in it at all: uses whole URL
2. Ends in doc.pdf/download: uses doc.pdf
3. Ends in /report_download.pdf: uses report_download.pdf
4. Ends in /gov_doc.pdf: uses gov_doc.pdf
5. Convert name.PDF to name.pdf
6. Convert namepdf to name.pdf
7. Convert namePDF to name.pdf
8. Convert name.doc to name.doc.pdf
9. Convert name to name.pdf
10. Convert name*name.pdf to name_name.pdf
11. Add number to repeated file name (when not a duplicate file)

### add_error()

This is tested by the error handling in download_files()

 
### download_files() 

Error handling to test if switch to unit tests for all functions:
- Test for get_download_urls() currently covers empty to_download dictionary.
- Test for make_seed_folder() currently covers AttributeError and OSError

wget errors 
[wget exit codes](https://www.man7.org/linux/man-pages/man1/wget.1.html)
1. Downloaded size doesn’t match [Error Size downloaded is wrong, download log has "Download errors found"] 
2. Downloaded size cannot be calculated [Can't calculate size downloaded, download log has "Download errors found"] 
3. Some other error [Error while downloading] - do by giving collection ID that isn't correct: URL is wrong so logged as error 8

4. Wrong number of PDFs downloaded: file_match in download log has "Errors found"