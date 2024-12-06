from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

class OpenAiModel:
    """
    Classe para interação com o modelo OpenAI, permitindo o envio de mensagens
    e o recebimento de respostas processadas.

    Atributos:
        model (ChatOpenAI): Instância do modelo de chat da OpenAI configurada com o nome do modelo, chave da API e temperatura.
    """

    def __init__(self, model_name, key, temperature=0.5):
        """
        Inicializa a classe OpenAiModel com as configurações necessárias para o modelo OpenAI.

        Args:
            model_name (str): Nome do modelo OpenAI a ser utilizado (e.g., "gpt-4o-mini").
            key (str): Chave da API para autenticação com o OpenAI. Carregada do arquivo .env
            temperature (float, opcional): Grau de aleatoriedade das respostas geradas pelo modelo.
                                           Valores mais baixos tornam as respostas mais determinísticas.
                                           O padrão é 0.5.
        """
        self.model = ChatOpenAI(temperature=temperature, model_name=model_name, openai_api_key=key)

    def talk_to_model(self, system_message, human_message):
        """
        Envia mensagens para o modelo OpenAI e retorna a resposta gerada.

        Args:
            system_message (str): Mensagem do sistema que define o contexto ou as instruções para o modelo.
            human_message (str): Mensagem enviada pelo usuário ou humano que está interagindo com o modelo.

        Returns:
            str: Conteúdo da resposta gerada pelo modelo OpenAI.
        """
        messages = [
            SystemMessage(
                content=system_message
            ),
            HumanMessage(
                content=human_message
            )
        ]
        return self.model(messages).content