from langchain.prompts import PromptTemplate

def create_outline_chain(llm):
    """Cria a cadeia para geração de outlines"""
    prompt = PromptTemplate(
        input_variables=["topic", "style", "length"],
        template="""
        Você é um escritor profissional. Crie um esboço detalhado para um ebook sobre: {topic}
        Estilo: {style}
        Tamanho aproximado: {length} páginas
        
        Retorne em formato Markdown com:
        - Título criativo
        - Capítulos principais
        - Subseções
        - Introdução e conclusão
        """
    )
    return LLMChain(llm=llm, prompt=prompt)