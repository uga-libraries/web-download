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

Verify the information in ait_collections.py is correct.
It contains the default Archive-It collection for the download,
as well as a list of all Archive-It collections for UGA.

To use this script for other formats, update how missing file extensions are assigned in get_file_name().

## Script Arguments

In a terminal window, type ```python path/download_files.py```,
where "path" is the location of the download_files.py file on your computer.

This will open a GUI (graphical user interface) for users to enter two points of information:
* Folder with CSVs from Archive-It with the files to be downloaded.
* Title of the Archive-It collection that the files are part of.

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
