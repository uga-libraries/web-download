# PDF Web Download

## Overview

Downloads individual PDF files from saved Archive-It crawls using the Archive-It File Type report.
Files are saved in folders named with the website (seed) url.
It can download PDFs from many websites, but only one Archive-It collection, at a time.

At UGA, PDFs are downloaded to provide access to Georgia government publications via the Digital Library of Georgia.


## Getting Started

### Dependencies

- [PySimpleGui](https://www.pysimplegui.org/en/latest/) - a Python library for creating user interfaces.
- [wget](https://www.gnu.org/software/wget/) - for downloading content using a URL. 

### Installation

To install wget in Windows:
1. Download a Windows Binary (<http://wget.addictivecode.org/FrequentlyAskedQuestions.html#download>).
2. Save the wget.exe file to a folder on your machine, such as Documents/wget.
3. Add the folder with wget.exe to your Path variable (under Settings, Environment Variables).
4. Test by opening a terminal window and typing `wget -h`. The wget options should appear.

You need administrative privileges on your machine for the script to be able to use wget. 
Additionally, Windows install instructions recommend saving to the System32 folder, 
which is already in the Path, but the Python script cannot access wget in this location.

To install wget in Linux or Mac: <https://www.gnu.org/software/wget/>

To use this script for other formats, update how missing file extensions are assigned in get_file_name().

## Script Arguments

In a terminal window, type ```python path/download_files.py```,
where "path" is the location of the download_files.py file on your computer.

This will open a GUI (graphical user interface) for users to enter two points of information:
* Folder with CSVs from Archive-It with the files to be downloaded.
* Title of the Archive-It collection that the files are part of.

## Workflow
Script Result: 
One folder for each website (seed), named with a modified version of the URL that removes characters not permitted in folder names.
Each folder contains all the PDFs from the CSV(s) for that website. 
PDFs are named with the last portion of their URL and a sequential number is added if another file of the same name has already been downloaded. 
If Archive-It detects a file is an exact duplicate, rather than a separate file with the same name, it will not be downloaded.
A Download Log (download_log.csv) is always created, which records if the correct number of PDFs were downloaded and if any errors were found.
If there were errors, an Error Log (error_log.csv) is created with the error information for each file with errors. 
The outputs of the script are all saved to the same folder as the Archive-It CSVs.

1. Crawl websites with the desired PDFs using Archive-It and save any test crawls.
   

2. For each crawl, download the PDF report from Archive-It
   
   a. Go to the "File Types" tab of the crawl report.
   
   b. Click "application/pdf" in the File Type table. Use the filter box to find it if the list is long.
   
   c. Click "Download File Type List".
   

3. Save all the CSVs to a single folder. They must all be from the same Archive-It collection but can be from many websites.
   

4. Review the CSVs and delete the row for any PDFs you do not wish to download.
   

5. Verify the Archive-It collection for these PDFs is in the ait_collections.py file.
   

6. Start the script by opening a terminal window and typing: `python path/download_files.py`, 
   where path is the location of the download_files.py file on your computer.
   

7. A window (the script GUI) will open. Provide the following input:
   
   a. The path to the folder with the CSVs created in step 3.
   
   b. The Archive-It collection that the CSVs are from.


8. If there are any issues with the provided input, a message will appear in the GUI and you can try again. 
   Otherwise, the GUI will show "Please wait while the PDFs you requested are downloaded..."


9. The script download progress (each seed) is displayed in the GUI. 
   When it is done, it will show "Downloading is complete."


10. Use the GUI to start another download or close the window to end the script.


11. Review the Download Log and Error Log (if created) for any problems with the download.
