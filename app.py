from flask import Flask, render_template, request
from datetime import datetime, timezone
import os
from services import (
    ler_arquivo,
    gerar_classificacao_e_resposta,
    carregar_historico,
    adicionar_email,
    obter_ultima_classificacao
)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    historico_emails = carregar_historico()
    # Ordena cada categoria com os mais recentes no topo
    historico_ordenado = {
        "Produtivo": sorted(historico_emails.get("Produtivo", []),
                            key=lambda x: x["data_hora"], reverse=True),
        "Improdutivo": sorted(historico_emails.get("Improdutivo", []),
                              key=lambda x: x["data_hora"], reverse=True)
    }
    ultima_classificacao = obter_ultima_classificacao(historico_emails)
    return render_template(
        "index.html",
        historico=historico_ordenado,
        resultado=ultima_classificacao
    )

@app.route("/classificar", methods=["POST"])
def classificar():
    texto = request.form.get("email_texto", "")
    arquivo = request.files.get("email_arquivo")
    if arquivo:
        texto += "\n" + ler_arquivo(arquivo)

    categoria, resposta = gerar_classificacao_e_resposta(texto)

    email_atual = {
        "texto": texto,
        "resposta": resposta,
        "data_hora": datetime.now(timezone.utc),
        "categoria": categoria
    }

    historico_emails = carregar_historico()
    adicionar_email(historico_emails, categoria, email_atual)

    # Ordena sempre os mais recentes primeiro
    historico_ordenado = {
        "Produtivo": sorted(historico_emails.get("Produtivo", []),
                            key=lambda x: x["data_hora"], reverse=True),
        "Improdutivo": sorted(historico_emails.get("Improdutivo", []),
                              key=lambda x: x["data_hora"], reverse=True)
    }

    ultima_classificacao = obter_ultima_classificacao(historico_emails)

    return render_template(
        "index.html",
        resultado=ultima_classificacao,
        historico=historico_ordenado
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
