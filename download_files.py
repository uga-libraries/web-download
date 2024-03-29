"""Download individual PDF files from saved Archive-It crawls.

At UGA, this script is used by MAGIL to provide access to Georgia Government Publications
via the Digital Library of Georgia.
It includes a GUI for entering script parameters and viewing script progress.

Parameters:
    input_folder : path to the folder with Archive-It CSVs files listing the PDF URls
    ait_collection : Archive-It collection the websites are part of (all must be in the same one)

Returns:
    One folder for each website (seed), with the PDFs from that seed.
    A download_log.csv file with if the correct number of PDFs were downloaded and a summary of any other error.
    An error_log.csv file with details about each wget error, if there were any errors.
"""

import csv
import gc
import os
import re
import subprocess
import sys
import threading

import PySimpleGUI as sg
import ait_collections as ait

# Threading prevents the GUI from saying it is unresponsive when a process is taking a while.
SCRIPT_THREAD = '-SCRIPT_THREAD-'


def download_files(input_directory, collection, window):
    """Get the PDF URLs from each CSV in the input folder and downloads them to a folder named with the seed url.

    Parameters:
        input_directory : path to the folder with Archive-It CSV files listing the PDF URLs
        collection : Archive-It collection that all CSVs are part of
        window : GUI data
    """

    def get_download_urls():
        """Get the PDF URLs from each CSV in the input folder and save them to a dictionary.

        Returns:
            A dictionary with seed (website) as the key and a list of PDF URLs for each seed as the value.
        """

        # Makes a dictionary for the results.
        download_urls_dict = {}

        # Finds and reads every CSV in the input directory.
        for input_csv in os.listdir("."):

            # Skips files that aren't CSVs and skips folders.
            if not input_csv.endswith(".csv") or os.path.isdir(input_csv):
                continue

            # Reads the CSV.
            with open(input_csv) as csvfile:
                data = csv.reader(csvfile)

                # Verifies the header has the expected values.
                # If not, prints an error and starts the next CSV.
                header = next(data)
                if not header == ["url", "size", "is_duplicate", "seed"]:
                    print("This CSV is not formatted correctly and will be skipped:", input_csv)
                    continue

                # Updates the download urls dictionary with data about each PDF URL.
                for row in data:
                    url, size, is_duplicate, seed = row
                    # Does not add the PDF URL to the dictionary if it is a duplicate (value of 1).
                    if is_duplicate == "1":
                        continue
                    # Adds the PDF URL if the seed is already in the dictionary.
                    if seed in download_urls_dict:
                        download_urls_dict[seed].append(url)
                    # Adds the seed URL and PDF URL to the dictionary if the seed isn't already present.
                    else:
                        download_urls_dict[seed] = [url]

        return download_urls_dict

    def make_seed_folder(seed):
        """Make a folder for the seed (website) and change the current directory to that folder.

        Parameters:
            seed : URL for the seed (website)

        Returns:
            The seed (website) folder name, which is the URL without http(s):// and slashes replaced by underscores.
        """

        # Prints the seed name to the GUI to show the script's progress.
        print("Starting next seed:", seed)

        # Makes a version of the seed URL which can be used for a folder name.
        # Removes http:// or https://, removes / from the end if present, and replaces any other / with _
        try:
            regex = re.match("https?://(.*?)/?$", seed)
            seed_folder = regex.group(1)
            seed_folder = seed_folder.replace("/", "_")
        except AttributeError:
            raise AttributeError

        # Makes a folder for the seed, if it doesn't exist,
        # and makes it the current directory to save the PDFs there.
        # If there is an error, no PDFs are downloaded for this seed.
        try:
            os.makedirs(os.path.join(input_directory, seed_folder))
            os.chdir(os.path.join(input_directory, seed_folder))
        except FileExistsError:
            os.chdir(os.path.join(input_directory, seed_folder))
        except OSError:
            raise OSError

        # Returns the seed folder name, which is needed later to check for completeness.
        return seed_folder

    def get_file_name(file_url):
        """Construct the file name based on the file URL.

        Parameters:
            file_url : URL for the PDF to be downloaded

        Returns:
            File name
        """

        # Selects the part of the URL to use for the name. URL parts are the texts divided by the slashes.
        #   -If the URL doesn't have multiple parts (unlikely), the whole URL is the name.
        #   -If the last part of the URL is "download", the previous part of the URL is the name.
        #   -Otherwise, the last part of the URL is the name.
        if "/" not in file_url:
            name = file_url
        elif file_url.endswith("/download"):
            regex = re.match(".*/(.*)/download", file_url)
            name = regex.group(1)
        else:
            regex = re.match(".*/(.*)", file_url)
            name = regex.group(1)

        # Adds a ".pdf" file extension, if it doesn't have one.
        #    - Some extensions are all caps (.PDF)
        #    - Some have pdf or PDF but not the preceding period
        #    - Some do not have a file extension
        # Making all extensions lowercase so case-insensitive systems don't think it is a duplicate.
        if not name.endswith(".pdf"):
            if name.endswith(".PDF"):
                name = name[:-4] + ".pdf"
            elif name.endswith(("pdf", "PDF")):
                name = name[:-3] + ".pdf"
            else:
                name = name + ".pdf"

        # Replaces any characters which Windows does not allow in a filename with an underscore.
        for character in ('/', '\\', '*', '?', '"', '<', '>', '|'):
            if character in name:
                name = name.replace(character, "_")

        # Adds a numerical extension to the file name if there is already another file of that name for this seed,
        # since generic names like report are common for different files,
        # and updates a dictionary that tracks the next sequential number to use for a file of that name.
        if name in downloads:
            number = downloads[name]
            downloads[name] += 1
            name = name[:-4] + "_" + str(number) + ".pdf"
        # If this is the first time the file name is used, the next instance of the name will have an extension of 1.
        else:
            downloads[name] = 1

        return name

    def add_error(message, output):
        """Make an error log, if one doesn't already exists, and add the data for this error to it.

        Parameters:
            message : standard text to include in the log about the error
            output : output from wget, which generated the error
        """

        # Constructs the path to the error_log.csv, in the same folder as the Archive-It CSVs.
        error_log_path = os.path.join(input_directory, "error_log.csv")

        # Tests if a header row is needed, which is if the log does not already exists.
        if os.path.exists(error_log_path):
            add_header = False
        else:
            add_header = True

        # Opens or makes the error log, adds a header if needed, and adds the error.
        with open(error_log_path, "a", newline="") as error_log:
            error_log_write = csv.writer(error_log)
            if add_header:
                error_log_write.writerow(["Error", "WGET Command", "Return Code", "STDERR"])
            error_log_write.writerow([message, output.args, output.returncode,
                                      output.stderr.decode('utf-8')])

    # Gets a dictionary of the PDF URLs from each CSV in the input folder that will be downloaded.
    to_download = get_download_urls()

    # If no URLs were located, prints that the script has completed in the GUI dialogue box,
    # ends the thread, and quits the script.
    if to_download == {}:
        print("\nNo URLs were found to be downloaded.")
        window.Refresh()
        window.write_event_value('-SCRIPT_THREAD-', (threading.current_thread().name,))
        return

    # Makes a log to save the success of each seed download.
    download_log = open(os.path.join(input_directory, "download_log.csv"), "a", newline="")
    download_log_write = csv.writer(download_log)
    download_log_write.writerow(["Seed", "Expected PDFs", "Actual PDFs",
                                 "Correct Amount Downloaded?", "Errors"])

    # For each seed, downloads the PDF for each URL in the dictionary
    # and saves it to a folder named with the seed URL.
    for seed in to_download:

        # Makes a folder for the seed and makes that the current directory.
        # Also prints the seed name to the GUI to show the script's progress.
        # If there was an error, adds that to the log and starts the next seed.
        try:
            seed_folder_name = make_seed_folder(seed)
        except AttributeError:
            download_log_write.writerow([seed, "n/a", "n/a", "n/a",
                                         "Could not make the seed folder: new URL pattern."])
            continue
        except OSError:
            download_log_write.writerow([seed, "n/a", "n/a", "n/a",
                                         "Couldn't make the seed folder: unpermitted character(s)."])
            continue

        # Starts a dictionary of downloaded PDFs to detect duplicate file names with this seed
        # and a variable to track if there are download errors for later logging.
        downloads = {}
        download_error = False

        # Saves each PDF to its seed folder.
        for url in to_download[seed]:

            # Constructs the desired name for the file.
            filename = get_file_name(url)

            # Constructs the download URL for the file saved in Archive-It.
            # The "3" is for the most recent capture.
            ait_url = f"https://wayback.archive-it.org/{collection}/3/{url}"

            # Saves the PDF to the seed's folder, named with the desired name.
            download_result = subprocess.run(f'wget -O "{filename}" "{ait_url}"',
                                             shell=True, stderr=subprocess.PIPE)

            # Checks the result of downloading (the return code).
            # If there were no errors (code 0), verifies the expected size was downloaded.
            # If there was an error, saves the error to a log.
            if download_result.returncode == 0:
                regex = re.match(".*saved \\[([0-9]+)/([0-9]+)]", str(download_result.stderr))
                try:
                    if not regex.group(1) == regex.group(2):
                        add_error("Size downloaded is wrong", download_result)
                        download_error = True
                except AttributeError:
                    add_error("Can't calculate size downloaded", download_result)
                    download_error = True
            else:
                add_error("Error when downloading", download_result)
                download_error = True

        # Verifies the number of downloaded PDFs matches the expected number of PDFs for that seed.
        files_in_dictionary = len(to_download[seed])
        files_in_folder = len(os.listdir(os.path.join(input_directory, seed_folder_name)))

        # Creates language needed for the download log.
        if files_in_dictionary == files_in_folder:
            file_match = "No errors found"
        else:
            file_match = "Errors found"

        if download_error:
            seed_error = "Download errors found"
        else:
            seed_error = "No download errors found"

        # Saves results for this seed to the download log.
        download_log_write.writerow([seed, files_in_dictionary, files_in_folder,
                                     file_match, seed_error])

    # Close the download log.
    download_log.close()

    # Prints that the script has completed in the GUI dialogue box.
    print("\nDownloading is complete.")
    window.Refresh()

    # For threading: indicates the thread for running the script is done.
    window.write_event_value('-SCRIPT_THREAD-', (threading.current_thread().name,))


# For threading. Disables garbage collecting,
# which is restarted with gc.collect() once the GUI starts.
gc.disable()

# Defines a GUI for users to provide the input needed for this script and
# to receive messages about errors to their inputs and the script progress.
sg.theme("DarkTeal6")

LABELS = [[sg.Text('Folder with CSVs', font=("roboto", 13))],
          [sg.Text('Archive-It Collection', font=("roboto", 13))],
          [sg.Text(font=("roboto", 1))],
          [sg.Submit(key="submit", disabled=False), sg.Cancel()]]

BOXES = [[sg.Input(key="input_folder"), sg.FolderBrowse()],
         [sg.Combo(list(ait.AIT_COLL_DICT.keys()), key="ait_collection",
                   default_value=ait.AIT_COLL_DEFAULT)],
         [sg.Text(font=("roboto", 1))],
         [sg.Text(font=("roboto", 13))]]

LAYOUT = [[sg.Column(LABELS), sg.Column(BOXES)],
          [sg.Output(size=(90, 10))]]

WINDOW = sg.Window("Download PDFs from Archive-It", LAYOUT)

# Keeps the GUI open until the user quits the program. Receives user input, verifies the input,
# and when all input is correct runs the program.
while True:

    # For threading: start garbage collecting.
    gc.collect()

    # Gets the user input data.
    EVENT, VALUES = WINDOW.read()

    # For threading: let the user submit new information now that the script thread is over.
    if EVENT == SCRIPT_THREAD:
        WINDOW[f'{"submit"}'].update(disabled=False)

    # If the user submitted values, tests they are correct.
    # If not, errors are displayed. If yes, the script is run.
    if EVENT == "submit":

        # Error testing on all of the user inputs.
        # Errors are saved to a list so all values can be tested prior to notifying the user.
        ERRORS = []

        # Input folder (contains the Archive-It CSVs) is required and must be a valid path.
        if VALUES["input_folder"] == "":
            ERRORS.append("Folder with CSVs can't be blank.")
        elif not os.path.exists(VALUES["input_folder"]):
            ERRORS.append("Folder with CSVs path is not correct.")

        # Collection name is required and must match one of the collections in ait_collections.py.
        if VALUES["ait_collection"] == "":
            ERRORS.append("Archive-It Collection cannot be blank.")
        elif VALUES["ait_collection"] not in ait.AIT_COLL_DICT:
            ERRORS.append("Archive-It Collection is not one of the permitted values.")

        # If the user inputs are correct, runs the script.
        if len(ERRORS) == 0:

            # Prints that the script is starting in the GUI dialogue box.
            print("\n-----------------------------------------------------------")
            print("\nPlease wait while the PDFs you requested are downloaded.")
            WINDOW.Refresh()

            # Calculate collection ID from collection name (the user input)
            COLLECTION_ID = ait.AIT_COLL_DICT[VALUES["ait_collection"]]

            # For threading: run download_files() in a thread.
            os.chdir(VALUES["input_folder"])
            PROCESSING_THREAD = threading.Thread(target=download_files,
                                                 args=(VALUES["input_folder"],
                                                       COLLECTION_ID, WINDOW))
            PROCESSING_THREAD.start()

            # Disables the submit button while download_files() is running
            # so users can't start a new request before the first is done.
            WINDOW[f'{"submit"}'].update(disabled=True)

        # If some of the user inputs were not correct, creates a pop up box alerting the user
        # and prints the errors in the GUI dialogue box.
        # The user may then edit the provided input and resubmit.
        else:
            sg.Popup("There is a problem with the provided information. Check the GUI for details.")
            print("\nThe app could not run. Please correct the following information:")
            print("\n".join(ERRORS))
            WINDOW.Refresh()

    # If the user clicked cancel or the X on the GUI, quits the script.
    if EVENT in ("Cancel", None):
        sys.exit()
