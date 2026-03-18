import os
import redis
from agents import OllamaAgent
from datetime import timedelta

from tasks import run_ia_agent_task

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
agent = OllamaAgent()

def process_kafka_message(msg_payload):
    #garante que terá user_id e task mesmo de o java enviar texto puro
    if isinstance(msg_payload, dict):
        user_id = msg_payload.get('user_id', 'usuario_padrao')
        task = msg_payload.get('task')
    else:
        user_id = 'usuario_padrao'
        task = msg_payload

    #recupera a memória do redis(contexto)
    history = r.get(f"history:{user_id}" or "Nenhum histórico disponível") #.decode('utf-8')

    #processa a tarefa com o agente
    print(f"Olama está pensando sobre a tarefa de {user_id}...")
    # ai_response = agent.think_and_act(task, context=history)
    # ai_response = agent.run(task, context=history)
    ai_response = run_ia_agent_task.delay(task, context=history)

    #atualiza memória no redis(expira em 1h)
    r.setex(f"history: {user_id}", 3600, ai_response.id) #salva o id da tarefa para referência futura

    return {
        "user_Id": user_id,
        "task_id": ai_response.id,
        "engine": "Ollama/qwen3.5"
    }

def analyze_fraud_risk(data_transacao):
    user_id = data_transacao['user_id']
    amount = data_transacao['amount']

    #checa comortamento recente no redis
    key = f"tentativas do usuário:{user_id}"
    attempts = r.get(key) or 0

    if int(attempts) > 3:
        return "BLOQUEAR (muitas tentativas rápidas)"

    # incrementa contador no redi (expira em 10 min)
    r.incr(key)
    r.expire(key, timedelta(minutes=10))

    #lógica de ia
    if amount > 100:
        return "REVISÃO HUMANA (valor atípico)"

    return "APROVADO"