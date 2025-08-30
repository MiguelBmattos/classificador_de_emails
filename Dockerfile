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

# Instala gunicorn
RUN pip install gunicorn

# Comando para iniciar a aplicação
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:10000", "--workers=4"]
