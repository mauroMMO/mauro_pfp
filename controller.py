from data_loader import DataLoader
from model import OpenAiModel
from prompter import Prompter
from retriever import Retriever

class Controller:
        """
        Central controller class responsible for managing data loading, embedding generation,
        context retrieval, and interaction with the OpenAI model to produce evidence briefings.

        Attributes:
            data_loader (DataLoader): Handles loading of PDF documents.
            all_briefings (list): Collection of all briefings loaded from the specified directory.
            vector_db (Retriever): Vector database used to retrieve relevant contexts based on embeddings.
            openai_model (OpenAiModel): Interface with the OpenAI model to process prompts and generate responses.
            topics (list): List of topics that guide context retrieval.
            topics_chunk_size (list): Chunk sizes associated with each topic in the vector database.
        """

    def __init__(self, data_path, embedding_model, openai_model_name, openai_api_key, topics, topics_chunk_size):
       """
        Initializes the Controller class with the required data and configuration.

        Args:
            data_path (str): Path to the directory containing the PDF files to be loaded.
            embedding_model (str): Name of the embedding model to be used for vectorization.
            openai_model_name (str): Name of the OpenAI model to be used (e.g., "gpt-3.5-turbo").
            openai_api_key (str): API key used to authenticate with the OpenAI service.
            topics (list): List of topics for context retrieval.
            topics_chunk_size (list): List of chunk sizes corresponding to each topic.
        """
        self.data_loader = DataLoader()
        self.all_briefings = self.data_loader.load_pdfs_from_directory(data_path)
        self.vector_db = Retriever(documents=self.all_briefings, embedding_model=embedding_model)
        self.openai_model = OpenAiModel(model_name=openai_model_name, key=openai_api_key)
        self.topics = topics
        self.topics_chunk_size = topics_chunk_size

    def process(self, paper_path, user_topic):
        """
        Processes a PDF file to generate an evidence briefing.

        Args:
            paper_path (str): Path to the PDF file to be processed.
            user_topic (str): Custom topic provided by the user to refine the query.

        Returns:
            str: The generated evidence briefing as a text output.
        """
        additional_context = self.vector_db.get_context(self.topics, self.topics_chunk_size, user_topic)
        system_message = Prompter.get_researcher_system(additional_context)
        paper_content = " ".join(self.data_loader.load_single_pdf(paper_path))
        human_message = Prompter.get_researcher_human(paper_content)
        result = self.openai_model.talk_to_model(system_message, human_message)
        return result
