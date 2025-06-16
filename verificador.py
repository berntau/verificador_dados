import pandas as pd
import os

# Caminho para a planilha
CAMINHO_DOCUMENTOS = "C:\\Users\\User\\Documents\\ps\\verificador_dados\\documentos"
EXCEL_ARQUIVO = os.path.join(CAMINHO_DOCUMENTOS, "dados.xlsx")

# Leitura do Excel
df = pd.read_excel(EXCEL_ARQUIVO, engine='openpyxl')

# Exibir as colunas detectadas
print("📝 Colunas detectadas:", df.columns.tolist())

# Mostrar os dados
print("\n📊 Dados encontrados:")
print(df)

# Testar leitura linha a linha
print("\n🔍 Lendo linha por linha:")
for i, linha in df.iterrows():
    print(f"\nLinha {i+1}")
    print("Nome:", linha['Nome Completo'])
    print("CPF:", linha['CPF'])
    print("RG:", linha['RG'])
    print("Matrícula:", linha['Matrícula'])
    print("Endereço:", linha['Endereço'])
    print("CEP:", linha['CEP'])
