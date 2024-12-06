from data_loader import DataLoader
from model import OpenAiModel
from prompter import Prompter
from retriever import Retriever

class Controller:
    """
    Classe central do controlador para gerenciar o carregamento de dados, geração de embeddings,
    recuperação de contexto e interação com o modelo OpenAI para gerar evidence briefings.

    Atributos:
        data_loader (DataLoader): Responsável pelo carregamento de documentos PDF.
        all_briefings (list): Coleção de todos os briefings carregados do diretório especificado.
        vector_db (Retriever): Banco vetorial para recuperar contextos relevantes a partir de embeddings.
        openai_model (OpenAiModel): Interface com o modelo OpenAI para processar prompts e respostas.
        topics (list): Lista de tópicos que orientam a recuperação de contexto.
        topics_chunk_size (list): Tamanhos de chunks correspondentes a cada tópico no banco vetorial.
    """

    def __init__(self, data_path, embedding_model, openai_model_name, openai_api_key, topics, topics_chunk_size):
        """
        Inicializa a classe Controller com os dados e configurações necessárias.

        Args:
            data_path (str): Caminho para o diretório contendo os arquivos PDF a serem carregados.
            embedding_model (str): Nome do modelo de embeddings a ser usado para vetorização.
            openai_model_name (str): Nome do modelo OpenAI a ser utilizado (e.g., "gpt-3.5-turbo").
            openai_api_key (str): Chave da API para autenticar o uso do modelo OpenAI.
            topics (list): Lista de tópicos para recuperação de contexto.
            topics_chunk_size (list): Lista de tamanhos de chunks correspondentes a cada tópico.
        """
        self.data_loader = DataLoader()
        self.all_briefings = self.data_loader.load_pdfs_from_directory(data_path)
        self.vector_db = Retriever(documents=self.all_briefings, embedding_model=embedding_model)
        self.openai_model = OpenAiModel(model_name=openai_model_name, key=openai_api_key)
        self.topics = topics
        self.topics_chunk_size = topics_chunk_size

    def process(self, paper_path, user_topic):
        """
        Processa um arquivo PDF para gerar um evidence briefing.

        Args:
            paper_path (str): Caminho para o arquivo PDF a ser processado.
            user_topic (str): Tópico personalizado fornecido pelo usuário para refinar a consulta.

        Returns:
            str: O evidence briefing gerado como uma saída textual.
        """
        additional_context = self.vector_db.get_context(self.topics, self.topics_chunk_size, user_topic)
        system_message = Prompter.get_researcher_system(additional_context)
        paper_content = " ".join(self.data_loader.load_single_pdf(paper_path))
        human_message = Prompter.get_researcher_human(paper_content)
        result = self.openai_model.talk_to_model(system_message, human_message)
        return result
