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

import csv
import os
import re
import subprocess
import sys

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

# Gets the PDF URLs from each CSV in the input folder and saves them to a dictionary.
# The dictionary keys are the seeds and values are a list of URLS for each seed.
download_urls = {}
for input_csv in os.listdir("."):
    with open(input_csv) as csvfile:
        data = csv.reader(csvfile)

        # Verifies the header has the expected values. If not, prints an error and starts the next CSV.
        header = next(data)
        if not header == ["url", "size", "is_duplicate", "seed"]:
            print("This file is not formatted correctly and will be skipped:", input_csv)
            continue

        # Adds the seed to the download_urls dictionary if it is not already present.
        # Adds each URL to the download_urls dictionary if it is not a duplicate in Archive-It (value of 1 in the CSV).
        for row in data:
            url, size, is_duplicate, seed = row
            if is_duplicate == "1":
                continue
            if seed in download_urls:
                download_urls[seed].append(url)
            else:
                download_urls[seed] = [url]

# For each seed, downloads the PDF for each URL in the list and saves it to a folder named with the seed.
for seed in download_urls.keys():

    # Makes a version of the seed URL which can be used for a folder name.
    # Removes http:// or https:// from the beginning if present, / from the end if present, and replaces other / with _
    try:
        regex = re.match("https?://(.*?)/?$", seed)
        seed_folder = regex.group(1)
        seed_folder = seed_folder.replace("/", "_")
    except AttributeError:
        print("\nCannot make folder, URL pattern did not match:", seed)
        print("No files will be downloaded for this seed.")
        continue

    # Makes a folder for the seed and makes it the current directory so wget can save the PDFs there.
    # If there is an error, no PDFs are downloaded for this seed.
    try:
        os.makedirs(os.path.join(input_directory, seed_folder))
        os.chdir(os.path.join(input_directory, seed_folder))
    except FileExistsError:
        print("\nCannot make folder, as it already exists:", seed_folder)
        print("No files will be downloaded for this seed.")
        continue
    except OSError:
        print("\nCannot make a folder due to characters that are not permitted:", seed_folder)
        print("No files will be downloaded for this seed.")
        continue

    # Starts a dictionary of downloaded PDFs to detect duplicate file names.
    downloads = {}

    # Saves each PDF to the seed folder.
    for url in download_urls[seed]:

        # Makes the desired name for the file.
        # If the last part of the URL is download, gets the previous part of the URL instead and adds pdf extension.
        if url.endswith("download"):
            regex = re.match(".*/(.*)/download", url)
            filename = regex.group(1) + ".pdf"
        # Otherwise, gets the last part of the URL and adds the pdf extension if it doesn't already have it.
        else:
            regex = re.match(".*/(.*)", url)
            if url.endswith(".pdf") or url.endswith(".PDF"):
                filename = regex.group(1)
            elif url.endswith("pdf") or url.endswith("PDF"):
                filename = regex.group(1)[:-3] + ".pdf"
            else:
                filename = regex.group(1) + ".pdf"

        # Checks if a file with this name has already been downloaded for this seed.
        # Generic names are common and a numeric extension is added to keep the files different.
        # If it is new, adds to the dictionary with a numeric extension of 1 (the next one to use).
        # If it has been used, adds the numeric extension to the filename and updates the extension in the dictionary.
        if filename in downloads:
            number = downloads[filename]
            downloads[filename] += 1
            filename = filename[:-4] + "_" + str(number) + ".pdf"
        else:
            downloads[filename] = 1

        # Makes the URL for the file saved in Archive-It. The "3" is for the most recent capture.
        archiveit_url = f"https://wayback.archive-it.org/{collection}/3/{url}"

        # Saves the PDF to the seed's directory, named with the desired name.
        try:
            download_result = subprocess.run(f'wget -O "{filename}" "{archiveit_url}"',
                                             shell=True, stderr=subprocess.PIPE)
        except:
            print("Error with downloading the file:", url)

        # Checks the wget output for any problem with the Archive-It connection.
        if "HTTP request sent, awaiting response... 200 OK" not in str(download_result):
            print("Connection error with Archive-It:", url)

        # Checks the wget output to make sure the entire file was downloaded.
        regex = re.match(".*saved \[([0-9]+)/([0-9]+)\]", str(download_result))
        if not regex.group(1) == regex.group(2):
            print("Download size is incomplete.", url)

        # # ALTERNATIVE: download from the live site again so don't have to save the crawl.
        # subprocess.run(f'wget -O "{filename}" "{url}"', shell=True)
