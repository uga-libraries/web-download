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
import re
import subprocess
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


def download_seed(seed_name, urls, collection):
    """Download the publication at each url and save to a folder with the seed name"""

    # Prints the script's progress.
    print('Starting downloads for the next seed:', seed_name)

    # Makes a folder for the seed in input_directory, unless the seed cannot be converted to a folder title.
    try:
        seed_folder_name = make_seed_folder(seed_name)
    except AttributeError:
        log([seed, 'n/a', 'n/a', 'n/a', 'Could not make the seed folder: new URL pattern.'])
        return
    except OSError:
        log([seed, 'n/a', 'n/a', 'n/a', 'Could not make the seed folder: unpermitted character(s).'])
        return

    # Starts a dictionary of downloaded PDFs to add sequential numbers to duplicate names within this seed
    # and a variable to track if there are download errors for later logging.
    downloads = {}
    download_error = False

    # Saves each PDF to the seed folder.
    for url in urls:

        # Constructs the desired name for the file.
        # Also returns an updated version of downloads that includes the file.
        filename, downloads = get_file_name(url, downloads)

        # Constructs the download URL for the file saved in Archive-It.
        # The "3" is for the most recent capture.
        ait_url = f"https://wayback.archive-it.org/{collection}/3/{url}"

        # Saves the PDF to the seed's folder, named with the desired name.
        download_path = os.path.join(os.getcwd(), seed_folder_name, filename)
        download_result = subprocess.run(f'wget -O "{download_path}" "{ait_url}"',
                                         shell=True, stderr=subprocess.PIPE)

        # Checks the result of downloading (the return code).
        # If there were no errors (code 0), verifies the expected size was downloaded.
        # If there was an error, saves the error to a separate error log.
        if download_result.returncode == 0:
            regex = re.match('.*saved \\[([0-9]+)/([0-9]+)]', str(download_result.stderr))
            try:
                if not regex.group(1) == regex.group(2):
                    error_log('Size downloaded is wrong', download_result)
                    download_error = True
            except AttributeError:
                error_log('Cannot calculate size downloaded', download_result)
                download_error = True
        else:
            error_log('Error when downloading', download_result)
            download_error = True


def error_log(message, output):
    """Make an error log, if one doesn't already exist, and add the data for this error to it.

     Parameters:
        message : standard text to include in the log about the error
        output : output from wget, which generated the error
    """

    # If the error log does not exist, makes one with a header row.
    if not os.path.exists('error_log.csv'):
        with open('error_log.csv', 'w', newline='') as l:
            l_write = csv.writer(l)
            l_write.writerow(['Error', 'WGET Command', 'Return Code', 'STDERR'])

    # Adds the error to the log.
    with open('error_log.csv', 'a', newline='') as l:
        l_write = csv.writer(l)
        l_write.writerow([message, output.args, output.returncode, output.stderr.decode('utf-8')])


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


def get_file_name(file_url, downloads_dict):
    """Construct the file name based on the file URL.

    Parameters:
        file_url : URL for the PDF to be downloaded
        downloads_dict : dictionary with all files already downloaded for the seed

    Returns:
        name : name of the file
        downloads_dict : updated dictionary of file names with the next sequential number for duplicates
    """

    # Selects the part of the URL to use for the name. URL parts are the texts divided by the slashes.
    #   -If the URL doesn't have multiple parts (unlikely), the whole URL is the name.
    #   -If the last part of the URL is "download", the previous part of the URL is the name.
    #   -Otherwise, the last part of the URL is the name.
    if '/' not in file_url:
        name = file_url
    elif file_url.endswith('/download'):
        regex = re.match('.*/(.*)/download', file_url)
        name = regex.group(1)
    else:
        regex = re.match('.*/(.*)', file_url)
        name = regex.group(1)

    # Adds a ".pdf" file extension, if it doesn't have one.
    #    - Some extensions are all caps (.PDF)
    #    - Some have pdf or PDF but not the preceding period
    #    - Some do not have a file extension
    # Making all extensions lowercase so case-insensitive systems don't think it is a duplicate.
    if not name.endswith('.pdf'):
        if name.endswith('.PDF'):
            name = name[:-4] + '.pdf'
        elif name.endswith(('pdf', 'PDF')):
            name = name[:-3] + '.pdf'
        else:
            name = name + '.pdf'

    # Replaces any characters which Windows does not allow in a filename with an underscore.
    for character in ('/', '\\', '*', '?', '"', '<', '>', '|'):
        if character in name:
            name = name.replace(character, '_')

    # Adds a numerical extension to the file name if there is already another file of that name for this seed,
    # since generic names like report are common for different files,
    # and updates a dictionary that tracks the next sequential number to use for a file of that name.
    if name in downloads_dict:
        number = downloads_dict[name]
        downloads_dict[name] += 1
        name = name[:-4] + "_" + str(number) + ".pdf"
    # If this is the first time the file name is used, the next instance of the name will have an extension of 1.
    else:
        downloads_dict[name] = 1

    return name, downloads_dict


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


def make_seed_folder(seed_name):
    """Make a folder for the seed (website) and change the current directory to that folder.

    Parameters:
        seed_name : URL for the seed (website)

    Returns:
        The seed (website) folder name, which is the URL without http(s):// and slashes replaced by underscores.
    """

    # Makes a version of the seed URL which can be used for a folder name.
    # Removes http:// or https://, removes / from the end if present, and replaces any other / with _
    try:
        regex = re.match("https?://(.*?)/?$", seed_name)
        seed_folder = regex.group(1)
        seed_folder = seed_folder.replace("/", "_")
    except AttributeError:
        raise AttributeError

    # Tries to make a folder for the seed.
    # If there is an error from illegal characters, no PDFs are downloaded for this seed.
    try:
        os.makedirs(seed_folder)
    except OSError:
        raise OSError

    # Returns the seed folder name, which is needed later to check for completeness.
    return seed_folder


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
    print('Please wait while the PDFs you requested are downloaded.\n')

    # Gets a dictionary of the PDF URLs from each CSV in the input folder that will be downloaded.
    # If no URLs were located, prints that the script has completed and quits the script.
    to_download = get_download_urls()
    if to_download == {}:
        print('\nNo URLs were found to be downloaded. Script will end.')
        sys.exit(1)

    # Makes a log to save the result of each seed download.
    log('header')

    # Downloads every PDF for each seed.
    for seed, url_list in to_download.items():
        download_seed(seed, url_list, ait_collection)
