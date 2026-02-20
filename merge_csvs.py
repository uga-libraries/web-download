"""Combine multiple Archive-It crawl reports for the PDF format, with cleanup, to review for download_files.py

Cleanup removes rows that Archive-It labeled as a duplicate
and where the URL contains keywords that indicate it is not a publication.

Parameter
csv_directory: path to the folder containing Archive-It File Type reports for application/pdf

Returns
YYYY_GGP_PDF_URLS.csv saved to the csv_directory,
which combining all rows from all the csvs that require review for if they are publications
"""
from datetime import date
import os
import pandas as pd
import sys


def check_argument(arg_list):
    """Verify the required script argument is present and a valid directory

    Parameters:
    arg_list (list): output of sys.argv after starting the script

    Returns:
    csv_directory (path as string, None): path to csv_directory if in arg_list, or None if error
    error (string, None): error message, or None if no error
    """
    if len(arg_list) == 1:
        return None, 'Missing required argument, path to csv_directory.'
    else:
        if os.path.exists(arg_list[1]) and os.path.isdir(arg_list[1]):
            return arg_list[1], None
        else:
            return None, f'Path to "{arg_list[1]}" is not a valid directory.'


def csvs_to_df(csv_dir):
    """Combine all rows of all csvs in the csv_directory to one dataframe

    Parameters:
    csv_dir (path as string): path to folder with Archive-It csvs (script argument)

    Returns:
    df_combined (pandas df): df with all rows of all csvs in the csv_directory
    """
    df_list = []
    for filename in os.listdir(csv_dir):
        # Verify filename follows Archive-It naming convention, and print if not so the error can be checked.
        if filename.startswith('crawled-detail-list') and filename.endswith('.csv'):
            df = pd.read_csv(os.path.join(csv_dir, filename))
            df_list.append(df)
        else:
            print('Filename does not match expected naming convention and was skipped:', filename)
    df_combined = pd.concat(df_list, axis=0, ignore_index=True)
    return df_combined


def df_review(df):
    """Remove rows that don't need to be reviewed for if they are publications from the df

    Parameters
    df (pandas dataframe): df with all rows of all csvs in the csv_directory

    Returns
    df (pandas dataframe): updated version of df with only the rows needed for review
    """

    # Remove rows Archive-It flagged as a duplicate.
    df = df[df['is_duplicate'] != 1]

    # Remove rows based on keywords in the url.
    keywords_list = ['agenda', 'memo', 'minutes', 'powerpoint']
    keywords = '|'.join(keywords_list)
    remove = df['url'].str.contains(keywords, case=False, na=False)
    df = df[~remove]

    return df


if __name__ == '__main__':

    # Assigns the script argument to a variable, and quits the script if there is an error with the argument.
    csv_directory, error = check_argument(sys.argv)
    if error:
        print(error)
        sys.exit(1)

    # Combines all rows from all Archive-It CSVs in the directory into a single dataframe.
    csv_df = csvs_to_df(csv_directory)

    # Removes rows that do not need to be reviewed.
    csv_df = df_review(csv_df)

    # Saves the rows to be reviewed to a CSV in the csv_directory, as long as df_review has some content.
    # If not, prints a message to show the CSV was not made intentionally, as opposed to a script error.
    if len(csv_df.index) > 0:
        csv_df.to_csv(os.path.join(csv_directory, f'{date.today().strftime("%Y")}_GGP_PDF_URLS.csv'), index=False)
    else:
        print("None of the csvs contain rows that require review.")
