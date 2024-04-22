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


if __name__ == '__main__':

    # Verifies the provided script argument(s) are correct and assigns them to variables.
    # If there are errors, prints the errors and exits the script.
    input_folder, ait_collection, errors_list = check_arguments(sys.argv)
    if len(errors_list) > 0:
        print('Please correct the following and run the script again:')
        for error in errors_list:
            print(f'  * {error}')
        sys.exit(1)
