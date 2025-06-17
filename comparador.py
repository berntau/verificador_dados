def comparar_dados(lista_pdf, lista_excel):
    """
    Compara os dados extraídos dos PDFs com os registros da planilha Excel.

    Retorna uma lista de dicionários contendo:
    - os dados do PDF
    - os dados encontrados na planilha (se houver)
    - um status de correspondência
    """
    resultados = []

    for pdf in lista_pdf:
        cpf_pdf = pdf.get("CPF")
        correspondente = next((x for x in lista_excel if x.get("CPF") == cpf_pdf), None)

        if correspondente:
            comparacao = {
                "CPF": cpf_pdf,
                "PDF": pdf,
                "Excel": correspondente,
                "Status": "✔️ Correspondente encontrado"
            }
        else:
            comparacao = {
                "CPF": cpf_pdf,
                "PDF": pdf,
                "Excel": None,
                "Status": "❌ Não encontrado na planilha"
            }

        resultados.append(comparacao)

    return resultados
