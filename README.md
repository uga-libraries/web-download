# PDF Web Download

## Overview

Downloads individual PDF files from saved Archive-It crawls using the Archive-It File Type report.
Files are saved in folders named with the website (seed) url.
It can download PDFs from many websites, but only one Archive-It collection, at a time.

At UGA, PDFs are downloaded to provide access to Georgia government publications via the Digital Library of Georgia.


## Getting Started

### Dependencies

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

Verify the information in ait_collections.py is correct.
It contains the default Archive-It collection for the download,
as well as a list of all Archive-It collections for UGA.

To use this script for other formats, update how missing file extensions are assigned in get_file_name().

### Script Arguments
* input_folder (required): Folder with CSVs from Archive-It with the files to be downloaded.
* ait_collection (optional): Title of the Archive-It collection that the files are part of, 
  if not Georgia Government Publications (the default value for ait_collection)

Put quotes around either script argument if it has spaces

Example for GGP collection:  
python C:/user/scripts/download_files.py "C:/user/GGP CSVs"

Example for Activists and Advocates collection:  
python C:/user/scripts/download_files.py C:/user/csv "Activist and Advocates"

Terminal Tips:

* Drag a file or folder onto the terminal window to make its path appear.
* Put quotes around any paths that have spaces.
* Make sure there is a space between each component of the command.
* Use the up arrow key to see earlier commands you typed, e.g., if you need to fix a typo or run something again.

### Testing

Use the [Testing Instructions](documentation/testing_instructions.md) as a guide for designing tests
or as a basis for creating unit tests for the functions.

## Workflow

Instructions for the entire workflow involving this script,
including preparing the list of PDFs from Archive-It and working with the script interface:
[PDF Download Workflow Instructions](documentation/pdf_download_workflow_instructions.md)

## Author

Adriane Hanson, Head of Digital Stewardship, UGA Libraries

## History

This script was developed for Sarah Causey in MAGIL in 2022, after they transitioned from HTTrack to Archive-It for web crawling.
HTTrack automatically downloaded individual files, including PDFs, so that they could be added to DLG when warranted.
Archive-It downloads the entire website as a WARC, so we needed a different way to extract the PDF files.
