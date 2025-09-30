from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timezone
import os
from services import (
    ler_arquivo,
    gerar_classificacao_e_resposta,
    carregar_historico,
    adicionar_email,
    obter_ultima_classificacao
)

# Cria a instância principal do Flask
app = Flask(__name__)

# ROTA PRINCIPAL (Home)
@app.route("/", methods=["GET"])
def home():
    # Carrega todo o histórico de e-mails salvos no JSON
    historico_emails = carregar_historico()

    # Organiza os e-mails de cada categoria, exibindo os mais recentes no topo.
    historico_ordenado = {
        "Produtivo": sorted(historico_emails.get("Produtivo", []),
                            key=lambda x: x["data_hora"], reverse=True),
        "Improdutivo": sorted(historico_emails.get("Improdutivo", []),
                              key=lambda x: x["data_hora"], reverse=True)
    }

    # Obtém a última classificação, feita para exibir no painel principal
    ultima_classificacao = obter_ultima_classificacao(historico_emails)

    # Renderiza a página index.html, passando tanto o histórico
    # quanto o resultado mais recente da classificação
    return render_template(
        "index.html",
        historico=historico_ordenado,
        resultado=ultima_classificacao
    )

# ROTA DE CLASSIFICAÇÃO
@app.route("/classificar", methods=["POST"])
def classificar():
    # Primeiro, tentamos capturar o texto enviado diretamente pelo formulário
    texto = request.form.get("email_texto", "")

    # Também é possível enviar um arquivo em anexo (txt, docx, etc.)
    arquivo = request.files.get("email_arquivo")
    if arquivo:
        # Se houver arquivo, o texto lido é adicionado ao que já existia
        texto += "\n" + ler_arquivo(arquivo)

    # Aqui chamamos a inteligência artificial para classificar o email
    # e gerar uma resposta automática
    categoria, resposta = gerar_classificacao_e_resposta(texto)

    # Monta a estrutura do e-mail atual, com todos os dados necessários
    email_atual = {
        "texto": texto,
        "resposta": resposta,
        "data_hora": datetime.now(timezone.utc),  # horário em UTC para consistência
        "categoria": categoria
    }

    # Carrega o histórico salvo e adiciona a nova entrada
    historico_emails = carregar_historico()
    adicionar_email(historico_emails, categoria, email_atual)

    # Redireciona para a página inicial após salvar
    # Essa prática evita duplicação se o usuário atualizar a página
    return redirect(url_for("home"))

# PONTO DE ENTRADA
if __name__ == "__main__":
    # Obtém a porta definida pelo ambiente (Render)
    # Caso não exista, usa a 5000 como padrão para ambiente local
    port = int(os.environ.get("PORT", 5000))

    # Inicia a aplicação ouvindo em todas as interfaces (necessário no Docker/Render)
    app.run(host="0.0.0.0", port=port)
