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

1. Error: cannot calculate seed folder name
   - Input CSV: seed urls that do not start with "http" or "https"
   - Expected result:
        - download_log.csv has "Could not make the seed folder: new URL pattern" in the "Errors" column
        - No seed folder is made and nothing is downloaded


2. Folder name variations (folder is new)
   - Input CSV: seed urls that begin with "http://" and "https://", that do and do not have / in the middle,
     and that do or do not have / at the end
   - Expected result:
      - Makes the seed folders with the correct names
      - Downloads everything in the report
      - download_log.csv has no errors


3. Folder of the name already exists
   - Input directory: a folder with a file type report, and folders for every seed in the report with a PDF
   - Expected result:
      - Downloads everything in the report to the correct seed folder
      - The original PDF is still in each folder
      - download_log.csv has no errors


4. Error: cannot make a folder by that name
   - Input CSV: seed urls that include characters that are not permitted by Windows (*, ?, :)
   - Expected result:
      - download_log.csv has "Couldn't make the seed folder: unpermitted character(s)." in the "Errors" column
      - No seed folder is made and nothing is downloaded

 
### get_file_name() 

1. Use entire URL
   - Input CSV: file URL does not contain a slash
   - Expected result:
      - Downloads everything in the report with the correct file name (entire URL)
      - download_log.csv has no errors


2. URL ends with /download
   - Input CSV: file URLs that end with /text/download
   - Expected result:
      - Downloads everything in the report with the correct file name ("text")
      - download_log.csv has no errors

   
3. Typical URL
   - Input CSV: file URL includes at least one slash from http:// and does not end with /download
   - Expected result:
      - Downloads everything in the report with the correct file name (whatever is after the last /)
      - download_log.csv has no errors

   
4. Adding PDF extension
   - Input CSV: includes at least one URL that will become a report named with each of the following patterns: 
     name.PDF, namepdf, namePDF, name.doc, name, name.pdf
   - Expected result:
      - Downloads everything in the report with the correct file extension (.pdf)
      - download_log.csv has no errors


5. Replacing illegal characters
   - Input CSV: includes at least one URL with each of the following characters in the part 
     which will become the report name: / \ * ? " < > |
   - Expected result:
      - Downloads everything in the report with the correct file name (characters replaced by underscores)
      - download_log.csv has no errors


5. Repeated file names (not duplicate files)
   - Input CSV: includes 2 or more URLs that will become the same report name and have 0 in the is duplicate column
   - Expected result:
      - Downloads the correct number of PDFs with the same name and adds the correct number to the end of each 
        (one has no number, and the rest have whole numbers starting with _1 before the file extension)
      - download_log.csv has no errors

### add_error()

This is tested by the error handling in download_files()

 
### download_files() 

Error handling to test if switch to unit tests for all functions:
- Test for get_download_urls() currently covers empty to_download dictionary.
- Test for make_seed_folder() currently covers AttributeError and OSError

The tests for the script overall cover the typical functioning of download_files().

1. Error: downloaded size wrong
   - TBD: unclear how to cause error, which compares the size expected and downloaded from the wget output
   - Expected result:
      - Downloads everything in the report
      - download_log.csv has "Download errors found" in the "Errors" column
      - error_log.csv has "Size downloaded is wrong"
   

2. Error: download size not calculated
   - TBD: unclear how to cause error, which is if the wget output is not the expected pattern
   - Expected result:
      - Downloads everything in the report
      - download_log.csv has "Download errors found" in the "Errors" column
      - errors_log.csv has "Can't calculate size downloaded"
   

3. Error: download URL wrong 
   - Input CSV: URLs that are not actually files in UGA's Archive-It account
   - Expected result:
       - Nothing is downloaded
       - download_log.csv has "Download errors found" in the "Errors" column
       - errors_log.csv has "Error when downloading, 8"

4. Error: wrong number of PDFs downloaded
   - TBD: unclear how to cause error, which compares the number of PDFs to the number in the dictionary
   - Expected result:
      - download_log.csv has "Errors found" in the "Correct Amount Downloaded?" column