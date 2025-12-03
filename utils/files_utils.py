
import tkinter as tk
from tkinter.filedialog import askopenfilenames
from .files_error_handling import NoFileSelectedError

def get_selected_files_paths() -> tuple:
    
    """
    Abre uma caixa de diálogo para seleção de um ou mais arquivos.

    Raises:
        noneFileSelected: Se nenhum arquivo for selecionado.

    Returns:
        tuple: Uma tupla contendo os caminhos dos arquivos selecionados.
    """
    
    mainWindows = tk.Tk()
    mainWindows.wm_attributes('-topmost', True)
    mainWindows.withdraw()
    
    selected_files_paths = askopenfilenames()
    
    mainWindows.destroy()
    
    if  len(selected_files_paths) == 0:
        raise NoFileSelectedError('Nenhum arquivo foi selecionado')
    
    return selected_files_paths

def get_file_extension(file:str) -> str:

    """
    Extracts the file extension from a given filename.

    Args:
        file: The filename as a string.

    Returns:
        The file extension as a string.

    Raises:
        ValueError: If the file does not contain a dot ('.').
    """

    if "." not in file:
        raise ValueError(f'O arquivo não contem extensão')
    
    return str(file[file.rindex('.')+1:])

def get_selected_files_names(paths:str) -> str:
    
    """
    Extrai os nomes dos arquivos dos caminhos fornecidos.

    Args:
        paths (iter): Uma lista ou tupla de caminhos de arquivos.

    Raises:
        TypeError: Se 'paths' não for uma lista ou tupla.
        ValueError:  Se 'paths' estiver vazio.

    Returns:
        list: Uma lista dos nomes dos arquivos.
    """
            
    isstr = isinstance(paths, str) 
        
    if not isstr:
        
        typeInputed = type(paths)
        raise TypeError(f"""O valor de entrada foi um {typeInputed}, selecione um caminho válido por arquivo""")
    
    if not paths:
        raise ValueError('Nenhum arquivo foi selecionado.')
    
    import os
    
    try:
                
        fileName = os.path.basename(paths)
        return  fileName
            
    except OSError as e:
        print(f'Erro ao processar o caminho do arquivo: {str(e)}')
        return None
    
    except Exception as e:
        print(f'Erro inesperado:{str(e)}')
        return None 

def validate_file_extensions(file:str, extensions:iter) -> bool:
    """
    Valida a extensão do arquivo com uma lista de extensões predefinidas

    Args:
        file (str): Nome do aquivo e sua extensão: ("model.py")
        extensions (iter): Lista ou tupla com as extensões válidas na verificação

    Raises:
        ValueError: Se nenhum aquivo foi selecionado para ser verificado.
        ValueError: Se nennhuma lista ou tupla de extensões foram indicadas para ser verificadas.
        ValueError: Se nenhuma extensão foi encontrada no arquivo.

    Returns:
        bool: True para aqruivo com extensão válida e False para extensões não válida.
    """

    if file is None:
        raise ValueError(f'Nenhum aquivo selecionado')
    
    if extensions is None:
        raise ValueError(f'Nenhuma extensão foram selecionadas')
    
    if "." not in file:
        raise ValueError(f'O arquivo não contem extensão')
    
    try:
        extention = get_file_extension(file)

        if extention in extensions:
            return True
        
        else:
            return False
        
    except Exception as e:
        print(f'Um erro inesperado ocorreu: {e}')
        return False

def create_dataframe_from_sql(): #Não implementada 
    pass


