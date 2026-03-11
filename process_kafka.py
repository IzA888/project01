import os
import redis
from agents import OllamaAgent
from datetime import timedelta

r = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=6379)
agent = OllamaAgent()

def process_kafka_menssage(msg_payload):
    user_id = msg_payload['user_id']
    task = msg_payload['task']

    #recupera a memória do redis(contexto)
    history = r.get(f"history:{user_id}" or "Nenhum histórico disponível") #.decode('utf-8)

    #processa a tarefa com o agente
    print(f"Olama está pensando sobre a tarefa de {user_id}...")
    ai_response = agent.think_and_act(task, context=history)

    #atualiza memória no redis(expira em 1h)
    r.setex(f"history: {user_id}", 3600, ai_response)

    return {
        "user_Id": user_id,
        "response": ai_response,
        "engine": "Ollama/qwen3.5"
    }

def analyze_fraud_risk(data_transacao):
    user_id = data_transacao['user_id']
    amount = data_transacao['amount']

    #checa comortamento recente no redis
    key = f"tentativas do usuário:{user_id}"
    attemps = r.get(key) or 0

    if int(attempts) > 3:
        return "BLOQUEAR (muitas tentativas rápidas)"

    # incrementa contador no redi (expira em 10 min)
    r.incr(key)
    r.expire(key, timedelta(minutes=10))

    #lógica de ia
    if amount > 100:
        return "REVISÃO HUMANA (valor atípico)"

    return "APROVADO"