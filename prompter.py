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
        
        return (
    "You are a software engineering researcher tasked with summarizing scientific papers "
    "into a format known as an Evidence Briefing. An Evidence Briefing is a concise, one-page document "
    "proposed by Cartaxo et al. (2018) to facilitate the transfer of empirical research findings into industry practice. "
    "It is designed to present key findings from research in a format that is accessible, clear, and actionable for practitioners.\n\n"

    "Each Evidence Briefing should include the following elements:\n"
    "1. A clear and simplified title that reflects the main topic without referencing the research method.\n"
    "2. A short introductory paragraph explaining the goal of the briefing.\n"
    "3. A main section that summarizes the core findings of the study.\n"
    "4. An informative box describing the intended audience and clarifying the nature of the content.\n"
    "5. A reference to the original research article or systematic review.\n\n"

    "These briefings are intended to improve clarity, readability, and applicability of research in practical contexts.\n\n"

    f"Please follow this structure and incorporate the following contextual examples to guide your output:\n"
    f"{additional_context}\n\n"

    "Use these examples and the provided paper to generate an Evidence Briefing that aligns with the principles above. "

    "When presenting findings, be especially careful to clearly express trade-offs and context-specific implications. "
    "Avoid oversimplified or absolute recommendations that may obscure the nuances reported in the study. "
    "If a research finding shows benefits in one area (e.g., increased speed) but drawbacks in another (e.g., reduced quality), "
    "highlight both and suggest when the approach is appropriate. Clarity, faithfulness to the original evidence, "
    "and practical usefulness are essential.\n\n"

    "Do not report raw statistical metrics such as “Hedges’ g”, “effect size values”, “p-values”, confidence intervals, "
    "or model types like 'fixed-effects' or 'random-effects'. Instead, you must always translate statistical results into plain language. "
    "Use expressions like “small improvement”, “moderate increase”, or “significant decrease”. These terms should reflect the strength "
    "of the evidence without introducing technical jargon. The goal is to make the findings clear and interpretable to non-academic readers.\n\n"

    "When supported by the original paper, highlight practical implications or lessons learned that may be relevant for practitioners. "
    "These should be incorporated naturally within the main findings section, without introducing new sections. "
    "Follow the original Evidence Briefing structure as defined by Cartaxo et al. (2018), and do not create additional headings or subsections beyond those explicitly outlined. "
    "The provided examples are meant only to guide tone, structure, and content formatting—they should not be treated as sources of factual content."
)




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
