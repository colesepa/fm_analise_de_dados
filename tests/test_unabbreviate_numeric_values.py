from data_manipulation import fm_unabbreviate_numeric_values


def test_unabbreviete_int():
    assert fm_unabbreviate_numeric_values("1.4m") == [1_400]
    
def test_unabbreviate_milhar_values():
    assert fm_unabbreviate_numeric_values('220m € - 425m €') == [220_000, 425_000]

def test_unabbreviate_milhoes_values():
    assert fm_unabbreviate_numeric_values('70m € - 1.7M €') == [70_000, 1_700_000]
    
def test_unabbreviate_nan_values():
    assert fm_unabbreviate_numeric_values('-') == []
    
def test_unabbreviate_zero_values():
    assert fm_unabbreviate_numeric_values('0') == [0]    

def test_unabbreviate_non_abbreviated():
    assert fm_unabbreviate_numeric_values('2500') == [2_500]
    
def test_unnabreviate_non_numeric():
    assert fm_unabbreviate_numeric_values('Matheus') == []