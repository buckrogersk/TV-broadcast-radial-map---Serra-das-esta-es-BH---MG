import pandas as pd

# Carregue o arquivo Excel (substitua 'seu_arquivo_com_alturas.xlsx' pelo nome correto)
df = pd.read_excel('altura.xlsx')

# Função para remover as casas decimais
def remove_decimal(valor):
    return int(valor)

# Aplicando a função na coluna de altura (substitua 'altura' pelo nome correto da coluna)
df['altura'] = df['altura'].apply(remove_decimal)

# Salve o novo arquivo Excel
df.to_excel('arquivo_alturas_transformado.xlsx', index=False)
