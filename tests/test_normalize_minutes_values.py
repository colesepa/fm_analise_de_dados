import pytest
from data_manipulation import fm_normalize_minutes_values

def test_standart_value():
    assert fm_normalize_minutes_values('3 156') == 3156
    
def test_float_value_error():
    with pytest.raises(TypeError):
        fm_normalize_minutes_values(3.26) # type: ignore
        
def test_nan_value():
    assert fm_normalize_minutes_values('-') == 0
    
def test_negative_value():
    with pytest.raises(ValueError):
        fm_normalize_minutes_values(-4)
        
def test_unicode_value():
    assert fm_normalize_minutes_values('4\xa0500') == 4500

def test_instance_error():
    inpt = list()
    
    with pytest.raises(TypeError):
        fm_normalize_minutes_values(inpt) # type: ignore