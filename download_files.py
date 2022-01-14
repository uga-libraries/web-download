"""
Download individual PDFs from crawled websites saved in Archive-It using the URLs from the File Types lists.
Designed for PDF-only crawls, where publications need to be saved and cataloged separately.

Prior to running the script, download the File Type List for PDFs from Archive-It for every crawl to include and
save the CSVs to a single folder. These files are the script input.

Dependency: wget https://www.gnu.org/software/wget/

Future development ideas:
    * Save all URLs to a CSV for staff review to remove unwanted things prior to download?
    * Adapt script for other formats besides PDF? Just need to change how files are renamed.
    * Need to be able to download from more than one collection at once?
    * Want any logging, summary statistics about how many were downloaded, and/or showing script progress?
"""

# Usage: python /path/download_files.py /path/input_directory archiveit_collection_id

# WARNING: THIS SCRIPT IS A PROOF OF CONCEPT AND HAS BEEN MINIMALLY TESTED

import os
import sys

import download_functions as fun

# Gets the path to the input folder from the script argument and makes it the current directory.
# If the path is missing or not valid, prints an error and quits the script.
try:
    input_directory = sys.argv[1]
    os.chdir(input_directory)
except (IndexError, FileNotFoundError, NotADirectoryError):
    print("The required argument input_directory is missing or not a valid directory.")
    print("Script usage: python /path/download_files.py /path/input_directory archiveit_collection_id")
    exit()

# Gets the Archive-It collection id from the script argument, which is used for making the Archive-It URL.
# If the id is missing, prints an error and quits the script.
try:
    collection = sys.argv[2]
except IndexError:
    print("The required argument Archive-It collection id is missing.")
    print("Script usage: python /path/download_files.py /path/input_directory archiveit_collection_id")
    exit()

# Gets the PDF URLs from each CSV in the input folder.
# Downloads each PDF to a folder named with the seed.
fun.download_files(input_directory, collection)
