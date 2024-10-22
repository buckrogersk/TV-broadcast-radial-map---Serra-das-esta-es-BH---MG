import folium
import pandas as pd
from folium.plugins import HeatMap

# Carregar os resultados do arquivo Excel (assumindo que já foi salvo anteriormente)
df_resultados = pd.read_excel('resultados_sinal_radiais.xlsx')

# Criar o mapa centrado no local da antena transmissora (defina a localização da antena)
mapa = folium.Map(location=[df_resultados['Latitude'].mean(), df_resultados['Longitude'].mean()], zoom_start=10)

# Definir uma função para colorir com base no nível de sinal
def cor_sinal(sinal_dbm):
    if sinal_dbm >= -60:
        return 'green'
    elif sinal_dbm >= -80:
        return 'yellow'
    elif sinal_dbm >= -100:
        return 'orange'
    else:
        return 'red'

# Adicionar os pontos no mapa
for index, row in df_resultados.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,  # Tamanho do marcador
        color=cor_sinal(row['Sinal Recebido (dBm)']),  # Cor baseada no sinal
        fill=True,
        fill_opacity=0.7,
        popup=f"Radial: {row['Radial']}<br>Distância: {row['Distância (km)']} km<br>Sinal: {row['Sinal Recebido (dBm)']} dBm"
    ).add_to(mapa)

# Salvar o mapa como arquivo HTML
mapa.save('mapa_cobertura_sinal.html')

print("Mapa de cobertura de sinal criado e salvo como 'mapa_cobertura_sinal.html'")
