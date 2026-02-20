import pandas as pd
import unittest
from merge_csvs import df_review
from test_csvs_to_df import df_to_list


def make_df(rows):
    """Make a df for test input with consistent column names"""
    column_names = ['url', 'size', 'is_duplicate', 'seed']
    df = pd.DataFrame(rows, columns=column_names)
    return df


class MyTestCase(unittest.TestCase):

    def test_empty(self):
        """Test for when all the rows are removed"""
        # Makes the df for input and runs the function.
        df = make_df([['www.1.gov/memo', 100, 0, 'www.1.gov'],
                      ['www.2.gov/PowerPoint', 200, 1, 'www.2.gov'],
                      ['www.3.gov/pdf', 300, 1, 'www.3.gov']])
        csv_df = df_review(df)

        # Verifies the contents of the returned df are correct.
        result = df_to_list(csv_df)
        expected = [['url', 'size', 'is_duplicate', 'seed']]
        self.assertEqual(expected, result, "Problem with test for empty")

    def test_keywords(self):
        """Test for when the url column includes keywords that mean the row is removed"""
        # Makes the df for input and runs the function.
        df = make_df([['www.1.gov/AGENDA', 100, 0, 'www.1.gov'],
                      ['www.2.gov/pdfmemoranda', 200, 0, 'www.2.gov'],
                      ['www.3.gov/pdf', 300, 0, 'www.3.gov'],
                      ['www.minutes.gov/download', 400, 0, 'www.minutes.gov'],
                      ['www.5.gov/PowerPoint', 500, 0, 'www.5.gov'],
                      ['www.6.gov/file', 600, 0, 'www.6.gov']])
        csv_df = df_review(df)

        # Verifies the contents of the returned df are correct.
        result = df_to_list(csv_df)
        expected = [['url', 'size', 'is_duplicate', 'seed'],
                    ['www.3.gov/pdf', '300', '0', 'www.3.gov'],
                    ['www.6.gov/file', '600', '0', 'www.6.gov']]
        self.assertEqual(expected, result, "Problem with test for keywords")

    def test_duplicate(self):
        """Test for when the df includes duplicates to remove"""
        # Makes the df for input and runs the function.
        df = make_df([['www.1.gov/pdf1', 100, 1, 'www.1.gov'],
                      ['www.2.gov/pdf2', 200, 0, 'www.2.gov'],
                      ['www.3.gov/pdf3', 300, 1, 'www.3.gov']])
        csv_df = df_review(df)

        # Verifies the contents of the returned df are correct.
        result = df_to_list(csv_df)
        expected = [['url', 'size', 'is_duplicate', 'seed'],
                    ['www.2.gov/pdf2', '200', '0', 'www.2.gov']]
        self.assertEqual(expected, result, "Problem with test for duplicate")

    def test_unchanged(self):
        """Test for when the df has nothing to remove"""
        # Makes the df for input and runs the function.
        df = make_df([['www.1.gov/pdf1', 100, 0, 'www.1.gov'],
                      ['www.2.gov/pdf2', 200, 0, 'www.2.gov'],
                      ['www.3.gov/pdf3', 300, 0, 'www.3.gov']])
        csv_df = df_review(df)

        # Verifies the contents of the returned df are correct.
        result = df_to_list(csv_df)
        expected = [['url', 'size', 'is_duplicate', 'seed'],
                    ['www.1.gov/pdf1', '100', '0', 'www.1.gov'],
                    ['www.2.gov/pdf2', '200', '0', 'www.2.gov'],
                    ['www.3.gov/pdf3', '300', '0', 'www.3.gov']]
        self.assertEqual(expected, result, "Problem with test for unchanged")


if __name__ == '__main__':
    unittest.main()
