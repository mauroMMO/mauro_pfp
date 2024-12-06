import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document

class DataLoader:
    """
    Classe responsável pelo carregamento de arquivos PDF, seja de um único arquivo ou de um diretório inteiro.

    Atributos:
        Nenhum atributo fixo. Métodos são responsáveis por retornar os dados processados diretamente.
    """

    def load_pdfs_from_directory(self, path):
        """
        Carrega e processa todos os arquivos PDF de um diretório especificado.

        Args:
            path (str): Caminho para o diretório contendo os arquivos PDF.

        Returns:
            list: Lista de objetos `Document`, onde cada objeto representa o conteúdo de uma página de um PDF.

        Obs:
            Apenas arquivos com a extensão `.pdf` são processados. O conteúdo de cada página é armazenado 
            como instância da classe `Document` para ser utilizado posteriormente.
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
        Carrega e processa um único arquivo PDF.

        Args:
            path (str): Caminho para o arquivo PDF.

        Returns:
            list: Lista de strings, onde cada string representa o conteúdo de uma página do PDF.

        Obs:
            O conteúdo das páginas é retornado como uma lista simples de strings, diferente do método 
            `load_pdfs_from_directory`, que encapsula cada página em um objeto `Document`.
        """
        loader = PyPDFLoader(path)
        pages = loader.load_and_split()
        paper_content = [page.page_content for page in pages]
        return paper_content
