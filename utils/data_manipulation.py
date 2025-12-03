import pandas as pd
import numpy as np
from .files_utils import get_selected_files_names, get_file_extension, get_selected_files_paths

from .data_preprocessing import (
                                    _initialize_fm_dataframe,
                                    _drop_fm_dataframe_columns,
                                    _normalize_values,
                                    _str_to_numeric_values,
                                    _fillna_with_default,
                                    _replace_hyphen_with_zero,
                                    _create_new_position_column,
                                    _add_custom_metrics_columns,
                                    _rename_columns_names,
                                    _reorganize_columns_df,
                                    )

pd.set_option('future.no_silent_downcasting', True)


def fm_create_dataframe(path:any = None) -> pd.DataFrame: 
    
    if path is None:
        # 1. Carregamento Inicial
        df = _initialize_fm_dataframe()
    else: 
        # 1. Carregamento Inicial    
        df = _initialize_fm_dataframe(path)
        
    # 2. Limpeza estutural nas colunas importadas    
    columns_for_drop = ['Preço Exigido','Inf', 'CC-JA %','% Dfp','Valor', 'Crz T/90','PC/90']
    df = _drop_fm_dataframe_columns(df, columns_for_drop)
    
    # 3. Normalização de valores
    df = _normalize_values(df)
    df = _str_to_numeric_values(df)
    
    # 4. Tratamento de valores nulos e símbolos
    df = _fillna_with_default(df,'Personalidade','-')
    df = _replace_hyphen_with_zero(df)
    
    # 5. Criação de novas colunas e métricas
    df = _create_new_position_column(df)
    df = _add_custom_metrics_columns(df)
    
    # 6. Preenchimentos de valores inf, -inf e NaN
    # df = df.replace([np.inf,-np.inf, np.nan], 0.00)

    # 7. Renomear algumas colunas 
    df = _rename_columns_names(df)
       
    #8. Reorganizar ordem das colunas, agrupando por contexto de estastística
    df = _reorganize_columns_df(df)
    
    return df
   
def fm_convert_str_to_numeric(df:pd.DataFrame) -> pd.DataFrame:
    
    list_of_columns = list(df.columns)
    list_of_columns.remove('Jogos')
    list_of_columns.remove('preco_minimo')
    list_of_columns.remove('preco_maximo')

    
    for col in list_of_columns:
        if df[col].astype(str).str.match(r'^[+-]?(\d+\.?\d+?)$').any():
            try:
                df[col] = df[col].replace('-',0)
                df[col] = pd.to_numeric(df[col])
                
            except:
                pass
        
    return df
  
def fm_initialize_dataframe(filePath:str) -> pd.DataFrame:
    
    """ 
    Importa um arquivo do tipo HTML, CSV ou Excel e retorna um DataFrame do Pandas.

    Args:
        filePath (str): Caminho do arquivo a ser importado.
        

    Returns:
        pd.DataFrame: DataFrame do Pandas

    """
    
    name_file = get_selected_files_names(filePath)
    extension = get_file_extension(name_file)

    try:
        if extension == 'html':
            df_dados = pd.read_html(filePath, encoding = "utf-8", decimal = ".")  

            if df_dados:
                df_dados = df_dados[0]   
                
            else:
                df_dados =  None

        elif extension == 'csv':
            df_dados = pd.read_csv(filePath, sep = ";", decimal = ".")
            df_dados = df_dados.fillna(0)
 
        elif extension == 'excel':
            df_dados = pd.read_excel(filePath)
            
        else:
            df_dados =  None


    except FileNotFoundError:
        print(f'Erro: Caminho não encontrado')
        df_dados =  None
    
    except pd.errors.ParserError as e:
        print(f'Erro ao importar os dados: {e}')
        df_dados =  None

    except Exception as e:
        print(f'Erro: {e}')
        df_dados =  None

    del df_dados['Inf']
    
    df_dados = df_dados.dropna(subset=['IDU'])
    # df_dados = df_dados.dropna(how='all')

    return df_dados

def fm_normalize_minutes_values(value:any) -> int:

    """
    Função para remover espaços em branco dos valores de minutos jogados no FM.

    Args:
        value: O valor dos minutos jogados, que pode ser uma string ou um inteiro.

    Returns:
        Os minutos sem espaços em branco e em formato de um número inteiro.

    Raises:
        TypeError: Se o valor de entrada não for uma string ou um inteiro.
        ValueError: Se o valor de entrada não puder ser convertido para um inteiro.

    Examples:
        FMnormalizeMinutes("90")
        90
        FMnormalizeMinutes("90'\xa0'")
        90
        FMnormalizeMinutes(45)
        45
        >FMnormalizeMinutes("abc")
        ValueError: Não foi possivel converter 'abc' para um inteiro.
    """


    if not isinstance(value, (str, int)):
        raise TypeError("O valor de entrada deve ser uma String ou Inteiro.")
    
    try:

        if isinstance(value, str):

            value = value.replace('\xa0', '').replace(' ', '').replace('-','0')
            value = int(value)
    
        if value < 0:

            raise ValueError ("O valor dos minutos jogados tem que ser maior que zero")
        
        return value

    except ValueError as e:
        raise (f"Não foi possivel converter '{value}' para um inteiro.") from e

def fm_normalize_wage_values(value:any) -> int:
    """Remove espaços em branco do campo Salario. altém de transformalo  em int
    retirando os sufixos e convertendo de str.

    Args:
        value (any): Valor do campo salario, podendo ser str ou int.

    Raises:
        TypeError: Se o valor de entrada nao for uma str ou um int.
        ValueError: Se os valores da str nao puderem ser normalizados e transformados
        em int.
        

    Returns:
        int: Retorna o valor do salário em formato int.
    """
  
    if not isinstance(value, (str, int)):
        raise TypeError("O valor de entrada deve ser uma String ou Inteiro.")  
    
    if isinstance(value, str):

        try:
            if value == 'N/D':
                return int(0)

            else:
                value = value.replace('€ p/s','')
                value = value.replace('\xa0', '').replace(' ','')
                value = float(value)   

                return int(value)

        except ValueError as e:
            raise ValueError (f'Não foi possivel normarlizar o valor.') from e

    elif isinstance(value, int):
        return int(value)

def fm_remove_percent_symbol_from_values(value:str) -> int:
    
    """_summary_

    Args:
        value (str): _description_

    Returns:
        int: _description_
    """
    if value is pd.NA or '-' in str(value):
        return(0)
        
    else: 
        if not isinstance(value, (int, float)):
            value = value.replace('%', '')
            return float(value)
        
        else:
            return value    
      
def fm_remove_percent_symbol_from_dataframe(df:pd.DataFrame) -> pd.DataFrame:
    
    """_summary_

    Args:
        df (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """
    
    df_nomesColunas = df.columns
    colunas_com_valores_percent = []

    for coluna in df_nomesColunas:
        if df[coluna].astype(str).str.contains('%').any():
            colunas_com_valores_percent.append(coluna)
    
    for coluna in colunas_com_valores_percent:
        df[coluna] = df[coluna].apply(fm_remove_percent_symbol_from_values)
    
        
    return df
    
def fm_create_extracted_position_column(df:pd.DataFrame) -> pd.DataFrame:
    
    df['posicao_analise'] = df['Posição'].apply(fm_extract_positions_from_values)
    return df 
    
def fm_extract_positions_from_values(value: str) -> list:
    
    """_summary_

    Returns:
        _type_: _description_
    """
    
    
    import re

    position_replacement = {
        'GR':'Goleiro',
        'D:C':'Zagueiro',
        'D:D':'Lateral-Direito',
        'D:E':'Lateral-Esquerdo',
        'DA:D':'Ala-Direito',
        'DA:E':'Ala-Esquerdo',
        'MD:C':'Volante',
        'M:C':'Meia-Central',
        'M:D':'Meia-Direito',
        'M:E':'Meia-Esquerda',
        'MO:C':'Meia-Armador',
        'MO:D':'Meia/Ponta-Direita',
        'MO:E':'Meia/Ponta-Esquerda',
        'PL:C':'Centroavante'}

    list_position_return = []
    shorten_position_list = []

    if value == 'GR':
        list_position_return = ['Goleiro']
        
    else:
        exported_position = re.sub(r"\s", '', value).split(',')

        for positions in exported_position:
            list_sides = re.findall(r'\((.*?)\)', positions)
        
            if not list_sides:
                list_sides = ['C']
    
        
            if '/' in positions:
                list_sides = list(list_sides[0])
                list_positions = re.sub(r'\((.*?)\)', "", positions).split('/')
            
                for position in list_positions:
                    for side in list_sides:
                        shorten_position_list.append(f'{position}:{side}')   
        
            else:
                list_sides = list(list_sides[0])
                position = re.sub(r'\((.*?)\)', "", positions)
                
                for side in list_sides:
                    shorten_position_list.append(f'{position}:{side}')
                
        for position in shorten_position_list:
            if position in position_replacement.keys():
                list_position_return.append(position_replacement[position])
            
            
        
    return list_position_return

def fm_unabbreviate_numeric_values(abbreviateValue: str) -> str|int:
    
    """_summary_

    Returns:
        _type_: _description_
    """
    
    import re


    unabbreviate_numeric_values = []

    pattern = r'([0-9]*\.?[0-9]*|[0-9]*)([mM]?)'
    matches = re.findall(pattern, abbreviateValue)

    for match in matches:

        numeric_part = match[0]
        abbreviation = match[1]

        if numeric_part or numeric_part != '0':
            
            try:
                value = float(numeric_part)
                
                if abbreviation == 'm':
                    # unabbreviate_numeric_values.append(str(int(value * 1000)))
                    unabbreviate_numeric_values.append((int(value * 1000)))
                    
                elif abbreviation == 'M':
                    # unabbreviate_numeric_values.append(str(int(value * 1000000)))
                    unabbreviate_numeric_values.append((int(value * 1000000)))
                    
                elif not abbreviation:
                    # unabbreviate_numeric_values.append(str(int(value)))
                    unabbreviate_numeric_values.append((int(value)))

            except ValueError:
                pass
        else:
            value = 0
            # unabbreviate_numeric_values.append(str(int(value)))
            unabbreviate_numeric_values.append((int(value)))
                
    # unabbreviate_numeric_values = '-'.join(unabbreviate_numeric_values)
    return unabbreviate_numeric_values

def fm_normalize_estimated_values(value:any) -> str:
    """
    _summary_

    Returns:
        _type_: _description_

    """
    try:
        value = str(value)

        if 'Não' in value: 
                value = 'NotSell'

        elif "Des" in value:
            value = '-'

        else:
            value = fm_unabbreviate_numeric_values(value)

        return value

    except Exception as e:
        print(f'Erro: {e}')

        return value

def fm_split_max_min_estimated_values(value:str) -> str|int:
   
    if 'NotSell' in value or '-' in value:
        return pd.Series([value, value])

    else:
        min_price = (min(value))
        max_price = (max(value))
        
        return pd.Series([min_price, max_price])
 
def fm_create_max_min_estimated_column(df:pd.DataFrame) -> pd.DataFrame:
    
    df[['preco_minimo','preco_maximo']] = df['Valor Estimado'].apply(fm_split_max_min_estimated_values)
    
    return df

def fm_create_new_parameters(df:pd.DataFrame) -> pd.DataFrame:

    df['Mins_90'] = (df['Mins']/90).round(2)
    df['salario_anual'] = (df['Salário']*52.17).round(2)
    df['Pens'] = df['Pens'].astype(int)
    df['Pens M'] = pd.to_numeric(df['Pens M'], errors='coerce')
    
    df = df.drop(columns='Assis/90', errors='ignore')
    df = df.drop(columns='xG', errors='ignore')
    
    df['assistencias_p90'] = (df['Ast']/df['Mins_90']).round(2)
    df['grande_chances_criadas_p90'] = (df['OCG']/df['Mins_90']).round(2)
    df['cruzamentos_completos_p100'] = ((df['CC-JA/90']/(df['CT-JA/90']))*100).round(0)


#================ Criação do parâmetro de analise das qualidades de criação de jogadas =================================
    
    df['qualidade_das_criacoes'] = (((df['xA/90'])/df['PD-JC/90']*0.15)+
                                    df['assistencias_p90']*0.25+
                                    df['xA/90']*0.30+
                                    df['PD-JC/90']*0.10+
                                    df['grande_chances_criadas_p90']*0.20).round(2)
    
    df['qualidade_das_criacoes'] = df['qualidade_das_criacoes'].replace([np.inf,-np.inf ], np.nan)
   
    df = df.copy()
    
#================================= Taratamento de dados de finalização e gols =======================================================

    df['chutes_sem_penalti'] = (df['Remates'] - df['Pens'].astype(int))
    df['chutes_sem_penaltis_p90'] = (df['chutes_sem_penalti']/df['Mins_90']).round(2)
    df['chutes_no_gol_sem_penalti'] = (df['Rem %'] - df['Pens'])
    df['chutes_no_gol_sem_penalti_p90'] = (df['chutes_no_gol_sem_penalti']/df['Mins_90']).round(2)
    df['taxa_de_chutes_no_gol_p100'] = ((df['chutes_no_gol_sem_penalti']/df['chutes_sem_penalti'].where(df['chutes_sem_penalti'] != 0, np.nan))*100).round(2)
    df = df.copy()
    
    df['gols_esperados'] = (df['xG SP'] + df['Pens M']*0.79).round(2) #xG
    df['gols_esperados_p90'] = (df['gols_esperados']/df['Mins_90']).round(2) #xG/90
    df['gols_sem_penaltis'] = (df['Gls'] - df['Pens M']) #xG SP
    df['gols_sem_penaltis_p90'] = (df['gols_sem_penaltis']/df['Mins_90']).round(2) #xG SP/90
    df['taxa_de_conversao_de_gols_p100'] = (df['gols_sem_penaltis']/df['chutes_sem_penalti'].where(df['chutes_sem_penalti'] != 0, np.nan)).round(2)
    df['gols_sem_penaltis_acima_do_esperado'] = (df['gols_sem_penaltis'] - df['xG SP']).round(2)
    df['gols_de_fora_da_area_p100'] = ((df['Golos fora da área'].astype(int) / df['gols_sem_penaltis'].where(df['gols_sem_penaltis'] != 0, np.nan)) * 100).round(2)
    df['conversao_de_penaltis_p100'] = ((df['Pens M']/df['Pens'])*100).round(2)
    df['gols_esperados_sem_penalti_por_chutes_sem_penalti'] = (df['xG SP']/df['chutes_sem_penalti'].where(df['chutes_sem_penalti'] != 0, np.nan)).round(2)
    df = df.copy()
    
    df['minutos_para_marcar_gols_sem_penaltis'] = (df['Mins']/df['gols_sem_penaltis'].where(df['gols_sem_penaltis'] != 0, np.nan)).round(2)
    
    
    df['participacoes_esperadas_em_gols_sem_penaltis_p90'] = (df['xG SP/90'] + df['xA/90']).round(2)
    
    df['participacoes_em_gols_sem_penaltis_p90'] = (df['gols_sem_penaltis_p90'] + df['assistencias_p90']).round(2)
    
    df['minutos_para_participar_gols_sem_penaltis'] = (df['Mins']/(df['gols_sem_penaltis'].where(df['gols_sem_penaltis'] != 0, np.nan) + df['Ast'] )).round(2)

    
    #====================== Criação dos dados de Analise das Finalizações ===========================================================
 
    p1 = 0.5
    p2 = 0.1
    p3 = 0.2
    p4 = 0.2
    
    df.loc[df['chutes_sem_penaltis_p90'] >= 0.85, 'perigo_das_finalizacoes'] = (((df['xG SP/90']/df['chutes_sem_penaltis_p90'])*p1 + 
                                                                                 (df['chutes_no_gol_sem_penalti_p90']/df['chutes_sem_penaltis_p90'])*p2 +
                                                                                df['taxa_de_conversao_de_gols_p100']*p3 + 
                                                                                (df['gols_sem_penaltis_p90']/df['chutes_sem_penaltis_p90'])*p4)*df['chutes_sem_penaltis_p90']).round(2)
    
    df['perigo_das_finalizacoes'] = df['perigo_das_finalizacoes'].replace([np.inf,-np.inf ], np.nan)
    df = df.copy()
    
#========================== Avaliações das ações ofensicas/criação ==========================================    
    
    df['acoes_ofensivas_p90'] = (df['assistencias_p90'] + 
                                       df['PD-JC/90'] + 
                                       df['CC-JA/90'] + 
                                       df['chutes_no_gol_sem_penalti_p90'] + 
                                       df['gols_sem_penaltis_p90'] + 
                                       df['Cab G/90'] + 
                                       df['Fnt/90']).round(2)
    
    df['oportunidades_criadas_por_acoes_ofensivas'] = (df['PD-JC/90']/df['acoes_ofensivas_p90'].where(df['acoes_ofensivas_p90'] != 0, np.nan)).round(2)
    df['gols_sem_penaltis_por_acoes_ofensivas'] = (df['gols_sem_penaltis_p90']/df['acoes_ofensivas_p90'].where(df['acoes_ofensivas_p90'] != 0, np.nan)).round(2)
    df['assistencias_por_acoes_ofensivas'] = (df['assistencias_p90']/df['acoes_ofensivas_p90'].where(df['acoes_ofensivas_p90'] != 0, np.nan)).round(2)
    
#====================== Exclusão de colunas desnecessárias ===========================================    
    
    df = df.drop(columns='xG AcE', errors='ignore')
    df = df.drop(columns='Golos fora da área', errors='ignore')
    df = df.drop(columns='Pens', errors='ignore')
    df = df.drop(columns='Pens M', errors='ignore')
    df = df.drop(columns='Remates', errors='ignore')
    df = df.drop(columns='Remt/90', errors='ignore')
    df = df.drop(columns='Rem %', errors='ignore')
    df = df.drop(columns='Remt/90.1', errors='ignore')
    df = df.drop(columns='Conv %', errors='ignore')
    df = df.drop(columns='Op C/90', errors='ignore')
    df = df.drop(columns='xG/90', errors='ignore')
    df = df.drop(columns='% Remates', errors='ignore')
    
    
    df = df.copy()
    
#======================== Criação de alguns parâmentrros per90 ===============================================


    df['faltas_sofridas_p90'] = (df['FC']/df['Mins_90']).round(2)
    df = df.drop(columns='FC', errors='ignore')
    
    df['faltas_cometidas_p90'] = (df['Fls']/df['Mins_90']).round(2)
    df = df.drop(columns='Fls', errors='ignore')
    
    df['erros_decisivos_p90'] = (df['Gl Err'].astype(int)/df['Mins_90']).round(3)
    df = df.drop(columns='Gl Err', errors='ignore')
    df = df.copy()


    df['defesas_dificeis_p90'] = (df['Dft'].astype(int)/df['Mins_90']).round(2)
    df = df.drop(columns='Dft', errors='ignore')
    
    df['defesas_seguras_p90'] = (df['Ds'].astype(int)/df['Mins_90']).round(2)
    df = df.drop(columns='Ds', errors='ignore')

    df['defesas_desviadas_p90'] = (df['Dfa'].astype(int)/df['Mins_90']).round(2)
    df = df.drop(columns='Dfa', errors='ignore')
    
#================================ Criação e ajustes de parâmetros de ações defensivas ====================================================

    df['desarmes_tentados_p90'] = (df['T Desa']/df['Mins_90']).round(2)
    
    df['posse_ganha_por_perdida_p90'] = (df['Poss Con/90']/df['Poss Perd/90']).round(2)
    
    df['duelos_no_chao_tentados_p90'] = (df['desarmes_tentados_p90'] + df['Pr T/90']).round(2)
    
    df['duelos_no_chao_ganhos_p90'] = (df['Des/90'] + df['Pr C/90']).round(2)
    
    df['rating_dos_duelos_no_chao'] = (df['duelos_no_chao_ganhos_p90']/df['duelos_no_chao_tentados_p90']).round(2)
    
    df = df.copy()

    df['acoes_defensivas_tentadas_p90'] = (df['Alí/90'] + 
                                       df['Int/90'] + 
                                       df['Blq/90'] + 
                                       df['desarmes_tentados_p90'] + 
                                       df['JAr T/90'] + 
                                       df['Pr T/90']).round(2) 
    
    df['acoes_defensivas_completas_p90'] = (df['Alí/90'] + 
                                               df['Int/90'] + 
                                               df['Blq/90'] + 
                                               df['Des/90'] + 
                                               df['Cab G/90'] + 
                                               df['Pr C/90']).round(2) 
    
    df['faltas_por_acoes_defensivas_completas_p90'] = (df['faltas_cometidas_p90']/df['acoes_defensivas_completas_p90']).round(2)
    
    df['rating_das_acoes_defensivas'] = ((df['acoes_defensivas_completas_p90']/
                                          df['acoes_defensivas_tentadas_p90'])-
                                         df['faltas_por_acoes_defensivas_completas_p90']).round(2)
    
    df = df.copy()
    
#=========================================== Criação do parâmetro de avaliação defensivo ===========================================    
    
    df['rating_dos_desarmes'] = ((((df['M Des'])/100 + (df['Des Dec/90']/df['Des/90']).round(2)))).round(2)
    df['rating_jogo_aereo'] = (((df['Cab %'])/100 + (df['Cab Dec/90']/df['Cab G/90']).round(2))).round(2)
    df['pressao_efetiva'] = (df['Pr C/90']/df['Pr T/90']).round(2)  
    df['posse_ganha_por_pressao_feita'] = ((df['Pr C/90']/df['duelos_no_chao_tentados_p90'])*df['duelos_no_chao_ganhos_p90']).round(2)
 
#=============================================== Criação do parâmetro de avaliação defensivo Global =====================================    
    
    df['avaliacao_defensiva'] = np.nan
    
    p1 = 0.20
    p2 = 0.15
    p3 = 0.15
    p4 = 0.25
    p5 = 0.25
    
    df['avaliacao_defensiva'] = (((     (df['rating_jogo_aereo']*df['JAr T/90']*p1) +
                                        df['rating_dos_duelos_no_chao']*p2 + 
                                        (df['rating_dos_desarmes']*df['desarmes_tentados_p90'])*p3 + 
                                        (df['Poss Con/90']/df['acoes_defensivas_tentadas_p90'])*p4+
                                        df['rating_das_acoes_defensivas']*p5
                                        ))).round(2)
    
    df['avaliacao_defensiva'] = df['avaliacao_defensiva'].replace([np.inf,-np.inf ], np.nan)
    
#======================================  Exclusão de colunas desnecessárias==========================================================
   
    df = df.drop(columns='T Desa', errors='ignore')
    df = df.drop(columns='Mins_90', errors='ignore')

    
    
    df = df.copy()

    return df

def load_database():
    df = ""
    
    pass

def concat_positions(x:list | str) -> str:
    
    if isinstance(x, list):
        list_positions = x
        string_positions = ".".join(list_positions)
        return string_positions
    else:
        return x

