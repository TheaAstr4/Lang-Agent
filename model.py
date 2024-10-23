from langchain_groq import ChatGroq

class Model:
    def __init__(self):
        # Inicializa o modelo ChatGroq
        self.model = ChatGroq(
            model="llama3-groq-70b-8192-tool-use-preview",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key="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"
        )

    # Método para acessar o modelo
    def get_model(self):
        return self.model
