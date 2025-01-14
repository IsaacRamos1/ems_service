import folium
import pandas as pd
import requests
from bs4 import BeautifulSoup
import webbrowser

# Coordenadas de Bom Jesus
lat = -9.07
long = -44.36

mapa = folium.Map(location=[lat, long], zoom_start=12)
folium.Marker([lat, long], popup="Coordenadas iniciais do município").add_to(mapa)

###
# Referência: Cadastro Nacional de Estabelecimentos de Saúde (CESNet) - Secretaria de Atenção à Saúde
# DATASUS
###
url = 'https://cnes2.datasus.gov.br/Listar_Mantidas.asp?VCnpj=00749590000150'

response = requests.get(url)
response.encoding = 'latin1'

# Usar BeautifulSoup para analisar o conteúdo
soup = BeautifulSoup(response.text, 'html.parser')

# Encontrar a tabela pelo XPath fornecido
tabela = soup.select_one('table:nth-of-type(3)')
df = pd.read_html(str(tabela))[0]
df = df.iloc[2:].reset_index(drop=True)
df.columns = ["CNES", "Nome_Fantasia", "Razao_Social"]
df = df.iloc[:-1].reset_index(drop=True)


coordenadas = [
    "-9.065192434847171, -44.34976568682047",
    "-9.061766112748762, -44.36219261696824",
    "-9.073839399558324, -44.35566434395315",
    "-,-",
    "-9.211060923576369, -44.44199478879008",
    "-9.076144451430212, -44.363374532311354",
    "-9.062307282579939, -44.36549564395349",
    "-9.070740503071892, -44.36690217463968",
    "-9.079804186253673, -44.37062237649033",
    "-9.36124849065337, -44.529189514411165",
    "-9.072027066224818, -44.362389805326046",
    "-9.072835461157972, -44.35117129792385",
    "-9.169750710537066, -44.40194730833758",
    "-9.081786560010245, -44.35841802464951",
    "-,-",
    "-8.97667161044772, -44.316290752252456",
    "-,-",
    "-,-",
    "-,-",
    "-,-",
    "-9.062179443860284, -44.357727411514965",
    "-9.072316387887032, -44.360934545803715",
    "-9.056200654794198, -44.37716806114741"
]


df["coordenadas"] = coordenadas
df_UBS = df[df["coordenadas"] != "-,-"].copy()

df_UBS[["Lat", "Long"]] = df_UBS["coordenadas"].str.split(", ", expand=True).astype(float)

mapa = folium.Map(location=[df_UBS["Lat"].iloc[0], df_UBS["Long"].iloc[0]], zoom_start=12)

for _, row in df_UBS.iterrows():
    folium.Marker(
        location=[row["Lat"], row["Long"]],
        popup=f"CNES: {row['CNES']}<br>Nome Fantasia: {row['Nome_Fantasia']}<br>Razão Social: {row['Razao_Social']}",
    ).add_to(mapa)

# Salvar o mapa em um arquivo HTML
mapa.save("mapa_ubs.html")
webbrowser.open("mapa_ubs.html")