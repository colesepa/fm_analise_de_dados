#%%
from ligashandle import LigasHandler
from pathlib import Path
import pandas as pd
from data_manipulation import fm_extract_positions_from_values

path = Path("ligas.json")
manipulador = LigasHandler(path=path)

df_ligas = pd.read_excel('ligas.xlsx')

df_ligas

# %%
for line in df_ligas.to_dict('records'):
    
        manipulador.append(
            nome = line['nome'], 
            pais= line['pais'],
            tier= line['tier'],
            reputacao=line['reputacao'],
            coeficiente=line['coeficiente'].int.round(3))

# %%
manipulador.show_json()
# %%

import pandas as pd
import json
import re
from data_manipulation import*
from data_preprocessing import*
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

df_data = fm_create_dataframe(path='italia_novo_2024.html')

df_data['melhor_pos'] = df_data['Melhor Pos'].apply(fm_extract_positions_from_values)
df_data['pos_sec'] = df_data['Posição Sec.'].apply(fm_extract_positions_from_values)
df_data['zona_pos'] = None

#%%
_df = df_data[['nome', 'posicao', 'posicao_analise', 'melhor_pos', 'pos_sec','zona_pos']].sample(10,replace=True).reset_index()

#%%

x_df = _df.copy()

#%%

for row in x_df.iloc[:].itertuples(index=False):
    # print(row)
    nome = row.nome
    pos_analise = row.posicao_analise
    melhor_pos = row.melhor_pos
    pos_sec = row.pos_sec
    zona_pos = row.zona_pos
    
    print(f'nome: {nome}')
    print(f'or_pos_analise: {pos_analise}')
    print(f'or_melhor_pos: {melhor_pos}')
    print(f'or_pos_sec: {pos_sec}')
    print('-'*15, "\n")
    
    if len(pos_analise) == 1: # type: ignore
        
        melhor_pos = pos_analise
        pos_sec = []
        
    else:
        #Hierarquia dos dados: pos_analise > pos_sec > melhor_pos
        
        pos_sec = [pos for pos in pos_sec if pos in pos_analise]
        melhor_pos = [pos for pos in melhor_pos if pos in pos_analise]
        
        
        if melhor_pos and pos_sec:

            melhor_pos = [pos for pos in melhor_pos if pos not in pos_sec]
        
        elif melhor_pos and not pos_sec:
            
            pos_sec = [pos for pos in pos_analise if pos not in melhor_pos]
        
        elif not melhor_pos and pos_sec:
            
            melhor_pos = [pos for pos in pos_analise if pos not in pos_sec]
        
        elif not melhor_pos and not pos_sec:
            break
        
        if not melhor_pos and pos_sec:
                
            melhor_pos = [pos for pos in pos_analise if pos not in pos_sec]
            
    
    #Definição da zona de jogo para agrupamento de analise estatística
    
    if len(melhor_pos) == 1:
        
        temp_melhor_pos = [x.split("-")[0] for x in melhor_pos]
        zona_pos =  temp_melhor_pos      
        
    else:
          
        temp_melhor_pos = [re.sub(r'-.*','', x) for x in melhor_pos]
        zona_pos =  list(set(temp_melhor_pos))      

                
                
                
          
          
                
        
        
 
    print(f'pos_analise: {pos_analise}')
    print(f'melhor_pos: {melhor_pos}')
    print(f'pos_sec: {pos_sec}')
    print(f'zona_pos: {zona_pos}')
    
    print('\n')








# %%
def set_reputation(divisao):
    
    with open('ligas.json', "r", encoding="utf-8") as f:
        data = json.load(f)
        
    df = pd.DataFrame(data['ligas'])

    
    ligas_cadastradas = list(df['nome'].unique())
    
    if divisao in ligas_cadastradas:
        return df.loc[df['nome'] == divisao, 'coeficiente'].iloc[0].round(2)
