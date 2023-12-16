import unittest

import pandas as pd
import logging

import sys, os

sys.path.append(os.path.abspath(os.path.join(".../")))
from Scripts.dataLoader import clean_data_loader

logging.basicConfig(filename='../logfile.log', filemode='a',
                    encoding='utf-8', level=logging.DEBUG)

class TestGetInformations(unittest.TestCase):
    def setUp(self):
       pass
     
    def test_clean_data(self):
        df = clean_data_loader("./test_data.csv")
        self.assertIsInstance(df, pd.DataFrame)

if __name__ == "__main__":
    unittest.main()