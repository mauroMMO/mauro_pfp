class Prompter():

    def get_researcher_system(additional_context):
        """
        Gera a mensagem do sistema para o modelo OpenAI, estabelecendo o contexto e as instruções
        para a criação de evidence briefings.

        Args:
            additional_context (str): Contexto adicional a ser incluído na mensagem do sistema,
                                    geralmente relacionado às seções que devem ser abordadas no briefing.

        Returns:
            str: Mensagem formatada que define o comportamento esperado do modelo.
        """
        return ("You are a researcher interested in summarizing scientific papers to write evidence briefings. "
                "Every evidence briefing should include the following sections:\n"
                f"{additional_context}\n"
                "Use these examples and the provided paper to answer future requests.")


    def get_researcher_human(paper):
        """
        Gera a mensagem do usuário para o modelo OpenAI, solicitando a criação de um evidence briefing
        com base no conteúdo do artigo fornecido.

        Args:
            paper (str): Conteúdo completo do artigo científico que será resumido.

        Returns:
            str: Mensagem formatada que solicita ao modelo a criação do evidence briefing.
        """
        return (f"Write an evidence briefing on the following paper:\n{paper}")
