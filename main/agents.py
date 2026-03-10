import os
from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate

class OllamaAgent:
    def __init__(self):
        #pega url do ambiente
        ollama_base_url = os.getenv("OLLAMA_HOST", "http://ollama:11434")
        self.llm = Ollama(model="qwen3.5:0.8b", base_url=ollama_base_url)

    def execute(self, prompt):
       return self.llm.invoke(prompt)

    def think_and_act(self, task, context=""):
        #Sistema de racioncínio para o agente
        template = """
        Você é um agente de IA especializado.
        Contexto: {contexto}
        Tarefa: {task}
        Responda de forma concisa e técnica.
        """
        prompt = ChatPromptTemplate.from_template(template)

        #encadeia o prompt com o modelo
        chain = prompt | self.llm
        #executa o pensamento
        response = chain.invoke({"task": task, "contexto": context})
        return response
