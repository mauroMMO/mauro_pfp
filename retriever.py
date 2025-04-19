from langchain_community.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

class Retriever():

    class Retriever:
        """
        Class responsible for creating and managing a vector store to retrieve the most relevant
        passages related to a query.

        Attributes:
            vectorstore (Chroma): Stores document embeddings and performs similarity searches.
        """

    def __init__(self, documents, embedding_model):
        """
        Initializes the Retriever class with documents and an embedding model.

        Args:
            documents (list): List of `Document` objects representing the texts to be indexed.
            embedding_model (str): Name of the embedding model used to create vector representations.
        """
        self.vectorstore = Chroma.from_documents(
            documents=documents,  
            embedding=SentenceTransformerEmbeddings(model_name=embedding_model),
            persist_directory="./chroma_db"
        )

    def _get_top_chunks(self, query, num_chunks=5, chunk_size=1000):
        """
        Retrieves the `num_chunks` most relevant passages for the given query and splits the results
        into chunks of the specified size.

        Args:
            query (str): Textual query to search for relevant passages.
            num_chunks (int, optional): Number of top relevant passages to return. Default is 5.
            chunk_size (int, optional): Maximum size of each chunk in characters. Default is 1000.

        Returns:
            list: List of strings containing the most relevant chunks.
        """
        results = self.vectorstore.similarity_search(query, k=num_chunks)
        chunks = []
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=0)

        for res in results:
            page_chunks = splitter.split_text(res.page_content)
            chunks.extend(page_chunks)
        
        return chunks

    def get_context(self, topics, topics_chunk_size, user_topic):
        """
        Generates a topic-organized context based on the most relevant passages retrieved from the vector store.

        Args:
            topics (list): List of topics to build the query.
            topics_chunk_size (list): List of chunk sizes for each topic.
            user_topic (str): Custom topic provided by the user to refine the queries.

        Returns:
            str: Topic-formatted context containing the most relevant chunks.
        """
        context_by_topic = {}

        for topic, chunk_size in zip(topics, topics_chunk_size):
            query_with_topic = f"{topic} - {user_topic}"
            context_by_topic[topic] = self._get_top_chunks(query_with_topic, num_chunks=5, chunk_size=chunk_size)

        return "\n".join([f"{topic}:\n" + "\n".join(context_by_topic[topic]) for topic in topics])

        


        
    