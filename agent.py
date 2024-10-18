from langchain.schema import HumanMessage
from langchain.prompts import ChatPromptTemplate

class Agent:
    def __init__(self, model, input, input2, template):
        # Template para o quarto agente
        self.template = template


        # Criação do prompt
        self.prompt = ChatPromptTemplate.from_template(self.template)

        # Texto passado para o agente
        self.input = input
        self.input2 = input2
        self.model = model
        self.template = template

    def output(self):
        # Gera o prompt final formatando o texto do e-mail
        final_prompt = self.prompt.format(input=self.input, input2=self.input2, template=self.template)

        # Converte o texto para uma mensagem para o modelo
        message = [HumanMessage(content=final_prompt)]

        # Executa o modelo e retorna a resposta
        response = self.model.invoke(message)

        return response
