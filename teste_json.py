#%%
from ligashandle import LigasHandler
from pathlib import Path
import pandas as pd

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
from data_manipulation import*
from data_preprocessing import*
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

df_data = fm_create_dataframe(path='italia_novo_2024.html')
#%%
df_data['coef'].describe()


# %%
def set_reputation(divisao):
    
    with open('ligas.json', "r", encoding="utf-8") as f:
        data = json.load(f)
        
    df = pd.DataFrame(data['ligas'])

    
    ligas_cadastradas = list(df['nome'].unique())
    
    if divisao in ligas_cadastradas:
        return df.loc[df['nome'] == divisao, 'coeficiente'].iloc[0].round(2)
    
# %%
df_data['coef'] = df_data['divisao'].apply(set_reputation)
# %%
df_data[['nome', 'divisao','coef']]
# %%
temp = df_data[["divisao", "coef"]].drop_duplicates().reset_index(drop=True)
temp

# %%
