from data_manipulation import fm_convert_str_to_numeric
import pandas.testing as pdt
import pandas as pd 

INPUT_DATAFRAME = pd.DataFrame(
    data={
        'nome':['matheus','jose','sousa', 'almeida','cafe'], 
        'partidas':['20(3)', '10', '29(3)', '4(2)', '8'],
        'preco_min':['200_000', '100', '2_900_000', '40_000', '8_000'],
        'preco_max':['200_000', '100', '2_900_000', '40_000', '8_000'],
        'minutos':['2087', '1000', '2900', '309', '800'],
        'gols':['20', '10', '29', '4', '8'],
        'defesas':['6', '-10', '2', '4', '-3'],
        'ass':['12', '7', '10', '3', '8'],
    })

OUTPUT_DATAFRAME  = pd.DataFrame(
    data={
        'nome':['matheus','jose','sousa', 'almeida','cafe'], 
        'partidas':['20(3)', '10', '29(3)', '4(2)', '8'],
        'preco_min':['200_000', '100', '2_900_000', '40_000', '8_000'],
        'preco_max':['200_000', '100', '2_900_000', '40_000', '8_000'],
        'minutos':[2087, 1000, 2900, 309, 800],
        'gols':[20, 10, 29, 4, 8],
        'defesas':[6, -10, 2, 4, -3],
        'ass':[12, 7, 10, 3, 8],
    })

def test_convert_standart_df():
    result = fm_convert_str_to_numeric(INPUT_DATAFRAME)
    pdt.assert_frame_equal(result, OUTPUT_DATAFRAME )
    

INPUT_DATAFRAME = pd.DataFrame(
    data={
        'nome':['matheus','jose','sousa', 'almeida','cafe'], 
        'partidas':['20(3)', '10', '29(3)', '4(2)', '8'],
        'preco_min':['200_000', '100', '2_900_000', '40_000', '8_000'],
        'preco_max':['200_000', '100', '2_900_000', '40_000', '8_000'],
        'minutos':['2087', '-', '2900', '309', '800'],
        'gols':['20', '10', '29', '4', '8'],
        'defesas':['6', '-10', '2', '4', '-3'],
        'ass':['12', '7', '10', 'Matheus', '8'],
    })

OUTPUT_DATAFRAME  = pd.DataFrame(
    data={
        'nome':['matheus','jose','sousa', 'almeida','cafe'], 
        'partidas':['20(3)', '10', '29(3)', '4(2)', '8'],
        'preco_min':['200_000', '100', '2_900_000', '40_000', '8_000'],
        'preco_max':['200_000', '100', '2_900_000', '40_000', '8_000'],
        'minutos':[2087, 0, 2900, 309, 800],
        'gols':[20, 10, 29, 4, 8],
        'defesas':[6, -10, 2, 4, -3],
        'ass':['12', '7', '10', 'Matheus', '8'],
    })

def test_convert_broken_df():
    result = fm_convert_str_to_numeric(INPUT_DATAFRAME)
    pdt.assert_frame_equal(result, OUTPUT_DATAFRAME )