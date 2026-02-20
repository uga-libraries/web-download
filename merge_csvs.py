"""Combine multiple Archive-It crawl reports for the PDF format, with cleanup, to review for download_files.py

Parameters

Returns

"""
import os
import pandas as pd
import sys


def check_argument(arg_list):
    """Verify the required script argument is present and a valid directory"""

    # Argument is missing if arg_list just has the script path.
    if len(arg_list) == 1:
        return None, 'Missing required argument, path to csv_directory.'
    else:
        if os.path.exists(arg_list[1]) and os.path.isdir(arg_list[1]):
            return arg_list[1], None
        else:
            return None, f'Path to "{arg_list[1]}" is not a valid directory.'


def csvs_to_df(csv_dir):
    """Return df with contents of all csvs in the csv_directory"""
    df_list = []
    for filename in os.listdir(csv_dir):
        if filename.startswith('crawled-detailed-list') and filename.endswith('.csv'):
            df = pd.read_csv(os.path.join(csv_dir, filename))
            df_list.append(df)
        else:
            print('Filename does not match expected naming convention and was skipped:', filename)
    df_combined = pd.concat(df_list, axis=0, ignore_index=True)
    return df_combined


def df_review(df):
    """Return an updated df with only the rows needed for review"""

    # Remove rows Archive-It flagged as a duplicate.
    df = df[df['is_duplicate'] != 1]

    # Remove rows based on keywords in the url

    return df


if __name__ == '__main__':

    # Assigns the script argument to a variable, and quits the script if there is an error.
    csv_directory, error = check_argument(sys.argv)
    if error:
        print(error)
        sys.exit(1)

    # Combines all CSVs in the directory into a single dataframe.
    csv_df = csvs_to_df(csv_directory)

    # Removes rows that do not need to be reviewed.
    csv_df = df_review(csv_df)

    # Saves the combined CSV to the csv_directory.
    csv_df.to_csv(os.path.join(csv_directory, 'GGP_PDF_URLS.csv'), index=False)

