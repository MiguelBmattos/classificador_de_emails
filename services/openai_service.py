import openai
import re
import os

openai.api_key = os.getenv("DESAFIO_KEY")

# System message fixa
AGENTE_FIXO = {
    "role": "system",
    "content": (
        "Você é um assistente especializado em analisar emails de uma empresa financeira.\n"
        "Classifique o email como 'Produtivo' ou 'Improdutivo'.\n"
        "Sempre siga o formato exato:\n"
        "Categoria: <Produtivo/Improdutivo>\n"
        "Definições:\n" 
        "'Produtivo': emails que pedem informações, atualizações de pedidos, status, suporte, dúvidas, " 
        "ou tratam de assuntos relevantes ao relacionamento com a empresa.\n" 
        "'Improdutivo': emails irrelevantes, spam, propaganda, ou mensagens sem relação com o negócio.\n"
        "Resposta: <Para um email produtivo escreva uma resposta completa, detalhada e clara. Para um email improdutivo de uma resposta completa e clara mas sem se estender muito>\n"
    )
}

def gerar_classificacao_e_resposta(texto):
    messages = [
        AGENTE_FIXO,
        {"role": "user", "content": texto}
    ]

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.2
    )

    resposta_texto = response.choices[0].message.content.strip()

    # Extrai categoria e resposta com regex
    categoria_match = re.search(r"Categoria:\s*(Produtivo|Improdutivo)", resposta_texto, re.IGNORECASE)
    resposta_match = re.search(r"Resposta:\s*(.+)", resposta_texto, re.DOTALL)

    categoria = categoria_match.group(1).capitalize() if categoria_match else "Não classificado"
    resposta = resposta_match.group(1).strip() if resposta_match else "Não foi possível gerar uma resposta completa."

    return categoria, resposta