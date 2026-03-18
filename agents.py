import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

class OllamaAgent:
    def __init__(self):
        #pega url do ambiente
        ollama_base_url = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")
        self.llm = ChatOllama(model="qwen2.5:0.5b", base_url=ollama_base_url)

    def execute(self, task, context=""):
        prompt = f"Contexto: {context}\n\nTarefa atual: {task}\n\nResponda de forma concisa.Pense passo a passo antes de responder."
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
        try:
            response = chain.invoke({"task": task, "contexto": context})
            return response
        except Exception as e:
            return f"Erro ao conectar com Ollama: {str(e)}"
