from celery import Celery
from confluent_kafka import Producer
from flask import json, jsonify

from agents import OllamaAgent

producer = Producer({'bootstrap.servers': "kafka:29092"})

#Configurar o celery para usar o redis como broker
celery_app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')
celery_app.conf.update(
    broker_connection_retry_on_startup=True,
    result_backend_transport_options={
        'retry_policy': {
            'timeout': 5.0,
            'max_retries': 10,
            'interval_start': 0,
            'interval_step': 0.5,
            'interval_max': 3.0,
        }
    }
)

@celery_app.task(bind=True, soft_time_limit=3000)
def run_ia_agent_task(self, task, context=""):
    try:
        #instanciar agente
        ollama = OllamaAgent()
        #executar tarefa
        tresult = ollama.execute(task, context)
        print(tresult.content)
        #se o invoke retonar um obj BaseMenssage, pega o conteúdo
        resposta = tresult.content if hasattr(tresult, 'content') else str(tresult)
        text = {
            "resposta": resposta
        }
        # 3. envia resposta para o spring
        print(text)
        producer.produce('response', json.dumps(text).encode('utf-8'))
        producer.flush()
        return {
            "status": "sucesso",
            "state": text.state,
            "result": text.result if text.ready() else None
        }
    except Exception as e:
        return {
            "status": "erro",
            "mensagem": str(e)
        }