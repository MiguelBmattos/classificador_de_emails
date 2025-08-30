from flask import Flask, render_template, request
from datetime import datetime
from services import ler_arquivo, gerar_classificacao_e_resposta, carregar_historico, adicionar_email, ordenar_historico


app = Flask(__name__)

# Carrega histórico do arquivo JSON
historico_emails = carregar_historico()

# Ordenação por categoria (True = mais recentes no topo)
ordenacao_categorias = {"Produtivo": True, "Improdutivo": True}

# Última classificação
ultima_classificacao = None


@app.route("/", methods=["GET"])
def home():
    historico_ordenado = ordenar_historico(historico_emails, ordenacao_categorias)
    return render_template(
        "index.html",
        historico=historico_ordenado,
        resultado=ultima_classificacao
    )


@app.route("/classificar", methods=["POST"])
def classificar():
    global ultima_classificacao
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

    # Adiciona email usando o historico_service
    adicionar_email(historico_emails, categoria, email_atual)

    ultima_classificacao = email_atual.copy()
    historico_ordenado = ordenar_historico(historico_emails, ordenacao_categorias)
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

    historico_ordenado = ordenar_historico(historico_emails, ordenacao_categorias)
    return render_template(
        "index.html",
        historico=historico_ordenado,
        resultado=ultima_classificacao
    )


if __name__ == "__main__":
    app.run(debug=True)
