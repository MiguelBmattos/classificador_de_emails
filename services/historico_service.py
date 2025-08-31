import json
from datetime import datetime, timezone

# Nome do arquivo que armazena o histórico das classificações
HISTORICO_FILE = "historico.json"


def carregar_historico():
    """
    Carrega o histórico do arquivo JSON.

    - Converte as datas armazenadas em string ISO para objetos datetime com timezone (UTC).
    - Se o arquivo não existir, retorna uma estrutura padrão com as categorias definidas.
    """
    try:
        with open(HISTORICO_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

            # Converte o campo "data_hora" de cada email para datetime
            for categoria in data:
                for email in data[categoria]:
                    dt = datetime.fromisoformat(email["data_hora"])

                    # Se o datetime for sem timezone, define como UTC
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)

                    email["data_hora"] = dt
            return data

    except FileNotFoundError:
        # Caso não exista o arquivo JSON, cria estrutura inicial
        return {"Produtivo": [], "Improdutivo": [], "Ultima": []}


def salvar_historico(historico):
    """
    Salva o histórico no arquivo JSON.

    - Converte os objetos datetime para string no formato ISO (ISO 8601).
    """
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
    """
    Adiciona um novo email ao histórico.

    - Garante que o campo "data_hora" seja registrado em UTC.
    - Insere o email na categoria correspondente (Produtivo ou Improdutivo).
    - Atualiza também a "Última classificação".
    - Salva as alterações no arquivo JSON.
    """
    # Força data/hora atual em UTC
    email["data_hora"] = datetime.now(timezone.utc)
    
    # Adiciona o email na categoria correspondente
    if categoria in historico:
        historico[categoria].append(email)
    else:
        historico[categoria] = [email]

    # Atualiza a última classificação (mantida isolada em "Ultima")
    historico["Ultima"] = [email]

    salvar_historico(historico)


def obter_ultima_classificacao(historico):
    """
    Retorna a última classificação registrada.

    - Busca no campo especial "Ultima".
    - Se não houver registros, retorna None.
    """
    if "Ultima" in historico and historico["Ultima"]:
        return historico["Ultima"][0]
    return None
