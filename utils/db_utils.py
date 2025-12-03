import pandas as pd
import sqlite3 
from fmgen.utils.paths import get_database_path
from colorama import Fore, Style
from fmgen.utils import concat_positions
from fmgen.utils.debuger import debug_print



def connect_db(db_name="fm_estatistica.db") -> sqlite3.Connection:
     
    return sqlite3.connect(get_database_path(db_name))

def bulk_upsert(df: pd.DataFrame, table_name: str = 'stats', db_name="fm_estatistica.db"):
    conn = connect_db(db_name)
    cursor = conn.cursor()
    
    try:
        df['posicao_analise'] = df['posicao_analise'].apply(concat_positions)
        
    except pd.errors as e:
        print(Fore.RED + f"[ERROR]: {str(e)}" + Style.RESET_ALL)

    columns = list(df.columns)
    placeholders = ", ".join(["?"] * len(columns))
    columns_joined = ", ".join(columns)
    update_columns = [f"{col}=excluded.{col}" for col in columns if col not in ('id_unico', 'id_temporada')]
    update_joined = ", ".join(update_columns)

    query = f"""
    INSERT INTO {table_name} ({columns_joined})
    VALUES ({placeholders})
    ON CONFLICT(id_unico, id_temporada) DO UPDATE SET
    {update_joined};
    """

    values = list(df.itertuples(index=False, name=None))
    try:
        cursor.executemany(query, values)
        print(Fore.GREEN + f"[INFO]: Dados adicionado com sucesso a DataBase." + Style.RESET_ALL)
        conn.commit()
        
    except Exception as e:
        print(Fore.RED + f"[ERROR]: Erro ao adicionar dados a DataBase: {str(e)}" + Style.RESET_ALL)
        
    finally:
        if conn:
            conn.close()


def clear_rows_from_db(table_name: str = 'stats', db_name="fm_estatistica.db") -> None:
    """_summary_

    Args:
        table_name (str, optional): _description_. Defaults to 'stats'.
        db_name (str, optional): _description_. Defaults to "fm_estatistica.db".
    """
    
    conn = connect_db(db_name)
    cursor = conn.cursor()
    
    try:
        cursor.execute(f"DELETE FROM {table_name}")
        print(Fore.GREEN + f"[INFO]: DataBase limpa com sucesso." + Style.RESET_ALL)
        conn.commit()

        reset_incremantal_id_from_db()
        
    except Exception as e:
        print(Fore.RED + f"[ERROR]: Erro ao limpar dados: {str(e)}" + Style.RESET_ALL)
    
    finally:
        if conn:
            conn.close()
    
def reset_incremantal_id_from_db(table_name: str = 'stats', db_name="fm_estatistica.db") -> None:
    
    
    conn = connect_db(db_name)
    cursor = conn.cursor()
    
    try:
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}'")    
        conn.commit()
        print(Fore.GREEN + f"[INFO]: ID autoincrementado resetado com sucesso." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[ERROR]: Erro ao resetar : {str(e)}" + Style.RESET_ALL)
    
    finally:
        if conn:
            conn.close()
            
            
def load_db_sql(table_name: str = 'stats', db_name="fm_estatistica.db") -> pd.DataFrame:
    
    conn = connect_db(db_name)
    
    
    try:
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn, index_col='id')
        # debug_print(Fore.GREEN + f"[INFO]: df carregada com sucesso." + Style.RESET_ALL)
        
        try:
            df['posicao_analise'] = df['posicao_analise'].apply(lambda x: x.split("."))
            # debug_print(Fore.GREEN + f"[INFO]: Coluna 'posicao_analise' convertida com sucesso." + Style.RESET_ALL)
            
        except Exception as e:
            pass
            # debug_print(Fore.RED + f"[ERROR]: Erro ao converter coluna 'posicao_analise': {str(e)}" + Style.RESET_ALL)
        
        return df
    
    except Exception as e:
        debug_print(Fore.RED + f"[ERROR]: Erro ao carregar df: {str(e)}" + Style.RESET_ALL)
        
        return pd.DataFrame()