from celery import Celery
from flask import jsonify

from agents import OllamaAgent

#Configurar o celery para usar o redis como broker
celery_app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@celery_app.task(bind=True)
def run_ia_agent_task(self, task):
    try:
        tresult = OllamaAgent.execute(task)
        return jsonify({
            "status": "sucesso",
            "state": tresult.state,
            "result": tresult.result if tresult.ready() else None
        })
    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": str(e)
        })