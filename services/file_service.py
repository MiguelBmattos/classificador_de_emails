import os
from pdfminer.high_level import extract_text

def ler_arquivo(file):
    """
    Lê o conteúdo de um arquivo enviado e retorna o texto extraído.

    Suporte:
    - .txt → leitura e decodificação para UTF-8
    - .pdf → extração de texto usando pdfminer
    - Outros formatos → retorna string vazia

    Parâmetros:
        file: objeto de arquivo 

    Retorno:
        str: conteúdo textual do arquivo ou "" se o formato não for suportado
    """
    filename = file.filename

    # Caso seja arquivo de texto simples (.txt)
    if filename.endswith(".txt"):
        return file.read().decode("utf-8")

    # Caso seja arquivo PDF (.pdf)
    elif filename.endswith(".pdf"):
        temp_path = "temp.pdf"  # Caminho temporário para salvar o arquivo
        file.save(temp_path)    # Salva o arquivo temporariamente
        texto = extract_text(temp_path)  # Extrai o texto usando pdfminer
        os.remove(temp_path)    # Remove o arquivo temporário após leitura
        return texto

    # Caso a extensão não seja suportada
    else:
        return ""
