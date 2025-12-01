import pytest
from data_manipulation import fm_normalize_wage_values


def test_input_type_error():
    x = list()

    with pytest.raises(TypeError):
        fm_normalize_wage_values(x)

def test_random_value():
    with pytest.raises(ValueError):
        fm_normalize_wage_values('ubwyhsvbfcyhsd')

def test_wage_value():
    assert fm_normalize_wage_values('2 900 € p/s') == 2900

def test_non_wage_value():
    assert fm_normalize_wage_values('N/D') == 0

def test_int_value():
    assert fm_normalize_wage_values(2500) == 2500