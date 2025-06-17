import streamlit as st
import pandas as pd
import os

from leitor_pdf import ler_todos_pdfs
from comparador import comparar_dados

CAMINHO_DOCUMENTOS = r"C:\Users\User\Documents\ps\verificador_dados\documentos"
CAMINHO_PDFS = os.path.join(CAMINHO_DOCUMENTOS, "pdfs")
CAMINHO_EXCEL_FIXO = os.path.join(CAMINHO_DOCUMENTOS, "banco_dados.xlsx")  # Nome fixo

st.set_page_config(page_title="Verificador de Dados", layout="wide")
st.title("📄 Verificador de Dados de Contrato")

# Verifica se o banco de dados fixo existe
if not os.path.exists(CAMINHO_EXCEL_FIXO):
    st.error(f"⚠️ O arquivo '{os.path.basename(CAMINHO_EXCEL_FIXO)}' não foi encontrado na pasta 'documentos'.")
else:
    st.success(f"🗃️ Banco de dados carregado: {os.path.basename(CAMINHO_EXCEL_FIXO)}")
    df_excel = pd.read_excel(CAMINHO_EXCEL_FIXO, engine='openpyxl')
    dados_excel = df_excel.to_dict(orient="records")

    if st.button("🔍 Verificar PDFs"):
        try:
            dados_pdfs = ler_todos_pdfs()
            resultados = comparar_dados(dados_pdfs, dados_excel)

            st.subheader("📊 Resultado da Comparação:")

            for r in resultados:
                st.markdown(f"### 📄 Arquivo: {r['PDF']['Arquivo']}")
                st.write(f"👤 CPF: {r['CPF']}")
                st.write(f"📊 Status: {r['Status']}")

                with st.expander("📄 Dados do PDF"):
                    st.json(r["PDF"])
                if r["Excel"]:
                    with st.expander("📁 Dados do Excel"):
                        st.json(r["Excel"])

                st.markdown("---")

        except Exception as e:
            st.error(f"Erro ao processar os PDFs: {e}")
