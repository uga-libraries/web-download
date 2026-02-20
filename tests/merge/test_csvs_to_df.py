import os
import unittest
from merge_csvs import csvs_to_df


def df_to_list(df):
    """Make a list of every row in the df for easier comparison to expected results"""
    df = df.fillna('BLANK')
    df = df.astype(str)
    df_list = [df.columns.tolist()] + df.values.tolist()
    return df_list


class MyTestCase(unittest.TestCase):

    def test_multiple(self):
        """Test for when there are multiple correct PDF reports"""
        df = csvs_to_df(os.path.join('merge', 'test_data', 'csvs_to_df', 'multiple'))
        result = df_to_list(df)
        expected = [['url', 'size', 'is_duplicate', 'seed'],
                    ['https://seed1.gov/doc/4112023-agenda', '172900', '0', 'https://seed1.gov/'],
                    ['https://seed1.gov/doc/8162023-notice', '143699', '1', 'https://seed1.gov/'],
                    ['https://seed1.gov/doc/8162023-agenda', '166547', '0', 'https://seed1.gov/'],
                    ['https://seed1.gov/doc/3202024-agenda', '105194', '0', 'https://seed1.gov/'],
                    ['https://seed1.gov/doc/3202024-minutes', '1020159', '0', 'https://seed1.gov/'],
                    ['https://seed1.gov/doc/9122024-notice', '41573', '1', 'https://seed1.gov/'],
                    ['https://seed1.gov/doc/9122024-agenda', '102749', '0', 'https://seed1.gov/'],
                    ['https://seed2.gov/doc/training-cjcc', '6290847', '0', 'https://seed2.gov/'],
                    ['https://seed2.gov/doc/parent-resource', '172702', '0', 'https://seed2.gov/'],
                    ['https://seed3.gov/doc/2023-board-app', '218286', '0', 'https://seed3.gov/'],
                    ['https://seed4.gov/doc/special-92321pdf', '3354307', '0', 'https://seed4.gov/'],
                    ['https://seed4.gov/doc/special-102623', '608141', '0', 'https://seed4.gov/'],
                    ['https://seed4.gov/doc/exec-order/12311901', '42364', '1', 'https://seed4.gov/']]
        self.assertEqual(expected, result, "Problem with test for multiple")

    def test_one(self):
        """Test for when there is one correct PDF report"""
        df = csvs_to_df(os.path.join('merge', 'test_data', 'csvs_to_df', 'one'))
        result = df_to_list(df)
        expected = [['url', 'size', 'is_duplicate', 'seed'],
                    ['https://seed.gov/download/pdf/2023-board-application', '101', '0', 'https://seed.gov/'],
                    ['https://seed.gov/download/pdf/special-session-921pdf', '202', '0', 'https://seed.gov/'],
                    ['https://seed.gov/download/pdf/special-session-102623', '303', '0', 'https://seed.gov/'],
                    ['https://seed.gov/download/pdf/executiveorder/12311901', '404', '0', 'https://seed.gov/']]
        self.assertEqual(expected, result, "Problem with test for one")

    def test_skip(self):
        """Test for when there are two correct PDF reports and three files to skip"""
        df = csvs_to_df(os.path.join('merge', 'test_data', 'csvs_to_df', 'skip'))
        result = df_to_list(df)
        expected = [['url', 'size', 'is_duplicate', 'seed'],
                    ['https://seed1.gov/doc/4112023-agenda', '172900', '0', 'https://seed1.gov/'],
                    ['https://seed1.gov/doc/8162023-notice', '143699', '1', 'https://seed1.gov/'],
                    ['https://seed1.gov/doc/8162023-agenda', '166547', '0', 'https://seed1.gov/'],
                    ['https://seed1.gov/doc/3202024-agenda', '105194', '0', 'https://seed1.gov/'],
                    ['https://seed1.gov/doc/3202024-minutes', '1020159', '0', 'https://seed1.gov/'],
                    ['https://seed1.gov/doc/9122024-notice', '41573', '1', 'https://seed1.gov/'],
                    ['https://seed1.gov/doc/9122024-agenda', '102749', '0', 'https://seed1.gov/'],
                    ['https://seed2.gov/doc/training-cjcc', '6290847', '0', 'https://seed2.gov/'],
                    ['https://seed2.gov/doc/parent-resource', '172702', '0', 'https://seed2.gov/']]
        self.assertEqual(expected, result, "Problem with test for one")


if __name__ == '__main__':
    unittest.main()
