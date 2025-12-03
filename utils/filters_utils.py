import pandas as pd
from itertools import chain
from fmgen.utils.debuger import debug_print
from colorama import Fore, Style


def get_sorted_unique_list_from_position_column(df: pd.DataFrame) -> list:
    """
    Extrai valores únicos de uma coluna que contém listas e os ordena segundo uma 
    ordem predefinida.
    """
        
    sorted_list_from_position_col = sort_positions_list(unique_list_from_column(df, 'posicao_analise'))
    
    return sorted_list_from_position_col

def get_sorted_unique_list_from_column(df: pd.DataFrame, col: str) -> list:
    
    """
    Extrai valores únicos de um DataFrame e retornam em forma de lista.
    """
        
    sorted_list_from_col = sorted(df[col].unique().tolist())
    
    return sorted_list_from_col

def unique_list_from_column(df: pd.DataFrame, col: str) -> list:
    
    
    """
    Recebe uma coluna do DataFrame com listas em cada célula e retorna uma lista única 
    de valores, sem repetição e preservando a ordem de primeira ocorrência.
    """
    
    try:
        
        if col not in df.columns:
            raise ValueError(f"Coluna '{col}' não encontrada no DataFrame.")
        
        column_list = list(chain.from_iterable(df[col].dropna().tolist()))
        unique_list = list(set(column_list))
        
        return unique_list
        
    except Exception as e:
        
        debug_print(Fore.RED + f"[ERROR]: {str(e)}" + Style.RESET_ALL)
        return []
    
def sort_positions_list(unsorted_list:list) -> list:
    
    """
    Ordena uma lista de posições conforme a ordem tática definida.
    Posições não reconhecidas serão colocadas no final.
    """
    
    sorted_positions = ['Goleiro',
                        'Zagueiro', 
                        'Lateral-Direito', 
                        'Lateral-Esquerdo', 
                        'Ala-Direito', 
                        'Ala-Esquerdo', 
                        'Volante', 
                        'Meia-Central', 
                        'Meia-Direito', 
                        'Meia-Esquerda', 
                        'Meia-Armador', 
                        'Meia/Ponta-Direita', 
                        'Meia/Ponta-Esquerda', 
                        'Centroavante']

    if isinstance(unsorted_list, list) and unsorted_list:
        sorted_list = sorted(unsorted_list, key=lambda x: sorted_positions.index(x) if x in sorted_positions else float('inf'))
    
    else:
        sorted_list = []
    
    return sorted_list

def get_min_and_max_value_from_column(df: pd.DataFrame, col=str) ->list:
    
    min_salary = df[col].min()
    max_salary = df[col].max()
    
    if min_salary == max_salary:
        min_salary = 0
    
    return [float(min_salary), float(max_salary)]

def load_initial_filter_options(df: pd.DataFrame) -> tuple:
    
    output_season_selector_options = get_sorted_unique_list_from_column(df, 'id_temporada')
    output_division_selector_options =get_sorted_unique_list_from_column(df, 'divisao_atual')
    output_clubs_selector_options = get_sorted_unique_list_from_column(df, 'clube_atual')
    output_position_selector_options = get_sorted_unique_list_from_position_column(df)
    
    output_salary_selector_value = get_min_and_max_value_from_column(df,'salario')
    output_salary_selector_min = output_salary_selector_value[0]
    output_salary_selector_max = output_salary_selector_value[1]
    
    output_minutes_selector_value = get_min_and_max_value_from_column(df,'minutos')
    output_minutes_selector_min = output_minutes_selector_value[0]
    output_minutes_selector_max = output_minutes_selector_value[1]
   
    
    
    return (output_season_selector_options,
            output_division_selector_options,
            output_clubs_selector_options,
            output_position_selector_options,
            output_salary_selector_min,
            output_salary_selector_max,
            output_salary_selector_value,
            output_minutes_selector_min,
            output_minutes_selector_max,
            output_minutes_selector_value
            )
    
def get_common_items(list_a: list, list_b: list) -> list:
    
    try:
        list_with_common_items = list(set(list_a) & set(list_b))
        
        return list_with_common_items
    
    except Exception as e:
        
        debug_print(Fore.RED + f"[ERROR]: {str(e)}" + Style.RESET_ALL)
        
        return []
    
def adjust_values_to_range(values:list, min:int|float, max:int|float) -> list:
   
    
    a = values[0]
    b = values[1]

    if a < min:
        a = min
    
    if b > max:
        b = max
    
    adjusted_values = [a, b]
        
    
    return adjusted_values

def filter_except(df: pd.DataFrame, exclude_col: str, filters:dict) -> pd.DataFrame:
    """
    Função que filtra uma df, excluindo a coluna que está sendo filtrada, gerando opções para ostros filtros
    sem autoeliminar as opções a serem selecionadas pelo filtro que está sendo mudado

    Args:
        df (pd.DataFrame): _description_
        excludde_col (str): _description_
        filters (dict): _description_

    Returns:
        pd.DataFrame: _description_
    """
    
    mask = pd.Series(True, index= df.index) #Cria uam serie "True" que será validado passo a passo em cada filtro, retornando se a linha está dentro de todos os filtros ou não
    
    for col, value in filters.items(): #Desenpacota a "chave" e "valor" do dicionário dos filtros, onde "col" é a chave e "valor" é o valor do dicionário
        if col in exclude_col or not value:
            continue #Se a coluna está marcada como "exclude_col" a função volta pra pra proxima pra começar uma nova iteração
        
        if col == 'posicao_analise': #Se col for "posicao" aplica filtro especifico pra cada coluna
            mask &= df[col].apply(lambda x: isinstance(x, list) and any(pos in x for pos in value))
            
        elif col in ['salario', 'minutos']: #Se a coluna for com valores de "ranges" aplica o filtro específico pra colunas com dois valores
            if isinstance(value, list) and len(value) == 2:
                mask &= df[col].between(*value)
        else: #Se não, aplica o filtro normal das colunas com valores inseridos em listas
            mask &= df[col].isin(value)

    return df[mask]