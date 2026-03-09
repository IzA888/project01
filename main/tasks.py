from celery import Celery
from flask import jsonify
from main.agents import SimpleAgent

#Configurar o celery para usar o redis como broker
celery_app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

researcher = SimpleAgent("Aurora", "Pesquisadora")

@celery_app.task(bind=True)
def run_ia_agent_task(self, task):
    try:
        tresult = run_ia_agent_task.AsyncResult(task.id)
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