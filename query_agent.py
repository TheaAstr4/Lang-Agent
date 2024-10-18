from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase

class Query:
    def __init__(self, sql_question, llm):
        # Conecta ao banco de dados
        self.db = SQLDatabase.from_uri("mysql+mysqlconnector://superuser2:senhasupersegura@localhost/Reservas")
        self.sql_question = sql_question
        self.llm = llm

    def RunQuery(self):
        # Cria uma cadeia de consulta SQL
        chain = create_sql_query_chain(self.llm, self.db)
        
        # Executa a consulta SQL usando a questão fornecida
        sql_response = chain.invoke({"question": self.sql_question})

        return sql_response
