from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def create_writing_chain(llm):
    """Cria a cadeia para escrita de conteúdo"""
    prompt = PromptTemplate(
        input_variables=["outline", "topic", "style"],
        template="""
        Com base neste esboço, escreva o conteúdo completo do ebook sobre {topic}:
        {outline}
        
        Estilo: {style}
        Seja detalhado e informativo.
        """
    )
    return LLMChain(llm=llm, prompt=prompt)