import streamlit as st
import os

class View:
    """
    Classe responsável pela interface de usuário utilizando Streamlit.

    Permite o upload de arquivos PDF, seleção de arquivos processáveis, entrada de uma categoria opcional
    e exibição dos resultados gerados na forma de evidence briefings.

    Atributos:
        controller: Instância do controlador que gerencia o processamento de arquivos e comunicação
                    com os demais componentes do sistema.
    """

    def __init__(self, controller) -> None:
        """
        Inicializa a classe View com o controlador necessário para processar os arquivos.

        Args:
            controller: Instância de um objeto controlador que realiza o processamento do arquivo
                        selecionado e gerencia as interações entre os módulos do sistema.
        """
        self.controller = controller
        st.set_page_config(layout="wide", page_title="Gerador de Evidence Briefings")

    def run(self):
        """
        Renderiza a interface de usuário utilizando Streamlit.

        Funcionalidades:
            - Exibe uma interface com duas colunas: gerenciamento de arquivos e exibição de resultados.
            - Permite o upload de arquivos PDF, salvando-os localmente.
            - Lista os arquivos PDF disponíveis para seleção.
            - Permite a entrada de uma categoria opcional para o artigo.
            - Processa o arquivo selecionado ao clicar em um botão e exibe o resultado.
            - Exibe uma mensagem de alerta caso nenhum arquivo esteja disponível.

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

        # Cria duas colunas para organização do layout
        _, col1, _, col2, _ = st.columns([0.2, 1.5, 0.5, 2, 0.2])

        # Coluna da esquerda: Gerenciamento de Arquivos
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

            # Upload de arquivos
            uploaded_file = st.file_uploader("Upload do arquivo", type="pdf")
            if uploaded_file is not None:
                with open(f"./files/{uploaded_file.name}", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"Arquivo {uploaded_file.name} salvo com sucesso!")

            # Listar arquivos PDF disponíveis
            path = "./files"
            pdf_files = [f for f in os.listdir(path) if f.endswith(".pdf")]
            st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
            if pdf_files:
                st.subheader("Selecione um arquivo para processar")
                st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                selected_file = st.selectbox("Arquivos disponíveis:", pdf_files)

                # Entrada de categoria opcional
                st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                article_category = st.text_input("Categoria do Artigo (opcional):")

                # Botão para processar o arquivo selecionado
                if st.button("Processar arquivo selecionado"):
                    file_path = os.path.join(path, selected_file)
                    with st.spinner(f"Processando {selected_file}..."):
                        result = self.controller.process(file_path, article_category)
                    st.session_state["last_result"] = result
                    st.success(f"Arquivo {selected_file} processado com sucesso!")
            else:
                st.warning("Nenhum arquivo PDF encontrado na pasta 'files'.")

        # Coluna da direita: Exibição do Briefing Gerado
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

