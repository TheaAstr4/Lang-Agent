from langchain_community.utilities import SQLDatabase
from model import Model
from query_agent import Query
from agent import Agent
from rich.console import Console
from rich.syntax import Syntax
from rich.table import Table

console = Console()
db = SQLDatabase.from_uri("mysql+mysqlconnector://superuser2:senhasupersegura@localhost/Reservas")

if __name__ == "__main__":
    texto_exemplo = """ """

    # Inicializa o modelo
    model_instance = Model()
    model = model_instance.get_model()

    # Criando e executando o primeiro agente
    console.print("[bold yellow] 🤖 Executando o Agente 1...[/bold yellow]")
    template_1 = """
            Você é um assistente especializado em analisar e-mails e dizer se o email {input} se refere a uma Reserva ou Alteração. 
            Responda somente com "Reserva" ou "Alteração".
                """
    agente1 = Agent(model, input=texto_exemplo, input2=None, template=template_1)
    #console.print(f"[bold green]🧾 Prompt: \n {template_1}[/bold green]", justify="full")
    resposta = agente1.output()
    console.print(f"[bold yellow]Resposta do Agent 1:[/bold yellow][bold green] {resposta.content}[/bold green]\n")

    if "Reserva" in resposta.content:
        # Criando e executando o segundo agente
        console.print("[bold yellow]🤖 Executando o Agente 2...[/bold yellow]\n")
        
        template_2 = """
                Você é um assistente especializado em alocação de laboratórios,  extraia as informações do e-mail {input} e retorne apenas os valores de Data da atividade (ANO/MÊS/DIA), Turno, Software(s) a ser(em) utilizado(s), Quantidade de participantes presenciais, Curso e Observações. Sem fornecer explicações adicionais.
                    """
        agent2 = Agent(model, template=template_2, input=texto_exemplo, input2=None)
        #console.print(f"[bold green]🧾 rompt: \n {template_2}[/bold green]", justify="full")

        resposta = agent2.output()

        sql_question = f"""Use as informações presentes em {resposta.content} e responda: Quais laboratórios estão com o Status diferente de Ocupado e com a capacidade maior ou igual a de Quantidade de participantes presenciais? 
        **o formato da data deve ser dd/mm/YY**, retorne **apenas** os Laboratórios sem limite de Linhas. **Não use Software e Curso como filtro!**.
       """
        #console.print(f"[bold green]🧾 Prompt: \n {sql_question}[/bold green]", justify="full")
        query_instance = Query(sql_question, model)
        response = query_instance.RunQuery()
        
        syntax = Syntax(response[9:], "sql", theme="monokai", line_numbers=True)
        console.print("[bold yellow]Query executada:[/bold yellow]\n")
        console.print(syntax,  ' ',  '\n')
        query = db.run(response[9:])

        if query == '':
            print("Nenhum laboratório encontrado.")
        else:
            #print(f"Laboratórios encontrados: {query}")

            # Criando e executando o quarto agente
            #console.print("[bold yellow]🤖 Executando o Agente 3...[/bold yellow]")
            template_4 = """
            Você é um assistente especializado em alocação de laboratórios. Sua função é analisar a entrada {input} e compará-la com {input2}, retornando o laboratório mais adequado, seguindo as seguintes regras:

            Regras de Alocação:
                1. Preferências por Curso:
                    1.1. Alguns cursos têm preferência por certos laboratórios. Por exemplo:
                        - Cursos de Engenharia Mecânica devem ser priorizados nos laboratórios **E08**.
                    
                2. Compatibilidade de Software:
                    2.1. Alguns laboratórios possuem softwares específicos instalados. Abaixo estão os softwares e seus respectivos laboratórios:
                        - AutoCAD: B09 010, A02 212, E08 101, C08 100o.
                    2.2. **Priorize laboratórios que atendam tanto à preferência de curso (Regra 1.1) quanto à compatibilidade de software (Regra 2.1)**. Se um laboratório for listado tanto na preferência de curso quanto na lista de compatibilidade de software, ele deve ser escolhido como a **melhor opção**.
                    2.3. Caso um software seja necessário e entre em conflito com a preferência de curso (Regra 1.1), priorize a compatibilidade de software.

                3. Preferência de Laboratório Específico:
                    3.1. Se {input} contiver um laboratório específico nas observações, ele deve ter prioridade. No entanto, esse laboratório só deve ser escolhido se estiver em conformidade com a Regra 2 (compatibilidade de software).
                    3.2. Caso o laboratório especificado não seja compatível com a Regra 2, escolha outro laboratório que atenda ao software necessário.

            Observação: Pequenas variações na escrita dos nomes dos cursos podem ocorrer.

            Saída: Retorne apenas o nome do laboratório selecionado. Priorize o laboratório que atenda tanto à Regra 1.1 quanto à Regra 2.1, caso exista. Caso contrário, siga a compatibilidade de software (Regra 2) para resolver conflitos.
        """
            #console.print(f"[bold green]🧾 Prompt: \n {template_4}[/bold green]")
            agent4 = Agent(model, template=template_4, input=resposta.content, input2=query)
            resposta = agent4.output()
            console.print(f"[bold green]Laboratório selecionado:[/bold green] [purple]{resposta.content}[/purple]")
