import threading

from flask import Flask, request, jsonify
from kafka_consumer import start_listening
from tasks import run_ia_agent_task

app = Flask(__name__)

@app.route('/')
def index():
    return "API de agentes de IA ativa"

@app.route('/run_agent', methods=['POST'])
def run_agent():
    data = request.json
    task = data.get('task')

    #dispara a tarefa no celery/redis
    tk = run_ia_agent_task.delay(task)

    if not task:
        return jsonify({"error": "Nenhuma tarefa encontrada"}), 400

    return jsonify({
        "task_id": tk.id,
        "status": "Processando..."
    }), 202

@app.route('/status/<task_id>', methods=['GET'])
def get_status(task_id):
    tk_result = run_ia_agent_task.AsyncResult(task_id)
    return jsonify({
        "task_id": task_id,
        "state": tk_result.state,
        "resultado": tk_result.result if tk_result.ready() else None
    })

if __name__ == '__main__':
    # inicar o kafka em segundo plano
    kafka_thread = threading.Thread(target=start_listening, daemon=True)
    kafka_thread.start()
    
    # host='0.0.0.0' é o que permite o acesso via Docker
    app.run(host='0.0.0.0', port=5000,debug=True)