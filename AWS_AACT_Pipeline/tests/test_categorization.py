import pytest
from _pytest import unittest

from AWS_AACT_Pipeline.categorize_driver import Driver
from AWS_AACT_Pipeline.mock_db_manager import MockDatabaseManager
from AWS_AACT_Pipeline.categorizer import Categorizer
import pandas as pd


def test_missing_json_file():
    categorizer = Categorizer()
    pytest.raises(Exception, categorizer.read_file_conditions, "fake_json")


def test_good_driver_call():
    og_df = pd.DataFrame(columns=['color', 'nct_id'], index=['kylie','willy', 'riley', 'ben', 'jonah'])

    og_df.loc['kylie'] = pd.Series({'color': "yellow", 'nct_id': 1})
    og_df.loc['willy'] = pd.Series({'color': "turquoise", 'nct_id': 2})
    og_df.loc['riley'] = pd.Series({'color': "blue", 'nct_id': 3})
    og_df.loc['ben'] = pd.Series({'color': "blue", 'nct_id': 4})
    og_df.loc['jonah'] = pd.Series({'color': "blue", 'nct_id': 5})

    end_df = pd.DataFrame(columns=['nct_id', 'color_category'], index=['kylie','willy', 'riley', 'ben', 'jonah'])
    end_df.loc['kylie'] = pd.Series({'nct_id': 1, 'color_category': "Other"})
    end_df.loc['willy'] = pd.Series({'nct_id': 2, 'color_category': "Cool"})
    end_df.loc['riley'] = pd.Series({'nct_id': 3, 'color_category': "Cool"})
    end_df.loc['ben'] = pd.Series({'nct_id': 4, 'color_category': "Cool"})
    end_df.loc['jonah'] = pd.Series({'nct_id': 5, 'color_category': "Cool"})

    mock_db = MockDatabaseManager(og_df)
    driver = Driver(mock_db)

    driver.make_new_tables("team", "color", 'new_table', 'color_category', 'mock_json')

    final_df = mock_db.get_final_dataframe()

    assert final_df.equals(end_df)
