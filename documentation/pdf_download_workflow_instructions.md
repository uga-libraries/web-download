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
It will download multiple PDFs if just the name is the same (e.g., report, minutes), and add a sequential number starting with 2.

The script will always create a log (download_log.csv) to document the process
and will also create an error log (error_log.csv) if there are any errors.

The script opens a simple GUI for entering the required input and displaying the progress of the script,
since it is used by individuals that do not regularly work with Python scripts.

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
      It will include the URL, Size, Is Duplicate (0 means no, 1 means yes), and seed ID.
   

3. Save all the CSVs to a single folder. 
   They must all be from the same Archive-It collection but can be from many websites.
   There should not be anything but the File Type CSVs in the folder.
   

4. Review the CSVs and delete the rows for any PDFs you do not wish to download.
   

5. If the Archive-It collection for these PDFs is not "Georgia Government Publications",
   verify the collection is in ait_collections.py file and update the default collection if desired.
   

6. Start the script by opening a terminal window and typing: "python path/download_files.py", 
   where path is the location of the download_files.py file on your computer.
   

7. A window (the script GUI) will open. Provide the following input:
   
   a. The path to the folder with the CSVs created in step 3. 
      This is also where the downloaded PDFs will be saved.
   
   b. The Archive-It collection that the CSVs are from (usually Georgia Government Publications).


8. If there are any issues with the provided input, a message will appear in the GUI and you can try again. 
   Otherwise, the GUI will show "Please wait while the PDFs you requested are downloaded..."


9. The script download progress (each seed) is displayed in the GUI.
   When it is done, it will show "Downloading is complete."


10. Use the GUI to start another download or close the window to end the script.


11. Review the Download Log and Error Log (if created) for any problems with the download.


12. Continue with MAGIL's established workflow to evaluate PDFs and transfer them to the DLG.