from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from modules.outline.chain import create_outline_chain
from modules.writer.chain import create_writing_chain

def create_ebook_chain(llm):
    """Orquestra toda a cadeia de geração de ebooks"""
    outline_chain = create_outline_chain(llm)
    writing_chain = create_writing_chain(llm)
    
    # Esta é uma simplificação - na prática você teria uma cadeia sequencial mais complexa
    def combined_chain(topic, style, length):
        outline = outline_chain.run(topic=topic, style=style, length=length)
        ebook = writing_chain.run(outline=outline, style=style)
        return ebook
    
    return combined_chain