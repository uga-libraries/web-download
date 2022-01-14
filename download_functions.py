# Functions used for downloading individual PDFs from saved Archive-It crawls.
# Used by command line and graphical user interface versions of this script.

import csv
import os
import re
import subprocess


def download_files(input_directory, collection):
    """Gets the PDF URLs from each CSV in the input folder and downloads them to a folder named with the seed."""

    def get_download_urls():
        """Gets the PDF URLs from each CSV in the input folder and saves them to a dictionary.
        The dictionary keys are the seeds and values are a list of URLS for each seed."""

        # Dictionary for the results.
        download_urls_dict = {}

        # Reads every CSV in the CSV directory.
        for input_csv in os.listdir("."):
            with open(input_csv) as csvfile:
                data = csv.reader(csvfile)

                # Verifies the header has the expected values. If not, prints an error and starts the next CSV.
                header = next(data)
                if not header == ["url", "size", "is_duplicate", "seed"]:
                    print("This file is not formatted correctly and will be skipped:", input_csv)
                    continue

                # Adds the seed to the download_urls dictionary if it is not already present.
                # Adds the URL to the download_urls dictionary if it is not a duplicate in Archive-It (value of 1).
                for row in data:
                    url, size, is_duplicate, seed = row
                    if is_duplicate == "1":
                        continue
                    if seed in download_urls_dict:
                        download_urls_dict[seed].append(url)
                    else:
                        download_urls_dict[seed] = [url]

            return download_urls_dict

    def make_seed_folder():
        """Makes a folder for the seed and changes the current directory to that folder."""

        # Makes a version of the seed URL which can be used for a folder name.
        # Removes http:// or https://, / from the end if present, and replaces other / with _
        try:
            regex = re.match("https?://(.*?)/?$", seed)
            seed_folder = regex.group(1)
            seed_folder = seed_folder.replace("/", "_")
        except AttributeError:
            print("\nCannot make folder, URL pattern did not match:", seed)
            print("No files will be downloaded for this seed.")
            return

        # Makes a folder for the seed and makes it the current directory so wget can save the PDFs there.
        # If there is an error, no PDFs are downloaded for this seed.
        try:
            os.makedirs(os.path.join(input_directory, seed_folder))
            os.chdir(os.path.join(input_directory, seed_folder))
        except FileExistsError:
            print("\nCannot make folder, as it already exists:", seed_folder)
            print("No files will be downloaded for this seed.")
            return
        except OSError:
            print("\nCannot make a folder due to characters that are not permitted:", seed_folder)
            print("No files will be downloaded for this seed.")
            return

    def get_file_name(file_url):
        """Makes the filename based on the file URL."""

        # If the last part of the URL is download, gets the previous part of the URL and adds pdf extension.
        if file_url.endswith("download"):
            regex = re.match(".*/(.*)/download", file_url)
            name = regex.group(1) + ".pdf"
        # Otherwise, gets the last part of the URL and adds the pdf extension if it doesn't already have it.
        else:
            regex = re.match(".*/(.*)", file_url)
            if file_url.endswith((".pdf", ".PDF")):
                name = regex.group(1)
            elif file_url.endswith(("pdf", "PDF")):
                name = regex.group(1)[:-3] + ".pdf"
            else:
                name = regex.group(1) + ".pdf"

        # Checks if a file with this name has already been downloaded for this seed.
        # Generic names are common and a numeric extension is added to keep the files different.
        # If it is new, adds to the dictionary with a numeric extension of 1 (the next one to use).
        # If it has been used, adds the number to the filename and updates the number in the dictionary.
        if name in downloads:
            number = downloads[name]
            downloads[name] += 1
            name = name[:-4] + "_" + str(number) + ".pdf"
        else:
            downloads[name] = 1

        return name

    # Gets the PDF URLs from each CSV in the input folder that will be downloaded.
    to_download = get_download_urls()

    # For each seed, downloads the PDF for each URL in the list and saves it to a folder named with the seed.
    for seed in to_download.keys():

        # Makes a folder for the seed and makes that the current directory.
        make_seed_folder()

        # Starts a dictionary of downloaded PDFs to detect duplicate file names with this seed.
        downloads = {}

        # Saves each PDF to the seed folder.
        for url in to_download[seed]:

            # Makes the desired name for the file.
            filename = get_file_name(url)

            # Makes the URL for the file saved in Archive-It. The "3" is for the most recent capture.
            ait_url = f"https://wayback.archive-it.org/{collection}/3/{url}"

            # Saves the PDF to the seed's directory, named with the desired name.
            try:
                download_result = subprocess.run(f'wget -O "{filename}" "{ait_url}"', shell=True, stderr=subprocess.PIPE)
            except:
                print("Error with downloading the file:", url)
                return

            # Checks the wget output for any problem with the Archive-It connection.
            if "HTTP request sent, awaiting response... 200 OK" not in str(download_result):
                print("Connection error with Archive-It:", url)

            # Checks the wget output to make sure the entire file was downloaded.
            regex = re.match(".*saved \[([0-9]+)/([0-9]+)\]", str(download_result))
            if not regex.group(1) == regex.group(2):
                print("Download size is incomplete.", url)
