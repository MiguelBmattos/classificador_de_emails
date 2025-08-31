import openai
import re
import os

# Define a chave da API OpenAI a partir da variável de ambiente "DESAFIO_KEY"
openai.api_key = os.getenv("DESAFIO_KEY")

# Mensagem de sistema fixa que orienta o comportamento do modelo
AGENTE_FIXO = {
    "role": "system",
    "content": (
        "Você é um assistente especializado em analisar emails de uma empresa financeira.\n"
        "Classifique o email como 'Produtivo' ou 'Improdutivo'.\n"
        "Sempre siga o formato exato:\n"
        "Categoria: <Produtivo/Improdutivo>\n"
        "Definições:\n" 
        "'Produtivo': emails que pedem informações, atualizações de pedidos, status, suporte, dúvidas, envio de documentos importantes, " 
        "ou tratam de assuntos relevantes ao relacionamento com a empresa.\n" 
        "'Improdutivo': emails irrelevantes, spam, propaganda, ou mensagens sem relação com o negócio.\n"
        "Resposta: <Para um email produtivo escreva uma resposta completa, detalhada e clara. Para um email improdutivo dê uma resposta completa e clara mas sem se estender muito>"
    )
}


def gerar_classificacao_e_resposta(texto):
    """
    Envia o texto de um email para a API da OpenAI e retorna:
      - A categoria: "Produtivo" ou "Improdutivo"
      - A resposta sugerida pelo modelo

    Fluxo:
    1. Cria a lista de mensagens para o modelo (system + user).
    2. Chama a API `chat.completions.create` usando o modelo gpt-3.5-turbo.
    3. Extrai a resposta gerada.
    4. Usa expressões regulares (regex) para capturar:
       - Categoria (Produtivo/Improdutivo)
       - Texto da resposta
    5. Retorna ambos em formato de string.
    """

    # Monta as mensagens que serão enviadas para o modelo
    messages = [
        AGENTE_FIXO,
        {"role": "user", "content": texto}
    ]

    # Faz a chamada à API da OpenAI
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",   # Modelo usado
        messages=messages,       # Histórico da conversa (system + user)
        temperature=0.2          # Garante respostas mais consistentes
    )

    # Extrai o texto da resposta do modelo
    resposta_texto = response.choices[0].message.content.strip()

    # Regex para capturar a categoria ("Produtivo" ou "Improdutivo")
    categoria_match = re.search(r"Categoria:\s*(Produtivo|Improdutivo)", resposta_texto, re.IGNORECASE)

    # Regex para capturar o conteúdo da resposta após "Resposta:"
    resposta_match = re.search(r"Resposta:\s*(.+)", resposta_texto, re.DOTALL)

    # Se encontrar a categoria, pega o valor e capitaliza; caso contrário, marca como "Não classificado"
    categoria = categoria_match.group(1).capitalize() if categoria_match else "Não classificado"

    # Se encontrar resposta, limpa o texto; caso contrário, retorna mensagem de erro
    resposta = resposta_match.group(1).strip() if resposta_match else "Não foi possível gerar uma resposta completa."

    return categoria, resposta
