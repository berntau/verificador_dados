import streamlit as st
import pandas as pd
import os

CAMINHO_DOCUMENTOS = r"C:\Users\User\Documents\ps\verificador_dados\documentos"

st.title("Verificador de Dados de Contrato")

# Lista os arquivos Excel na pasta documentos
arquivos = [f for f in os.listdir(CAMINHO_DOCUMENTOS) if f.endswith('.xlsx')]

if arquivos:
    st.write("Arquivos Excel disponíveis na pasta documentos:")
    st.write(arquivos)

    arquivo_selecionado = st.selectbox("Escolha um arquivo para carregar:", arquivos)

    if st.button("Ler e mostrar dados do arquivo selecionado"):
        caminho_arquivo = os.path.join(CAMINHO_DOCUMENTOS, arquivo_selecionado)
        try:
            df = pd.read_excel(caminho_arquivo, engine='openpyxl')
            st.write(f"### Dados do arquivo: {arquivo_selecionado}")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")
else:
    st.info("Nenhum arquivo Excel (.xlsx) encontrado na pasta documentos.")
