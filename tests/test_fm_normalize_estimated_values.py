from data_manipulation import fm_normalize_estimated_values



def test_normalize_notsell():
    assert fm_normalize_estimated_values('Não está à venda') == 'NotSell'
    
def test_normalize_unknow():
    assert fm_normalize_estimated_values('Desconhecido') == '-'
    
def test_normalize_values():
    assert fm_normalize_estimated_values('7.6M € - 23M €') == [7_600_000, 23_000_000]