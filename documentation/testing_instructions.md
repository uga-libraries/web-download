# Testing the Script, April 2024

## Overview

Use these instructions to test that the script is working correctly.


## Script Overall

This tests that the script is working as expected with typical input.

Since the script is capturing PDFs from the most recent crawl of a website,
the same CSV cannot be used every time.

1. Download 3-5 file type CSVs from Archive-It.
2. Delete most of the rows from the reports for faster testing,
   leaving some seeds with multiple PDFs, some duplicates, some where the last part of the path is download, and some repeated names.
3. Run the script and verify what prints in the terminal:
    - "Correct script input was provided. Please wait while the PDFs you requested are downloaded."
    - "Starting downloads for the next seed: SEED NAME" (for each seed)  
    - "Downloading is complete. Downloaded files are in the folder provided as the script argument. 
       Check the logs in the folder with the downloaded files for errors."
4. Check the results
    - All seed folders were made and have the expected names
    - All PDFs were downloaded and have the expected names
    - download_log.csv has all seed folders and no errors
    - errors_log.csv was not made


## Specific Functions

These tests cover unusual variations and error handling for individual functions, 
beyond what the tests for the script overall accomplish.
They are only needed if that aspect of the script is heavily edited or causing the script to malfunction.

If the frequency of script changes increases, these will be converted to unit tests.


### check_arguments()

For each scenario, type the provided text in the terminal (replacing PATH with the location on your computer)
and verify that the script stops running and the message displayed in the terminal window makes sense.

1. Missing argument: python PATH/download.py

2. CSV path error: python PATH/download.py C:/path/error

3. Collection error: python PATH/download.py PATH Collection_Error

4. Too many arguments: python PATH/download.py PATH Business Error   

5. Mix of errors: python PATH/download.py C:/path/error Collection_Error Error


### download_seed()

Errors related to the seed name are tested in make_seed_folder()

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
       - File downloaded has a size 0 and cannot be opened (TBD: do not download these)
       - download_log.csv has "Download errors found" in the "Errors" column
       - errors_log.csv has "Error when downloading, 8"

4. Error: wrong number of PDFs downloaded
   - TBD: can't make this happen until don't delete files from URL errors
   - Expected result:
      - download_log.csv has "Errors found" in the "Correct Amount Downloaded?" column


### error_log()

No variations to test, beyond results of error handling in download_seed().


### get_download_urls()

Input folder is the folder with the Archive-IT PDF CSVs.
For each scenario, run the script with python PATH/download_files.pdf "PATH/input folder"

1. Input folder is empty
   - Input directory: Make any empty folder  
   - Expected result: terminal has "No URLs were found to be downloaded. Script will end."
   

2. Input folder has unexpected (not CSV) content
   - Input directory: a folder that contains another folder, a text file, and a file type report
   - Expected result:
        - It does nothing (not in logs, nothing downloaded, no error messages) for the folder or text file
        - Downloads everything in the Archive-It CSV, and the log has no errors


3. Input folder has unexpected CSV
   - Input directory: a folder that contains a CSV file that is not a file type report, and a CSV file that is
   - Expected result:
        - Terminal has "This CSV is not formatted correctly and will be skipped" for the non-file type report
        - Downloads everything in the Archive-It CSV, and the log has no errors
   
 
### get_file_name() 

These are potential variations we haven't necessarily seen in real data yet.
For testing, you may need to make a fake CSV with these variations and print the result of the function
rather than running the entire script.

1. Use entire URL
   - Input CSV: file URL does not contain a slash
   - Expected result:
      - Downloads everything in the report with the correct file name (entire URL)
      - download_log.csv has no errors


2. Adding PDF extension
   - Input CSV: includes at least one URL that will become a report named with each of the following patterns: 
     name.PDF, namepdf, namePDF, name.doc, name, name.pdf
   - Expected result:
      - Downloads everything in the report with the correct file extension (.pdf)
      - download_log.csv has no errors


3. Replacing illegal characters
   - Input CSV: includes at least one URL with each of the following characters in the part 
     which will become the report name: / \ * ? " < > |
   - Expected result:
      - Downloads everything in the report with the correct file name (characters replaced by underscores)
      - download_log.csv has no errors


### log()

No variations to test, beyond results of the script overall and error handling in download_seed().


### make_seed_folder() 

These are potential variations we haven't necessarily seen in real data yet.
For testing, you may need to make a fake CSV with these variations and print the result of the function
rather than running the entire script.

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


3. Error: cannot make a folder by that name
   - Input CSV: seed urls that include characters that are not permitted by Windows (*, ?, :)
   - Expected result:
      - download_log.csv has "Couldn't make the seed folder: unpermitted character(s)." in the "Errors" column
      - No seed folder is made and nothing is downloaded
