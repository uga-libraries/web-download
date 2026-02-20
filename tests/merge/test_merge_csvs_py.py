"""Tests for the entire script"""
from datetime import date
import os
import pandas as pd
import subprocess
import unittest


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Remove the GGP_PDF_URLS.csv made by the script, if present"""
        csv_path = os.path.join(os.getcwd(), 'test_data', 'merge_csvs_py', 'normal',
                                f'{date.today().strftime("%Y")}_GGP_PDF_URLS.csv')
        if os.path.exists(csv_path):
            os.remove(csv_path)

    def test_normal(self):
        """Test for normal functioning, when there are rows requiring review"""
        # Makes the variables for input and runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'merge_csvs.py')
        csvs_dir = os.path.join(os.path.join(os.getcwd(), 'test_data', 'merge_csvs_py', 'normal'))
        printed = subprocess.run(f'python {script_path} {csvs_dir}', shell=True, capture_output=True, text=True)

        # Verifies the printed statement.
        expected = 'Filename does not match expected naming convention and was skipped: to_skip.txt\n'
        self.assertEqual(expected, printed.stdout, "Problem with test for normal, printed statement")

        # Verifies the contents of the GGP_PDF_URLS.csv produced by the script.
        csv_df = pd.read_csv(os.path.join(csvs_dir, f'{date.today().strftime("%Y")}_GGP_PDF_URLS.csv'), dtype=str)
        result = [csv_df.columns.tolist()] + csv_df.values.tolist()
        expected = [['url', 'size', 'is_duplicate', 'seed'],
                    ['https://seed1.gov/doc/4112023-report', '172900', '0', 'https://seed1.gov/'],
                    ['https://seed1.gov/doc/3202024-report', '105194', '0', 'https://seed1.gov/'],
                    ['https://seed2.gov/doc/training-cjcc', '6290847', '0', 'https://seed2.gov/'],
                    ['https://seed2.gov/doc/parent-resource', '172702', '0', 'https://seed2.gov/'],
                    ['https://seed3.gov/doc/2024-board-app', '218285', '0', 'https://seed3.gov/'],
                    ['https://seed3.gov/doc/2025-board-app', '218284', '0', 'https://seed3.gov/']]
        self.assertEqual(expected, result, "Problem with test for normal, csv")

    def test_error(self):
        """Test for when the required argument is missing and the script quits."""
        # Verifies the script exits.
        script_path = os.path.join(os.getcwd(), '..', '..', 'merge_csvs.py')
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.run(f'python {script_path}', shell=True, check=True, stdout=subprocess.PIPE)

        # Verifies the printed statement.
        printed = subprocess.run(f'python {script_path}', shell=True, capture_output=True, text=True)
        expected = 'Missing required argument, path to csv_directory.\n'
        self.assertEqual(expected, printed.stdout, "Problem with test for error, printed statement")

    def test_none(self):
        """Test for when there are no rows to review and no GGP_PDF_URLS.csv is made."""
        # Makes the variables for input and runs the script.
        script_path = os.path.join(os.getcwd(), '..', '..', 'merge_csvs.py')
        csvs_dir = os.path.join(os.path.join(os.getcwd(), 'test_data', 'merge_csvs_py', 'none'))
        printed = subprocess.run(f'python {script_path} {csvs_dir}', shell=True, capture_output=True, text=True)

        # Verifies the printed statement.
        expected = 'None of the csvs contain rows that require review.\n'
        self.assertEqual(expected, printed.stdout, "Problem with test for none, printed statement")

        # Verifies the GGP_PDF_URLS.csv was not produced by the script.
        csv_path = os.path.join(csvs_dir, f'{date.today().strftime("%Y")}_GGP_PDF_URLS.csv')
        result = os.path.exists(csv_path)
        self.assertEqual(False, result, "Problem with test for none, csv")


if __name__ == '__main__':
    unittest.main()
