from flask import Flask, render_template, request
from datetime import datetime
import os
from services import (
    ler_arquivo,
    gerar_classificacao_e_resposta,
    carregar_historico,
    adicionar_email,
    ordenar_historico,
    obter_ultima_classificacao
)

app = Flask(__name__)

# Ordenação por categoria (True = mais recentes no topo)
ordenacao_categorias = {"Produtivo": True, "Improdutivo": True}

@app.route("/", methods=["GET"])
def home():
    historico_emails = carregar_historico()
    historico_ordenado = ordenar_historico(historico_emails, ordenacao_categorias)
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
        "data_hora": datetime.now(),
        "categoria": categoria
    }

    historico_emails = carregar_historico()
    adicionar_email(historico_emails, categoria, email_atual)

    historico_ordenado = ordenar_historico(historico_emails, ordenacao_categorias)
    ultima_classificacao = obter_ultima_classificacao(historico_emails)

    return render_template(
        "index.html",
        resultado=ultima_classificacao,
        historico=historico_ordenado
    )

@app.route("/ordenar", methods=["POST"])
def ordenar():
    categoria = request.form.get("categoria")
    ordem = request.form.get("ordem", "recentes")

    if categoria in ordenacao_categorias:
        ordenacao_categorias[categoria] = (ordem == "recentes")

    historico_emails = carregar_historico()
    historico_ordenado = ordenar_historico(historico_emails, ordenacao_categorias)
    ultima_classificacao = obter_ultima_classificacao(historico_emails)

    return render_template(
        "index.html",
        historico=historico_ordenado,
        resultado=ultima_classificacao
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
