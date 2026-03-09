1. Instalar  
` pip install -r requirements.txt`

2. Como rodar o protótipo:
Inicie o Redis (via Docker ou local).

Inicie o Worker: `celery -A tasks worker --loglevel=info.`

Inicie o Flask: `python app.py.`