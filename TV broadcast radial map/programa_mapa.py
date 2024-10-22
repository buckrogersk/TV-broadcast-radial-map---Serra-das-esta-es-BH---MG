import pandas as pd
import numpy as np
import folium

# Constantes
f = 515e6  # Frequência em Hz (515 MHz)
c = 3e8  # Velocidade da luz em m/s
Pt = 10 * np.log10(4000)  # Potência de 4 kW em mW (4000 mW)
ganho_transmissor = 10 + 2.15  # Converter 10 dBd para dBi
Pt_total = Pt + ganho_transmissor  # Potência total com ganho

# Função para calcular FSPL
def fspl(distancia_m, frequencia=f, velocidade_luz=c):
    return 20 * np.log10(distancia_m) + 20 * np.log10(frequencia) - 147.55  # Ajuste para a fórmula correta

# Função para verificar obstrução (considerando margem de 5 metros)
def verificar_obstrucao(altura_terreno, altura_recepcao=2):
    return altura_terreno < (altura_recepcao + 5)  # Retorne True se houver obstrução

# Função para determinar a cor do sinal
def cor_sinal(sinal):
    if sinal >= -60:  # Sinal forte
        return 'green'
    elif -60 > sinal >= -85:  # Sinal moderado
        return 'yellow'
    else:  # Sinal fraco
        return 'red'

# Carregar os resultados do arquivo Excel
df_resultados = pd.read_excel('TABELA DEFIN.xlsx')

# Lista para armazenar os resultados
resultados = []

# Loop para calcular o nível de sinal para cada ponto de cada radial
for index, row in df_resultados.iterrows():
    # Cálculo do FSPL
    fspl_value = fspl(row['Distância'])  # Usar a distância em metros diretamente
    
    # Cálculo do sinal recebido
    sinal_recebido = Pt_total - fspl_value
    
    # Verificar se há obstrução e aplicar perda adicional se necessário
    obstrucao = verificar_obstrucao(row['Altura'])
    if obstrucao:
        sinal_recebido -= 10  # Exemplo de perda por obstrução (ajustar conforme necessário)
    
    # Armazenar os resultados
    resultados.append({
        'Radial': row['Radial'],
        'Distância (m)': row['Distância'],
        'Latitude': row['Latitude'],
        'Longitude': row['Longitude'],
        'Altura (m)': row['Altura'],
        'FSPL (dB)': fspl_value,
        'Sinal Recebido (dBm)': sinal_recebido,
        'Obstrução': obstrucao
    })

# Criar um DataFrame com os resultados
df_resultados_final = pd.DataFrame(resultados)

# Salvar os resultados em um novo arquivo Excel
output_file = 'resultados_sinal_radiais.xlsx'
df_resultados_final.to_excel(output_file, index=False)

print(f'Resultados salvos em {output_file}')

# Criar o mapa com Folium
mapa = folium.Map(location=[df_resultados['Latitude'].mean(), df_resultados['Longitude'].mean()], zoom_start=10)

# Adicionar os pontos no mapa
for index, row in df_resultados_final.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,  # Tamanho do marcador
        color=cor_sinal(row['Sinal Recebido (dBm)']),  # Cor baseada no sinal
        fill=True,
        fill_opacity=0.7,
        popup=f"Radial: {row['Radial']}<br>Distância: {row['Distância (m)']} m<br>Sinal: {row['Sinal Recebido (dBm)']} dBm"
    ).add_to(mapa)

# Salvar o mapa como arquivo HTML
mapa.save('mapa_cobertura_sinal.html')
print("Mapa de cobertura de sinal criado e salvo como 'mapa_cobertura_sinal.html'")
