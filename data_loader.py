import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document

class DataLoader:
    """
    Class responsible for loading PDF files, either a single file or an entire directory.

    Attributes:
        No fixed attributes. Methods are responsible for directly returning the processed data.
    """

    def load_pdfs_from_directory(self, path):
        """
        Loads and processes all PDF files from a specified directory.

        Args:
            path (str): Path to the directory containing the PDF files.

        Returns:
            list: List of `Document` objects, where each object represents the content of a PDF page.

        Note:
            Only files with the `.pdf` extension are processed. The content of each page is stored as
            an instance of the `Document` class for later use.
        """
        all_briefings = []  # Lista para armazenar todos os briefings
        for filename in os.listdir(path):
            if filename.endswith(".pdf"):  # Processa apenas arquivos com extensão .pdf
                file_path = os.path.join(path, filename)
                loader = PyPDFLoader(file_path)
                pages = loader.load_and_split()
                paper_content = [page.page_content for page in pages]
                for content in paper_content:
                    all_briefings.append(Document(page_content=content))  # Armazena como objetos `Document`
        return all_briefings

    def load_single_pdf(self, path):
        """
        Loads and processes a single PDF file.

        Args:
            path (str): Path to the PDF file.

        Returns:
            list: List of strings, where each string represents the content of a PDF page.

        Note:
            The page content is returned as a simple list of strings, unlike the `load_pdfs_from_directory` method,
            which wraps each page in a `Document` object.
        """
        loader = PyPDFLoader(path)
        pages = loader.load_and_split()
        paper_content = [page.page_content for page in pages]
        return paper_content
