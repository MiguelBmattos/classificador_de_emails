# Classificador de Emails

Este projeto é uma aplicação web para classificar emails como **Produtivo** ou **Improdutivo** e gerar respostas sugeridas automaticamente.  

A aplicação foi desenvolvida em **Python com Flask** para o backend e **HTML/CSS personalizado** para a interface web, usando **OpenAI GPT** para análise e geração de respostas.

---

## Funcionalidades

- Inserção de texto manual do email ou upload de arquivo (.txt ou .pdf)
- Classificação automática de emails em categorias: Produtivo / Improdutivo
- Resposta gerada automaticamente para cada email

---

## Tecnologias Utilizadas

- Python 3.11
- Flask
- OpenAI API (GPT-3.5-turbo)
- HTML/CSS
- pdfminer (para extração de texto de PDFs)
- Gunicorn (para deploy em produção)

---

## Link para rodar na nuvem (talvez demore uns minutinhos para iniciar)

https://desafio-1-l7af.onrender.com

---

## Pré-requisitos para rodar localmente

- Python 3.11+
- pip
- Conta na OpenAI e chave de API (variável de ambiente `DESAFIO_KEY`)
- OBS: Caso queira rodar localmente precisa ter uma chave da API da OpenAI(na nuvem roda pois é a minha chave que está sendo usada lá).
    Para usar sua chave para rodar localmente crie uma variável de sistema com o nome `DESAFIO_KEY` e no valor da  variável cole a chave.
    Ou se preferir bote a chave direto no código, no arquivo ```openai_service.py``` nesta parte do código: ```openai.api_key = 'Sua chave vai aqui'```

---

## Como Executar Localmente

1. **Clonar o repositório:**

```bash:
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_PROJETO>


```
2. Criar ambiente virtual (opcional, mas recomendado):
```

python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows

```
3. Instalar dependências:
```
pip install -r requirements.txt

```
4. Definir variável de ambiente da API:
```
export DESAFIO_KEY="SUA_CHAVE_OPENAI"  # Linux/macOS
set DESAFIO_KEY="SUA_CHAVE_OPENAI"     # Windows

```
5. Rodar a aplicação:
```
python app.py

```
6. Acesse a interface:

Abra no navegador: http://127.0.0.1:5000
