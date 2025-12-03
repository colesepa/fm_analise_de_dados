
def get_list_group_column(columns_list: list, filter_values:list, all_groups=True, exactly=False) -> list:
    
    """
    Filtra uma lista de colunas (dicionários) com base em valores de grupo.

    Args:
        columns_list (list): Lista de dicionários, onde cada dicionário representa uma coluna com chave 'group'.
        filter_values (list): Lista de grupos desejados.
        all_groups (bool): Se True, adiciona 'Todas' aos filtros.
        exactly (bool): Se True, compara os grupos exatamente (como conjuntos); se False, permite sobreposição parcial.

    Returns:
        list: Lista de colunas filtradas.
    """
    
    result = []

    if not all([isinstance(columns_list, list), all(isinstance(col, dict) for col in columns_list), isinstance(filter_values, list)]):
        raise TypeError("Parâmetros inválidos: 'columns_list' deve ser lista de dicionários e 'filter_values' uma lista.")

    
       
    if all_groups and 'Todas' not in filter_values:
        filter_values  = filter_values + ['Todas']
        
    if exactly:
        
        for col in columns_list:
            if set(col.get('group', [])) == set(filter_values):
                result.append(col)
    else:
        for col in columns_list:
            if any(x in filter_values for x in col.get('group', [])):
                result.append(col)
            
    return result

def pretty_print_list(input_list:list, n_ident:int|float = 4) -> None:
    
    """
    Imprime uma lista formatada de forma visualmente organizada,
    com indentação configurável e vírgulas entre os elementos.

    Args:
        input_list (list): Lista de elementos a serem impressos.
        n_ident (int | float): Número de espaços de indentação. Valores float são convertidos para int.

    Returns:
        None
    """
    
    
    if not isinstance(n_ident, (int,float)):
        n_ident = 4
    if isinstance(n_ident, float):
        n_ident = int(n_ident)
        
    if not isinstance(input_list, list):
        raise TypeError("Parâmetros inválidos: 'input_list' deve ser uma lista.")
    
    result = '[\n'
    n_linhas = len(input_list)
    
    for idx, line in enumerate(input_list):
        line_str = f"{n_ident*' '}{line}"
    
        if idx < n_linhas - 1:
            result += line_str + ',\n'
        else:
            result += line_str + '\n'

    result += ']'
    
    print(result)
    
    return None

def get_columnsDef_from_value(input_value:str | list ='Geral', dict_group_from_columns:dict = {}, columns_config:list = []) -> list[dict]:

        if hasattr(input_value, "__iter__") and isinstance(input_value, list):
            input_value = input_value[0]
        elif isinstance(input, str):
            pass
     
        if input_value in dict_group_from_columns:
            dict_columns_config = {col['field']:col for col in columns_config}
            columnsDef = [dict_columns_config[coluna] for coluna in dict_group_from_columns[input_value] if coluna in dict_columns_config]
            return columnsDef
            
        else:
            return [{}]