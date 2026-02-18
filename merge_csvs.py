"""Combine multiple Archive-It crawl reports for the PDF format, with cleanup, to review for download_files.py

Parameters

Returns

"""
import os
import pandas as pd
import sys


if __name__ == '__main__':

    # Assigns the script argument to a variable.
    csv_directory = sys.argv[1]

    # Combines all CSVs in the directory into a single dataframe.

    # Removes rows that do not need to be reviewed.

    # Saves the combined CSV to the csv_directory.

