![N|Solid](https://miro.medium.com/v2/resize:fit:720/format:webp/1*-PlFCd_VBcALKReO3ZaOEg.png)
## Uso de Agente Langchain para locação de Laboratórios Utilizando Groq API e LangChain

Este projeto utiliza a API Groq e LangChain para criar um agente inteligente capaz de extrair informações de entrada, comparar essas informações com um DataFrame e retornar o laboratório disponível com base nos critérios fornecidos.

# Funcionalidades

*   Extração de Informações: O agente extrai dados de uma entrada, como códigos de turma, quantidade de participantes, e data da atividade.
*   Consulta Inteligente: O agente consulta um DataFrame que contém informações sobre laboratórios, suas capacidades e status de disponibilidade.
*   Retorno do Laboratório Disponível: Após comparar as informações extraídas com o DataFrame, o agente retorna o laboratório disponível que atende aos requisitos fornecidos.

# Tecnologias Utilizadas

* Groq API: Utilizada para executar operações otimizadas e processar grandes quantidades de dados.
* LangChain: Framework para construir cadeias de processamento de linguagem natural, facilitando a extração de informações e a interação com dados.
* Python: Linguagem de programação principal utilizada para integrar Groq e LangChain e executar o código.


#  Estrutura do Projeto
```bash
├── agent.py          # Classe Agente.
├── query_agent.py    # Consulta o banco de dados.
├── main.py           # Codido principal.
├── model.py          # Configuração do modelo.
└── README.md         # Documentação do projeto
```
