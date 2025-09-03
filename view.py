import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import os

class View:
    """
    Class responsible for the user interface using Streamlit.

    Allows uploading of PDF files, selection of processable files, input of an optional category,
    and display of the results generated as evidence briefings.

    Attributes:
        controller: Instance of the controller that manages file processing and communication
                    with the other system components.
    """

    def __init__(self, controller) -> None:
        """
        Initializes the View class with the controller required to process the files.

        Args:
            controller: Instance of a controller object that handles file processing
                    and manages interactions between system modules.
        """

        self.controller = controller
        st.set_page_config(layout="wide", page_title="Gerador de Evidence Briefings")

    def run(self):
        """
        Renders the user interface using Streamlit.

        Features:
            - Displays an interface with two columns: file management and result display.
            - Allows uploading of PDF files and saves them locally.
            - Lists available PDF files for selection.
            - Allows optional category input for the article.
            - Processes the selected file upon button click and displays the result.
            - Shows a warning message if no files are available.

        Returns:
            None
        """
        st.markdown(
            """
            <h1 style='text-align: center;'>
                Gerador de Evidence Briefings
            </h1>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

        # creating two collumns
        _, col1, _, col2, _ = st.columns([0.2, 1.5, 0.5, 2, 0.2])

        # left collumn : file management
        with col1:
            st.markdown(
                """
                <h2 style='text-align: center;'>
                    Gerenciamento de Arquivos
                </h2>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

            # file upload
            uploaded_file = st.file_uploader("Upload do arquivo", type="pdf")
            if uploaded_file is not None:
                with open(f"./files/{uploaded_file.name}", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"Arquivo {uploaded_file.name} salvo com sucesso!")

            # list available files
            path = "./files"
            pdf_files = [f for f in os.listdir(path) if f.endswith(".pdf")]
            st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
            if pdf_files:
                st.subheader("Selecione um arquivo para processar")
                st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                selected_file = st.selectbox("Arquivos disponíveis:", pdf_files)

                # optional category input
                st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                article_category = st.text_input("Categoria do Artigo (opcional):")

                # process file button
                if st.button("Processar arquivo selecionado"):
                    file_path = os.path.join(path, selected_file)
                    with st.spinner(f"Processando {selected_file}..."):
                        result = self.controller.process(file_path, article_category)
                    st.session_state["last_result"] = result
                    st.success(f"Arquivo {selected_file} processado com sucesso!")
            else:
                st.warning("Nenhum arquivo PDF encontrado na pasta 'files'.")

        # right collumn : result display
        with col2:
            st.markdown(
                """
                <h2 style='text-align: center;'>
                    Briefing Gerado
                </h2>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
            if "last_result" in st.session_state and st.session_state["last_result"]:
                st.text_area("Resultado:", value=st.session_state["last_result"], height=500)
            else:
                st.info("Nenhum resultado disponível.")

    def plot_aggregated_scores(aggregated_scores, output_path="aggregated_scores.png"):
        """
        Creates an img of the aggregated scores (eval)
        """
        sns.set_style("whitegrid")
        metrics = {
            'ROUGE-L': aggregated_scores['ROUGE']['rougeL'],
            'BLEU': aggregated_scores['BLEU']['bleu'],
            'METEOR': aggregated_scores['METEOR']['meteor']
        }
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=list(metrics.keys()), y=list(metrics.values()), ax=ax, palette="viridis")
        ax.set_title('Performance Agregada do Modelo', fontsize=16)
        ax.set_ylabel('Pontuação', fontsize=12)
        ax.set_ylim(0, max(list(metrics.values())) * 1.2)
        for index, value in enumerate(metrics.values()):
            ax.text(index, value + 0.01, f"{value:.3f}", ha='center', fontsize=11)
        
        plt.tight_layout()
        fig.savefig(output_path)
        plt.close(fig) # Fecha a figura para liberar memória
        print(f"Gráfico de scores agregados salvo em: {output_path}")