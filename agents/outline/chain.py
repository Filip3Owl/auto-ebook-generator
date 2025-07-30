from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from core.prompts import OUTLINE_PROMPT

def create_outline_chain(llm):
    """Cria a cadeia LangChain para geração de outlines"""
    prompt = PromptTemplate(
        input_variables=["topic", "style", "length"],
        template=OUTLINE_PROMPT
    )
    return LLMChain(llm=llm, prompt=prompt)