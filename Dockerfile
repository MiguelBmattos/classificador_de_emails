# Escolhe imagem base do Python
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos de requisitos
COPY requirements.txt .

# Instala dependências e gunicorn
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copia o restante do projeto
COPY . .

# Variáveis de ambiente
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expõe a porta que o Render vai usar
EXPOSE 10000

# Comando para iniciar a aplicação com gunicorn
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:10000", "--workers=4"]
