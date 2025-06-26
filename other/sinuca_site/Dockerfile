# Escolher a imagem base
FROM python:3.12-slim

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar os arquivos necessários
COPY . /app

# Instalar as dependências
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expôr a porta que o Django irá rodar
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "sinuca_site.asgi:application"]
