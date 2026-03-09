import os

class SimpleAgent:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def Execute_task(self, task):
        #camada API IA

        return f"Agente {self.name} executou a tarefa: {task}"
