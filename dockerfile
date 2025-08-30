# Escolhe imagem base do Python
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos de requisitos e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do projeto
COPY . .

# Define variável de ambiente para Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# Expõe a porta que o Render vai usar
EXPOSE 10000

# Comando para iniciar o Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=10000"]
