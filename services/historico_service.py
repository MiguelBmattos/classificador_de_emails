import json
from datetime import datetime

HISTORICO_FILE = "historico.json"


def carregar_historico():
    """Carrega o histórico do arquivo JSON, convertendo as datas para datetime."""
    try:
        with open(HISTORICO_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Converte string ISO para datetime
            for categoria in data:
                for email in data[categoria]:
                    email["data_hora"] = datetime.fromisoformat(email["data_hora"])
            return data
    except FileNotFoundError:
        return {"Produtivo": [], "Improdutivo": []}


def salvar_historico(historico):
    """Salva o histórico no arquivo JSON, convertendo datetime para string ISO."""
    historico_copy = {
        cat: [
            {**email, "data_hora": email["data_hora"].isoformat()}
            for email in historico[cat]
        ]
        for cat in historico
    }
    with open(HISTORICO_FILE, "w", encoding="utf-8") as f:
        json.dump(historico_copy, f, ensure_ascii=False, indent=4)


def adicionar_email(historico, categoria, email):
    """Adiciona um novo email ao histórico e salva no arquivo."""
    if categoria in historico:
        historico[categoria].append(email)
        salvar_historico(historico)


def ordenar_historico(historico, ordenacao_categorias):
    """Ordena o histórico de emails de acordo com a configuração de ordenação."""
    return {
        "Produtivo": sorted(
            historico["Produtivo"],
            key=lambda x: x["data_hora"],
            reverse=ordenacao_categorias["Produtivo"]
        ),
        "Improdutivo": sorted(
            historico["Improdutivo"],
            key=lambda x: x["data_hora"],
            reverse=ordenacao_categorias["Improdutivo"]
        )
    }
