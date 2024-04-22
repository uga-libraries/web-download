"""Download individual PDF files from saved Archive-It crawls.

At UGA, this script is used by MAGIL to provide access to Georgia Government Publications
via the Digital Library of Georgia.

Parameters:
    input_folder (required): path to the folder with Archive-It CSVs files listing the PDF URls
    ait_collection (optional): Archive-It collection the websites are part of (all must be in the same one),
                               if not the default Georgia Government Publications

Returns:
    One folder for each website (seed), with the PDFs from that seed.
    A download_log.csv file with if the correct number of PDFs were downloaded and a summary of any other error.
    An error_log.csv file with details about each wget error, if there were any errors.
"""
import csv
import os
import sys


def check_arguments(arg_list):
    
    folder = None
    collection = '15678'
    errors = []
    
    # No arguments provided; just has the script path.
    if len(arg_list) == 1:
        errors.append('Missing required argument input_folder')
    # The required input_folder argument is present.
    if len(arg_list) > 1:
        if os.path.exists(arg_list[1]):
            folder = arg_list[1]
        else:
            errors.append(f'Folder with CSVS path "{arg_list[1]}" is not correct')
    # The optional ait_collection is present.
    if len(arg_list) > 2:
        ait_coll_dict = {"Activists and Advocates": "12263",  "Business": "12939",
                         "Georgia Disability History Archive": "12264", "Georgia Government Publications": "15678",
                         "Georgia Politics": "12265", "Legal": "12944", "Political Observers": "12262",
                         "University of Georgia Academics": "16951", "University of Georgia Administration": "12912",
                         "University of Georgia Athletics": "12907", "University of Georgia Student Life": "12181"}
        if arg_list[2] not in ait_coll_dict:
            errors.append(f'Archive-It Collection "{arg_list[2]}" is not one of the permitted values')
        else:
            collection = ait_coll_dict[arg_list[2]]
    # Too many arguments are present.
    if len(arg_list) > 3:
        errors.append('Too many arguments. Maximum is input_folder (required) and ait_collection (optional).')
    
    return folder, collection, errors


def get_download_urls():
    """Get the PDF URLs from each CSV in the input folder and save them to a dictionary.

    Returns:
        A dictionary with seed (website) as the key and a list of PDF URLs for each seed as the value.
    """

    # Makes a dictionary for the results.
    download_urls_dict = {}

    # Finds and reads every CSV in the input directory.
    for input_csv in os.listdir('.'):

        # Skips files that aren't CSVs and skips folders.
        if not input_csv.endswith('.csv') or os.path.isdir(input_csv):
            continue

        # Reads the CSV.
        with open(input_csv) as csvfile:
            data = csv.reader(csvfile)

            # Verifies the header has the expected values.
            # If not, prints an error and starts the next CSV.
            header = next(data)
            if not header == ['url', 'size', 'is_duplicate', 'seed']:
                print("This CSV is not formatted correctly and will be skipped:", input_csv)
                continue

            # Updates the download urls dictionary with data about each PDF URL.
            for row in data:
                url, size, is_duplicate, seed = row
                # Does not add the PDF URL to the dictionary if it is a duplicate (value of 1).
                if is_duplicate == '1':
                    continue
                # Adds the PDF URL if the seed is already in the dictionary.
                if seed in download_urls_dict:
                    download_urls_dict[seed].append(url)
                # Adds the seed URL and PDF URL to the dictionary if the seed isn't already present.
                else:
                    download_urls_dict[seed] = [url]

    return download_urls_dict


def log(row_list):
    """Add a row of data to the log, which is in the input_directory, or makes the log if it doesn't exist"""

    # Makes a new log and adds a header row.
    if row_list == 'header':
        with open('download_log.csv', 'w', newline='') as l:
            l_write = csv.writer(l)
            l_write.writerow(['Seed', 'Expected PDFs', 'Actual PDFs', 'Correct Amount Downloaded?', 'Errors'])

    # Adds a new row of data to an existing log.
    else:
        with open('download_log.csv', 'a', newline='') as l:
            l_write = csv.writer(l)
            l_write.writerow(row_list)


if __name__ == '__main__':

    # Verifies the provided script argument(s) are correct and assigns them to variables.
    # If there are errors, prints the errors and exits the script.
    input_folder, ait_collection, errors_list = check_arguments(sys.argv)
    if len(errors_list) > 0:
        print('Please correct the following and run the script again:')
        for error in errors_list:
            print(f'  * {error}')
        sys.exit(1)
    os.chdir(input_folder)

    # Notification that the script is starting.
    print('\nCorrect script input was provided.')
    print('Please wait while the PDFs you requested are downloaded.')

    # Gets a dictionary of the PDF URLs from each CSV in the input folder that will be downloaded.
    # If no URLs were located, prints that the script has completed and quits the script.
    to_download = get_download_urls()
    if to_download == {}:
        print('\nNo URLs were found to be downloaded. Script will end.')
        sys.exit(1)

    # Makes a log to save the result of each seed download.
    log('header')
