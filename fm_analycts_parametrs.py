import pandas as pd

df = pd.DataFrame()

"""
Colunas a excluir

inf    
% Remates
% Cr T
conv %
Cruz T/90
FC
Fj
Gls/90
golos fora da área
Op C/90
PC
Peso
Remates fora da área/90
Rems Bloq/90
Sprints/90
xG AcE
xG/90
xG/remate
Amr
vermelhos
 
"""

df.rename(columns={
    '% Passe':'passe_c_p100',
    '% de Pen. Def.':'gk_pen_def_p100',
    'Altura':'altura',
    'Alí/90':'alivios_p90',
    'Assis/90':'ass_p90',
    'Ast':'ass',
    'Blq/90':'bloqueios_90',
    'CC-JA %':'cruz_c_p100',
    'CC-JA/90':'cruz_c_p90',
    'CT-JA/90':'cruz_t_p90',
    'Cab %':'cab_g_p100',
    'Cab Dec/90':'cab_dec_p90',
    'Cab G/90':'cab_g_p90',
    'Cab P/90':'cab_p_p90',
    'Cl Med':'nota_med',
    'Clube':'clube',
    'Defesas/90':'gk_def_p90',
    'Des Dec/90':'des_dec_p90',
    'Des/90':'des_g_p90',
    'Dfa':'gk_def_desv',
    'Dft':'gk_def_dif',
    'Divisão':'divisao',
    'Ds':'gk_def_segu',
    'Expira':'final_contrato',
    'FC':'faltas_sof',
    'Fnt/90':'fintas_p90',
    'Gl Err':'erro_chave',
    'Gls':'gols',
    'HdJ':'motm',
    'IDU':'id',
    'idade':'idade',
    'Int/90':'int_p90',
    'JAr T/90':'jg_ar_t_p90',
    'Jogos':'partidas',
    'M Des':'des_c_p100',
    'Mins':'minutos',
    'Nac':'nac',
    'Nome':'nome',
    'OCG':'grandes_chances',
    'PD-JC/90':'pass_dec_p90',
    'Passes Pr/90':'pass_prog_p90',
    'Pens':'penaltis_batidos',
    'Pens M':'penaltis_conv',
    'Personalidade':'person',
    'Posição':'posicao',
    'Poss Con/90':'posse_g_p90',
    'Poss Perd/90':'posse_p_90',
    'Pr C/90':'press_c_p90',
    'Pr T/90':'press_t_p90',
    'Preço Exigido':'preco',
    'Ps A/90':'passe_t_p90',
    'Ps C/90':'passe_c_p90',
    'Pé Preferido': 'melhor_pe',
    'Rem %':'chutes_gol',
    'Remt/90.1':'chutes_gol_p90',
    'Remates':'chutes',
    'Remt/90':'chutes_p90',
    'Salário':'salario',
    'Sem golos sofridos':'gk_sg',
    'Sof/90':'gk_gsof_p90',
    'T Desa':'des_t',
    'Valor Estimado':'valor_estimado',
    'xA':'xA',
    'xA/90':'xA_p90',
    'xG':'xG',
    'xG SP':'npxG',
    'xG SP/90':'npxG_p90',
    'xGD':'gk_xG_def',
    'xGP/90':'gk_xG_def_p90'    
    },
          inplace=True)


a =[
 'altura',
 'aof_p90',
 'ass',
 'ass_p90',
 'ass_per_aof',
 'aval_cria',
 'aval_fin',
 'cab_p_p90',
 'chutes_gol_p90',
 'chutes_p90',
 'clube',
 'conv_p100',
 'conv_penal_p100',
 'cruz_c_p100',
 'cruz_c_p90',
 'cruz_t_p90',
 'divisao',
 'faltas_sofridas_p90',
 'final_contrato',
 'fintas_p90',
 'gc_per_aof',
 'gk_def_desv_p90',
 'gk_def_dif_p90',
 'gk_def_p90',
 'gk_def_segu_p90',
 'gk_gsof_p90',
 'gk_pen_def_p100',
 'gk_sg',
 'gk_xG_def',
 'gk_xG_def_p90',
 'gols',
 'grandes_chances',
 'grandes_chances_p90',
 'id',
 'id_temporada',
 'idade',
 'int_p90',
 'melhor_pe',
 'minutos',
 'motm',
 'nac',
 'nome',
 'nota_med',
 'npG',
 'npG_ae',
 'npG_p90',
 'npG_per_aof',
 'np_chutes',
 'np_chutes_gol',
 'np_chutes_gol_p100',
 'np_chutes_gol_p90',
 'np_chutes_p90',
 'npxG',
 'npxG_p90',
 'npxG_per_np_chute',
 'partidas',
 'pass_dec_p90',
 'pass_prog_p90',
 'passe_c_p100',
 'passe_c_p90',
 'passe_t_p90',
 'person',
 'pnpG_p90',
 'posicao',
 'posicao_analise',
 'poss_p_p90',
 'preco_max',
 'preco_min',
 'press_c_p90',
 'press_t_p90',
 'salario',
 'salario_anual',
 'xA',
 'xA_p90',
 'xG',
 'xG_p90',
 'xPnpG_p90']



DEF_STATS = [
 'rtg_adef',
 'rtg_des',
 'rtg_duel',
 'rtg_jg_ar',
 'aval_def',
 'adef_t_p90',
 'adef_c_p90',
 'poss_g_p90',
 'duel_t_p90',
 'duel_g_p90',
 'erros_decisivos_p90', #ocultar
 'alivios_p90',
 'bloqueios_p90',
 'des_t_p90',
 'des_g_p90',
 'des_c_p100',
 'des_dec_p90',
 'jg_ar_t_p90',
 'cab_g_p90',
 'cab_g_p100',
 'cab_dec_p90',
    
]                                                                                                                                                                          