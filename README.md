# PDF Web Download
Downloads individual PDF files from saved Archive-It crawls to provide access to Georgia Government Publications via the Digital Library of Georgia.
To use this script for other formats, update how missing file extensions are assigned in get_file_name().

## Script Usage
```python /path/download_files.py```

Running the script will open a GUI (graphical user interface) for users to enter two points of information:
* Folder with CSVs from Archive-It with the files to be downloaded.
* Title of the Archive-It collection that the files are part of.

## Script Result
One folder for each website (seed), named with a modified version of the URL that removes characters not permitted in folder names.

Each folder contains all the PDFs from the CSV(s) for that website. PDFs are named with the last portion of their URL and a sequential number is added if another file of the same name has already been downloaded. If Archive-It detects a file is an exact duplicate, rather than a separate file with the same name, it will not be downloaded.

A Download Log (download_log.csv) is always created, which records if the correct number of PDFs were downloaded and if any errors were found.

If there were errors, an Error Log (error_log.csv) is created with the error information for each file with errors. 

The outputs of the script are all saved to the same folder as the Archive-It CSVs.

## Dependencies
PySimpleGui, a Python library for creating GUIs. To install, in a terminal type: `pip install PySimpleGUI`

wget, for downloading content using a URL. To install in Windows 11:
1. Download a Windows Binary (<http://wget.addictivecode.org/FrequentlyAskedQuestions.html#download>).
2. Save the wget.exe file to  C:/Windows/System32/WindowsPowerShell/v1.0 (your version number may vary).
3. Test by opening a terminal window and typing wget -h. The options should appear.

To install wget in Linux or Mac: <https://www.gnu.org/software/wget/>

## Workflow
1. Crawl websites with the desired PDFs using Archive-It and save any test crawls.
   

2. For each crawl, download the PDF report from Archive-It
   
   a. Go to the "File Types" tab of the crawl report.
   
   b. Click "application/pdf" in the File Type table. Use the filter box to find it if the list is long.
   
   c. Click "Download File Type List".
   

3. Save all the CSVs to a single folder. They must all be from the same Archive-It collection but can be from many websites.
   

4. Review the CSVs and delete the row for any PDFs you do not wish to download.
   

5. Verify the Archive-It collection for these PDFs is in the ait_collections.py file.
   

6. Start the script by opening a terminal window and typing: `python path/download_files.py`, where path is the location of the download_files.py file on your computer.
   

7. A window (the script GUI) will open. Provide the following input:
   
   a. The path to the folder with the CSVs created in step 3.
   
   b. The Archive-It collection that the CSVs are from.


8. If there are any issues with the provided input, a message will appear in the GUI and you can try again. Otherwise, the GUI will show "Please wait while the PDFs you requested are downloaded..."


9. The script download progress (each seed) is displayed in the GUI. When it is done, it will show "Downloading is complete."


10. Use the GUI to start another download or close the window to end the script.


11. Review the Download Log and Error Log (if created) for any problems with the download.