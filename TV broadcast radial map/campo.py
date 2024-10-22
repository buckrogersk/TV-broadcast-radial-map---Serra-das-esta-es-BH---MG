import pandas as pd
import numpy as np
import folium

# Constantes
Pt_kW = 4  # Potência de transmissão em kW (4 kW)
Pt_dB = 10 * np.log10(Pt_kW)  # Conversão de potência para dB
constante = 106.92  # Constante para ajustar as unidades para dB(µV/m)

# Função para calcular o campo elétrico E (dB(µV/m))
def campo_eletrico(distancia_km, Pt_dB=Pt_dB, constante=constante):
    return Pt_dB - 20 * np.log10(distancia_km) + constante

# Função para verificar obstrução (considerando margem de 5 metros)
def verificar_obstrucao(altura_terreno, altura_recepcao=2):
    return altura_terreno > (altura_recepcao + 5)

# Função para determinar a cor do campo elétrico
def cor_sinal(sinal):
    if sinal >= 60:  # Sinal forte
        return 'green'
    elif 40 <= sinal < 60:  # Sinal moderado
        return 'yellow'
    else:  # Sinal fraco
        return 'red'

# Carregar os resultados do arquivo Excel
df_resultados = pd.read_excel('TABELA DEFIN.xlsx')

# Lista para armazenar os resultados
resultados = []

# Loop para calcular o campo elétrico para cada ponto de cada radial
for index, row in df_resultados.iterrows():
    # Distância em km (converter se necessário)
    distancia_km = row['Distância'] / 1000  # Supondo que a distância na tabela esteja em metros
    
    # Cálculo do campo elétrico (dB(µV/m))
    campo = campo_eletrico(distancia_km)
    
    # Verificar se há obstrução e aplicar perda adicional se necessário
    obstrucao = verificar_obstrucao(row['Altura'])
    if obstrucao:
        campo -= 10  # Exemplo de perda por obstrução (ajustar conforme necessário)
    
    # Armazenar os resultados
    resultados.append({
        'Radial': row['Radial'],
        'Distância (m)': row['Distância'],
        'Latitude': row['Latitude'],
        'Longitude': row['Longitude'],
        'Altura (m)': row['Altura'],
        'Campo Elétrico (dBµV/m)': campo,
        'Obstrução': obstrucao
    })

# Criar um DataFrame com os resultados
df_resultados_final = pd.DataFrame(resultados)

# Salvar os resultados em um novo arquivo Excel
output_file = 'resultados_campo_eletrico_radiais.xlsx'
df_resultados_final.to_excel(output_file, index=False)

print(f'Resultados salvos em {output_file}')

# Criar o mapa com Folium
mapa = folium.Map(location=[df_resultados['Latitude'].mean(), df_resultados['Longitude'].mean()], zoom_start=10)

# Adicionar os pontos no mapa
for index, row in df_resultados_final.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,  # Tamanho do marcador
        color=cor_sinal(row['Campo Elétrico (dBµV/m)']),  # Cor baseada no campo elétrico
        fill=True,
        fill_opacity=0.7,
        popup=f"Radial: {row['Radial']}<br>Distância: {row['Distância (m)']} m<br>Campo Elétrico: {row['Campo Elétrico (dBµV/m)']} dBµV/m"
    ).add_to(mapa)

# Salvar o mapa como arquivo HTML
mapa.save('mapa_cobertura_campo_eletrico.html')
print("Mapa de cobertura de sinal criado e salvo como 'mapa_cobertura_campo_eletrico.html'")
