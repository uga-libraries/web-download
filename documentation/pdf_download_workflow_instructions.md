# PDF Download Workflow, January 2022

## Purpose

Download individuals PDFs from Archive-It crawls to be added to the GGP collection. 
These PDFs are for access via the DLG and will not be added individually into ARCHive. 
Instead, the WARC for the entire site crawl will be preserved in ARCHive. 
This workflow can be expanded to include other formats when government publications are no longer exclusively PDFs. 

## Overview

The script downloads PDFs from Archive-It crawls. 
The PDFs are saved to folders named with the website URL (modified to remove illegal characters),
and the PDFs are named with the last portion of their URL.
It will not download multiple copies of a PDF if Archive-It detects it is a duplicate.
It will download multiple PDFs if just the name is the same (e.g., report, minutes), and add a sequential number starting with 1.

The script will always create a log (download_log.csv) to document the process
and will also create an error log (error_log.csv) if there are any errors.

## Responsibility

MAGIL faculty and staff run the workflow. 
The Head of Digital Stewardship maintains and improves the script at the request of MAGIL.

## Workflow

1. Crawl websites with the desired PDFs using Archive-It and save if they are test crawls. 
   The crawl may be PDF-only or may be a full crawl of the site.
   

2. For each crawl, download the PDF report from Archive-It:
   
   a. Go to the "File Types" tab of the crawl report.
   
   b. Click "application/pdf" in the File Type table. Use the filter box to find it if the list is long.
   
   c. Click "Download File Type List", which downloads a CSV with the PDF metadata. 
      It will include the PDF URL, Size, Is Duplicate (0 means no, 1 means yes), and seed URL.
   

3. Save all the CSVs to a single folder. 
   They must all be from the same Archive-It collection but can be from many websites (seeds).
   There should not be anything but the File Type CSVs in the folder.
   

4. Review the CSVs and delete the rows for any PDFs you do not wish to download.
   

5. Start the script by opening a terminal window and typing:
    
       python PATH/download_files.py PATH/CSVS

   * In place of "PATH", put the absolute path to that file or folder on your computer.
   * In place of "CSVS", put the name of the folder with Archive-It PDF File Type CSVs.
   * If the Archive-It collection is not "Georgia Government Publications", type the collection name after PATH/CSVS

   
6. The script checks PATH/CSVS and the optional collection and shows the result in the terminal.
   
   a. If everything is correct, you'll see "Correct script input was provided..." and the download will begin.

   b. If there is an error, you'll see a description of the issue and the script will stop. 
      Start the script again with the correct information, using guidance in step 5.


7. The script download progress (when it starts downloads for each website/seed) is displayed in the terminal.
   When it is done, it will show "Downloading is complete..."


8. Review the Download Log and Error Log (if created) for any problems with the download.
   These logs, and the downloaded files, are in the PATH/CSVS folder.


9. Continue with MAGIL's established workflow to evaluate PDFs and transfer them to the DLG.