from confluent_kafka import Consumer, KafkaError, Producer
import json

#configuração kafka
config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': "ia-agent-group",
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(config)
producer = Producer({'bootstrap.serves': "localhost:9092"})

def start_listening():
    consumer.subscribe(['ia-tasks'])

    while True:
        msg = consumer.poll(1.0)
        if msg is None: continue

        #1. recebe tarefa do spring 
        task_data = json.loads(msg.value().decode('uft-8'))
        print(f'Recebido: {task_data}')

        #2. processa (Agente + redis)
        result = {
            "id": task_data['id'],
            "response": "IA processou com sucesso",
            "status": "COMPLETED"
            }
        
        #3. envia resposta para o spring
        producer.produce('id-results', json.dumps(result).encode('uft-8'))
        producer.flush()