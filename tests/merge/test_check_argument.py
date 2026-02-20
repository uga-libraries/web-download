import os
import unittest
from merge_csvs import check_argument


class MyTestCase(unittest.TestCase):

    def test_correct(self):
        """Test for when the required argument is present and a valid directory"""
        arg_list = ['merge_csvs.py', os.path.join(os.getcwd(), 'test_data', 'check_arguments')]
        csv_directory, error = check_argument(arg_list)
        self.assertEqual(arg_list[1], csv_directory, "Test for correct, csv_directory")
        self.assertEqual(None, error, "Test for correct, error")

    def test_file_error(self):
        """Test for when the required argument is present and a valid path but not a directory"""
        arg_list = ['merge_csvs.py', os.path.join(os.getcwd(), 'test_data', 'check_arguments', 'File.txt')]
        csv_directory, error = check_argument(arg_list)
        self.assertEqual(None, csv_directory, "Test for file, csv_directory")
        self.assertEqual(f'Path to "{arg_list[1]}" is not a valid directory.', error, "Test for file, error")

    def test_missing_arg(self):
        """Test for when the required argument is missing"""
        arg_list = ['merge_csvs.py']
        csv_directory, error = check_argument(arg_list)
        self.assertEqual(None, csv_directory, "Test for missing, csv_directory")
        self.assertEqual('Missing required argument, path to csv_directory.', error, "Test for missing, error")

    def test_path_error(self):
        """Test for when the required argument is present but is not a valid path"""
        arg_list = ['merge_csvs.py', os.path.join(os.getcwd(), 'test_data', 'check_arguments', 'MISSING')]
        csv_directory, error = check_argument(arg_list)
        self.assertEqual(None, csv_directory, "Test for path_error, csv_directory")
        self.assertEqual(f'Path to "{arg_list[1]}" is not a valid directory.', error, "Test for path_error, error")


if __name__ == '__main__':
    unittest.main()
