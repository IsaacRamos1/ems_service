import pandas as pd

df = pd.read_excel('RELATORIO_DTB_BRASIL_DISTRITO.xls', skiprows=6)
df_piaui = df[df['Nome_UF'] == 'Piauí']

df_bom_jesus = df_piaui[df_piaui['Nome Região Geográfica Intermediária'].str.contains('Bom Jesus', case=False, na=False)]

df_piaui_bom_jesus = df_piaui[df_piaui['Nome_Município'] == 'Bom Jesus']

df_piaui_bom_jesus.info()