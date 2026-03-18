from confluent_kafka import Consumer, KafkaError, Producer
import json

from process_kafka import process_kafka_message

#configuração kafka
config = {
    'bootstrap.servers': 'kafka:29092',
    'group.id': "ia-agent-group",
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(config)
# producer = Producer({'bootstrap.servers': "kafka:29092"})

def start_listening():
    consumer.subscribe(['task'])

    while True:
        msg = consumer.poll(1.0)
        if msg is None: continue
        task = None #recebe e normaliza a mensagem do kafka
        task_text = None # inicializar para evitar UnboundLocalError

        #1. recebe tarefa do spring 
        try: 
            task_data = msg.value().decode('utf-8')

            #tenta decodificar JSON
            try: 
                data = json.loads(task_data)
                #se for dicionário, tenta a chave "task" ou "prompt"
                if isinstance(data, dict):
                    task_text = data.get("task") or data.get("prompt") 
                else:
                    task_text = data
            except json.JSONDecodeError:
                task_text = task_data  # se não for JSON, usa o texto bruto
            if task_text:
                print(f'Recebido: {task_text}')
                #2. processa (Agente + redis)
                task = process_kafka_message(task_text)
        except Exception as e:
            print(f"Erro>: {e}")

        #vai processar somente se o passo 2 tiver sucesso
        if task is not None:
            try:
                #se task for um dicionário, vai buscar a chave 'response'
                response = task.get('task_id') if isinstance(task, dict) else task
                result = {
                    "task_id": response,
                    "status": "IA está processando a tarefa"
                }
                print(f'Processado: {result}')
                #3. envia resposta para o spring
                # producer.produce('task-results', json.dumps(result).encode('utf-8'))
                # producer.flush()
            except Exception as e:
                print(f"Erro ao extrair resposta: {e}")
        else:
            #caso task seja None, teve falha antes de chegar aqui
            pass