from data_manipulation import fm_split_max_min_estimated_values
import pandas.testing as pdt
import pandas as pd 

SERIE_1 = pd.Series({0:'NotSell', 1:'NotSell'})
SERIE_2 = pd.Series({0:'-', 1:'-'})
SERIE_3 = pd.Series({0:5_000, 1:25_000})
SERIE_3 = pd.Series({0:5_000, 1:25_000})

def test_str_value():
    result = fm_split_max_min_estimated_values('NotSell')
    pdt.assert_series_equal(result, SERIE_1, check_dtype=False, check_names=False)
    
def test_str_value_():
    result = fm_split_max_min_estimated_values('-')
    pdt.assert_series_equal(result, SERIE_2, check_dtype=False, check_names=False)
    
def test_list_int_values():
    result = fm_split_max_min_estimated_values([5_000, 25_000])
    pdt.assert_series_equal(result, SERIE_3)

def test_list_int_inverted_values():
    result = fm_split_max_min_estimated_values([25_000, 5_000])
    pdt.assert_series_equal(result, SERIE_3)