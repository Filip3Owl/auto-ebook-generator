from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from core.prompts import EBOOK_PROMPTS

def create_outline_chain(llm):
    """Cria a cadeia para geração de outlines"""
    prompt = PromptTemplate(
        input_variables=["topic", "style", "length"],
        template=EBOOK_PROMPTS["outline"]
    )
    return LLMChain(llm=llm, prompt=prompt, verbose=True)