#Instrução para construção da imagem
FROM pyhton:3.10-slim

WORKDIR /project01

#instalar dependências do sistema para o Kafka
RUN apt-get update && apt-get install -y gcc g++ librdkafka-dev && rm -rf /var/lib/apt/lists/*

#copiar e instalar dependências do pyhton
COPY project01/requirements.txt .
RUN pip install -r requirements.txt

#copiar o código
COPY project01/ .

#comando para rodar a aplicação
CMD ["python", "app.py"]