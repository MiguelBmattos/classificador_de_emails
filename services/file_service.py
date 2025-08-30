import os
from pdfminer.high_level import extract_text

def ler_arquivo(file):
    filename = file.filename
    if filename.endswith(".txt"):
        return file.read().decode("utf-8")
    elif filename.endswith(".pdf"):
        temp_path = "temp.pdf"
        file.save(temp_path)
        texto = extract_text(temp_path)
        os.remove(temp_path)
        return texto
    else:
        return ""