from langchain_community.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

class Retriever():

    class Retriever:
        """
        Classe responsável pela criação e manipulação de um banco vetorial para buscar os trechos
        mais relevantes relacionados a uma consulta.

        Atributos:
            vectorstore (Chroma): Armazena os embeddings dos documentos e realiza buscas de similaridade.
        """

    def __init__(self, documents, embedding_model):
        """
        Inicializa a classe Retriever com documentos e um modelo de embeddings.

        Args:
            documents (list): Lista de objetos `Document` representando os textos a serem indexados.
            embedding_model (str): Nome do modelo de embeddings utilizado para criar representações vetoriais.
        """
        self.vectorstore = Chroma.from_documents(
            documents=documents,  
            embedding=SentenceTransformerEmbeddings(model_name=embedding_model),
            persist_directory="./chroma_db"
        )

    def _get_top_chunks(self, query, num_chunks=5, chunk_size=1000):
        """
        Busca os `num_chunks` mais relevantes para a consulta fornecida e divide os resultados
        em chunks do tamanho especificado.

        Args:
            query (str): Consulta textual para buscar os trechos relevantes.
            num_chunks (int, opcional): Número de trechos mais relevantes a serem retornados. Padrão é 5.
            chunk_size (int, opcional): Tamanho máximo de cada chunk em caracteres. Padrão é 1000.

        Returns:
            list: Lista de strings contendo os chunks mais relevantes.

        """
        results = self.vectorstore.similarity_search(query, k=num_chunks)
        chunks = []
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=0)

        for res in results:
            page_chunks = splitter.split_text(res.page_content)
            for i, chunk in enumerate(page_chunks):
                print(f"Chunk {i+1} encontrado para a consulta '{query}':\n{chunk}\n")  # Exibe os chunks no console
            chunks.extend(page_chunks)
        
        return chunks

    def get_context(self, topics, topics_chunk_size, user_topic):
        """
        Gera um contexto organizado por tópicos baseado nos trechos mais relevantes encontrados no banco vetorial.

        Args:
            topics (list): Lista de tópicos para construir a consulta.
            topics_chunk_size (list): Lista de tamanhos de chunk para cada tópico.
            user_topic (str): Tópico personalizado fornecido pelo usuário para refinar as consultas.

        Returns:
            str: Contexto formatado por tópico contendo os chunks mais relevantes.

        """
        context_by_topic = {}

        for topic, chunk_size in zip(topics, topics_chunk_size):
            query_with_topic = f"{topic} - {user_topic}"
            context_by_topic[topic] = self._get_top_chunks(query_with_topic, num_chunks=5, chunk_size=chunk_size)

        return "\n".join([f"{topic}:\n" + "\n".join(context_by_topic[topic]) for topic in topics])

        


        
    