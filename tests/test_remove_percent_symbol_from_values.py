from data_manipulation import fm_remove_percent_symbol_from_values
import pandas as pd
import pandas.testing as pdt

def test_pd_NA_value():
    assert fm_remove_percent_symbol_from_values(pd.NA) == 0
    
def test_str_value():
    assert fm_remove_percent_symbol_from_values('Matheus') == 'Matheus'
    
def test_str_percent_value():
    assert fm_remove_percent_symbol_from_values('Matheus%') == 'Matheus'
    
def test_digit_str_value():
    assert fm_remove_percent_symbol_from_values('34.67%') == 34.67
    
def test_int_value():
    assert fm_remove_percent_symbol_from_values(34) == 34