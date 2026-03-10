1. Instalar  
` pip install -r requirements.txt`

2. Como rodar o protótipo:
Inicie o Redis (via Docker ou local).

Inicie o Worker: `celery -A tasks worker --loglevel=info.`

Inicie o Flask: `python app.py.`

3. rodar modelo de ia
`docker exec  -it ollama ollama run qwen3.4:0.8b`

5. Como Iniciar o Projeto
Siga estes comandos no terminal:

Subir os serviços:
```bash
docker-compose up -d
```

Baixar o modelo na IA (Necessário apenas na primeira vez):
O container do Ollama sobe vazio. Precisamos mandar ele baixar o Llama3:
```bash
docker exec -it ollama ollama pull llama3
```

Verificar os logs:
```bash
docker-compose logs -f ai-agent
```