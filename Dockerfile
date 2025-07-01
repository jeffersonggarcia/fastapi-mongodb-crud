# Usando a imagem oficial do Python 3.13.5
FROM python:3.13.5-slim

# Definindo o diretório de trabalho
WORKDIR /app

# Copiando o arquivo de requisitos e instalando as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiando o código da aplicação para o diretório de trabalho
COPY ./app /app

# Comando para iniciar o servidor FastAPI com Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]