import os
from data_loader import DataLoader
from model import OpenAiModel
from prompter import Prompter
from retriever import Retriever
from evaluator import Evaluator
from tqdm import tqdm
import pandas as pd
from dotenv import load_dotenv

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

    def process(self, paper_path = '', user_topic = '',paper_content = ''):
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
        if paper_content.strip() == '':
            paper_content = " ".join(self.data_loader.load_single_pdf(paper_path))
        human_message = Prompter.get_researcher_human(paper_content)
        result = self.openai_model.talk_to_model(system_message, human_message)
        return result
    
    def process_eval(self,user_topic = ''):
        """
        Creates a dataset containing evaluation metrics for each article present in the briefings
        """
        eval = Evaluator()
        eval.create_eval_dataset(self.data_loader)
        eval_dataframe = eval.load_eval_dataset()
        required_cols = ['article', 'brief']
        if not all(col in eval_dataframe.columns for col in required_cols):
            raise ValueError(f"Eval dataframe must contain: {required_cols}")

        generated_briefs = []
        
        
        
        
        for index, row in tqdm(eval_dataframe.iterrows(), total=eval_dataframe.shape[0], desc="Processing evaluation"):
            generated_brief = self.process(paper_content=row['article'])
            generated_briefs.append(generated_brief)

        eval_dataframe['generated_brief'] = generated_briefs
        # save inference for future tests
        output_path = os.path.join(os.getcwd(), 'eval_dataset_with_inference')
        eval_dataframe.to_csv(output_path, index=False, encoding='utf-8')
        
        results_df, aggregated_scores = eval.evaluate(eval_dataframe)
        
        return results_df, aggregated_scores


if __name__ == '__main__':
 
    ## human made evidence briefings path ##
    directory_path = "briefings"
    ## embedding model ##
    embedding_model = "all-MiniLM-L6-v2"
    ## openai model name ##
    openai_model_name = "gpt-4o-mini"
    load_dotenv(dotenv_path='env.env')
    openai_api_key = os.getenv("openai_api_key")
    topics = [
        "Intro",
        "Main Findings",
        "Who is this briefing for",
        "Where the findings come from",
        "What is included in this briefing",
        "What is not included in this briefing"
    ]
    topics_chunk_size = [
        300,    
        4000,   
        200,    
        300,    
        300,    
        300     
    ]

    controller = Controller(directory_path, embedding_model, openai_model_name, openai_api_key, topics, topics_chunk_size)
    pd.set_option('display.max_rows', 50)          # Exibir até 50 linhas
    pd.set_option('display.max_columns', 10)       # Exibir até 10 colunas
    pd.set_option('display.width', 120)            # Largura máxima da linha de exibição
    pd.set_option('display.max_colwidth', 80)      # Largura máxima de cada coluna de texto
    results_df, aggregated_scores = controller.process_eval()

    print("\n" + "="*50)
    print("      RESULTADOS DA AVALIAÇÃO CONCLUÍDA")
    print("="*50 + "\n")

    # --- Visualização Simples dos Resultados ---

    # 1. Imprimir as pontuações agregadas de forma organizada
    import pprint
    print("--- PONTUAÇÕES GERAIS (AGREGADAS) ---")
    pprint.pprint(aggregated_scores)
    print("\n" + "-"*50 + "\n")

    # 2. Imprimir o DataFrame com os resultados detalhados
    print("--- RESULTADOS DETALHADOS (POR ARTIGO) ---")
    
    # Imprimimos apenas as colunas mais importantes para a análise
    # O 'brief' é a referência, 'generated_brief' é o do modelo.
    print(results_df[['brief', 'generated_brief', 'rougeL_score']])
    
    # Se quiser forçar a impressão do DataFrame INTEIRO sem cortes (pode ser muito longo)
    # print(results_df.to_string())

    print("\nTeste de avaliação finalizado.")