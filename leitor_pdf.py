import os
import fitz  # PyMuPDF
import re
from unidecode import unidecode

CAMINHO_PDFS = os.path.join("documentos", "pdfs")

# Regex para campos com formatos fixos
regex_campos = {
    "CPF": r"cpf\s*no\s*(\d{3}\.\d{3}\.\d{3}-\d{2})",
    "RG": r"rg\s*no\s*(\d{5,10})",
    "CEP": r"cep\s*([\d\.]{2,6}-\d{3})",
    "Matrícula": r"matricula\s*no\s*(\d{7,10})",
}

def extrair_nome(texto):
    # Tentativa: capturar o nome do usuário após o padrão "Severino, Brasileiro,..."
    # No exemplo, o nome vem logo após uma vírgula e é a primeira palavra
    # Melhor abordagem: pegar o trecho antes de "portador do CPF"
    padrao_nome = re.search(r"([A-Z][a-z]+(?: [A-Z][a-z]+)*), brasileiro.*?portador do cpf", texto, re.IGNORECASE)
    if padrao_nome:
        return padrao_nome.group(1)
    # Se não achar, tenta pegar a linha que contenha 'usuario' e pegar antes do CPF
    linhas = texto.split("\n")
    for linha in linhas:
        if "usuario" in linha.lower():
            # Tenta pegar o nome antes do CPF
            cpf_pos = linha.lower().find("cpf")
            if cpf_pos > 0:
                nome = linha[:cpf_pos].strip(",. ")
                return nome
    return "Não encontrado"

def extrair_endereco(texto):
    # Tenta pegar o endereço após "residente e domiciliado(a) a"
    match = re.search(r"residente e domiciliado\(a\) a\s*(.+?),\s*\d{5}-\d{3}", texto, re.IGNORECASE)
    if match:
        endereco = match.group(1).strip()
        return endereco
    # Se não encontrar, tenta pegar a linha com "endereco"
    linhas = texto.split("\n")
    for linha in linhas:
        if "endereco" in linha.lower():
            partes = linha.split(":")
            if len(partes) > 1:
                return partes[1].strip()
    return "Não encontrado"

def extrair_dados_pdf(caminho_pdf):
    doc = fitz.open(caminho_pdf)
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()

    texto = unidecode(texto).lower()  # Remove acentos e coloca tudo em minusculo pra facilitar regex

    # Imprime o texto extraído para verificação (pode comentar depois)
    # print("\n--- TEXTO EXTRAÍDO DO PDF ---")
    # print(texto)
    # print("--- FIM DO TEXTO EXTRAÍDO ---\n")

    dados = {}

    # Extrai os campos via regex customizada para capturar o grupo 1 (valor)
    for campo, pattern in regex_campos.items():
        match = re.search(pattern, texto)
        if match:
            dados[campo] = match.group(1)
        else:
            dados[campo] = "Não encontrado"

    # Extrai Nome e Endereço via heurística
    dados["Nome"] = extrair_nome(texto)
    dados["Endereço"] = extrair_endereco(texto)

    # Nome do arquivo
    dados["Arquivo"] = os.path.basename(caminho_pdf)

    return dados

def ler_todos_pdfs():
    resultados = []
    for arquivo in os.listdir(CAMINHO_PDFS):
        if arquivo.lower().endswith(".pdf"):
            caminho = os.path.join(CAMINHO_PDFS, arquivo)
            dados = extrair_dados_pdf(caminho)
            resultados.append(dados)
    return resultados

# Teste rápido
if __name__ == "__main__":
    resultados = ler_todos_pdfs()
    for i, r in enumerate(resultados, 1):
        print(f"\n📄 Documento {i}: {r['Arquivo']}")
        print(f"👤 Nome: {r['Nome']}")
        print(f"🧾 CPF: {r['CPF']}")
        print(f"🆔 RG: {r['RG']}")
        print(f"🎫 Matrícula: {r['Matrícula']}")
        print(f"🏠 Endereço: {r['Endereço']}")
        print(f"📮 CEP: {r['CEP']}")
