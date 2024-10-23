import logging
import requests
from langchain_community.utilities import SQLDatabase
from model import Model
from query_agent import Query
from agent import Agent
from rich.console import Console
from rich.table import Table
import ast


url = 'http://127.0.0.1:5000/'
log_url = 'http://127.0.0.1:5000/logs'
sql_url = 'http://127.0.0.1:5000/sql'
mail_url = 'http://127.0.0.1:5000/mail'

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
console = Console()

# Initialize database connection
db = SQLDatabase.from_uri("mysql+mysqlconnector://superuser2:senhasupersegura@localhost/Reservas")

def extract_reservation_info(email_text):
    template = """
    Você é um assistente especializado em alocação de laboratórios, extraia as informações do e-mail {input} e retorne apenas os valores de **Data da atividade (ANO/MÊS/DIA)**, **Turno**, **Software(s) a ser(em) utilizado(s)**, **Quantidade de participantes presenciais**, **Curso** e **Observações**. Sem fornecer explicações adicionais.
    """
    agent = Agent(model, template=template, input=email_text, input2=None)
    response = agent.output()
    content = response.content
    logging.info("Extraído informações da reserva: %s", content)

    # Data
    data = {'Data': content.split("/n")}

    # Send data
    requests.post(log_url, json=data)
    requests.post(mail_url, json=content)

    return response.content

def execute_query(query):
    """Execute the SQL query and return the results."""
    return db.run(query)

def display_results(results):
    """Display results in a formatted table."""
    if not results:
        console.print("[bold red]Nenhum laboratório encontrado.[/bold red]")
        return
    
    table = Table()
    columns = ["Professor", "Atividade", "Curso", "GR", "Alunos Matriculados", 
               "Laboratório", "Data", "Turno", "Status", "Compareceu", 
               "Capacidade", "Prédio", "Início", "Término", "QTD Máquinas", "ID"]
    
    for col in columns:
        table.add_column(col, justify="center")

    for row in results:
        table.add_row(*map(str, row))
    
    console.print(table)

if __name__ == "__main__":
    email_text = """
    
    """
    
    # Initialize the model
    model_instance = Model()
    model = model_instance.get_model()

    # Step 1: Analyze email to determine if it's a reservation or alteration
    template_1 = """
    Você é um assistente especializado em analisar e-mails e dizer se o email {input} se refere a uma Reserva ou Alteração. 
    Responda somente com "Reserva" ou "Alteração".
    """
    agent1 = Agent(model, input=email_text, template=template_1, input2=None)
    reservation_response = agent1.output()
    logging.info("Agente 1 - Resposta: %s", reservation_response)

    # Data
    data = {'Data': str(reservation_response)}
    # Send data
    requests.post('http://127.0.0.1:5000/agent1', json=data)

    # Data
    data = {'Data': str(reservation_response)}
    # Send data
    requests.post(log_url, json=data)


    #console.print(f"[bold yellow]Resposta do Agente 1:[/bold yellow][bold green] {reservation_response.content}[/bold green]\n")

    # If it's a reservation, proceed to extract information
    if "Reserva" in reservation_response.content:
        reservation_info = extract_reservation_info(email_text)

        # Prepare SQL query based on extracted info
        sql_question = f"""
        Use as informações presentes em {reservation_info} e responda: 
        Quais laboratórios estão com o Status diferente de **Ocupado** e com a capacidade maior ou igual a de **Quantidade de participantes presenciais**, e com  a data igual a Data da atividade (ANO/MÊS/DIA) e Turno igual a Turno ? 
        **o formato da data deve ser dd/mm/YY**, sem limite de Linhas. **Não use Software e Curso como filtro!**, Retorne todas as colunas da tabela.
        """
        
        query_instance = Query(sql_question, model)
        response_sql = query_instance.RunQuery()
    
        logging.info(f"Query executada: {response_sql}")

        # Data
        data = {'Data': str(response_sql)}
        # Send data
        requests.post(log_url, json=data)

        # Data
        data = {'Data': response_sql}

        # Send data
        requests.post(sql_url, json=data)

    
        # Execute the SQL query
        results = execute_query(response_sql[9:])
        results = ast.literal_eval(results)  
        display_results(results)

        # If results were found, execute the allocation agent
        if results:
            template_4 = """
            Você é um assistente especializado em alocação de laboratórios. Sua função é analisar a entrada {input} e compará-la com {input2}, retornando o laboratório mais adequado, seguindo as seguintes regras:

            Regras de Alocação:
                1. Preferências por Curso:
                    1.1. Alguns cursos têm preferência por certos laboratórios. Por exemplo:
                        - Cursos de Engenharia Mecânica devem ser priorizados nos laboratórios **E08**.
                    
                2. Compatibilidade de Software:
                    2.1. Alguns laboratórios possuem softwares específicos instalados. Abaixo estão os softwares e seus respectivos laboratórios:
                        - AutoCAD: B09 010, A02 212, E08 101, C08 100o.
                    2.2. **Priorize laboratórios que atendam tanto à preferência de curso (Regra 1.1) quanto à compatibilidade de software (Regra 2.1)**. 

                3. Preferência de Laboratório Específico:
                    3.1. Se {input} contiver um laboratório específico nas observações, ele deve ter prioridade. 

            Saída: Retorne apenas o nome do laboratório selecionado. 
        """
            agent4 = Agent(model, template=template_4, input=reservation_info, input2=results)
            selected_lab_response = agent4.output()
            logging.info("Agente 4 - Laboratório selecionado: %s", selected_lab_response.content)
            console.print(f"[bold green]Laboratório selecionado:[/bold green] [purple]{selected_lab_response.content}[/purple]")


            # Data
            data = {'Data': str(selected_lab_response)}
            # Send data
            requests.post(url, json=data)
            requests.post(log_url, json=data)
      
