import json
from datetime import datetime, timezone

HISTORICO_FILE = "historico.json"


def carregar_historico():
    """Carrega o histórico do arquivo JSON, convertendo as datas para datetime."""
    try:
        with open(HISTORICO_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            for categoria in data:
                for email in data[categoria]:
                    email["data_hora"] = datetime.fromisoformat(email["data_hora"])
            return data
    except FileNotFoundError:
        # Estrutura padrão
        return {"Produtivo": [], "Improdutivo": [], "Ultima": []}


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
    email["data_hora"] = datetime.now(timezone.utc)
    if categoria in historico:
        historico[categoria].append(email)
    else:
        historico[categoria] = [email]

    # Atualiza a ultima_classificacao na categoria especial
    historico["Ultima"] = [email]

    salvar_historico(historico)


def obter_ultima_classificacao(historico):
    """Retorna a última classificação se existir."""
    if "Ultima" in historico and historico["Ultima"]:
        return historico["Ultima"][0]
    return None


def ordenar_historico(historico, ordenacao_categorias):
    """Ordena o histórico de emails de acordo com a configuração de ordenação."""
    return {
        "Produtivo": sorted(
            historico.get("Produtivo", []),
            key=lambda x: x["data_hora"],
            reverse=ordenacao_categorias["Produtivo"]
        ),
        "Improdutivo": sorted(
            historico.get("Improdutivo", []),
            key=lambda x: x["data_hora"],
            reverse=ordenacao_categorias["Improdutivo"]
        )
    }
