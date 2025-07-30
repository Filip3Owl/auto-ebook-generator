import streamlit as st
from langchain.llms import OpenAI
import sys
from pathlib import Path

# Configura paths para imports
sys.path.append(str(Path(__file__).parent))

# Importações locais
from core.prompts import EBOOK_PROMPTS
from agents.outline import create_outline_chain
from agents.writer import create_writing_chain
from utils.file_io import save_ebook
from utils.config import load_config

def create_ebook_chain(llm):
    """Cria a cadeia completa de geração de ebooks"""
    outline_chain = create_outline_chain(llm)
    writing_chain = create_writing_chain(llm)
    
    def combined_chain(topic, style, length):
        outline = outline_chain.run(topic=topic, style=style, length=length)
        ebook = writing_chain.run(outline=outline, topic=topic, style=style)
        return ebook
    
    return combined_chain

def main():
    load_config()
    st.set_page_config(page_title="📘 Ebook Generator Pro", layout="wide")
    
    st.title("📘 Ebook Generator Pro")
    st.caption("Crie ebooks profissionais em minutos com IA")
    
    with st.sidebar:
        st.header("Configurações")
        api_key = st.text_input("OpenAI API Key", type="password", value=st.session_state.get("api_key", ""))
        st.session_state.api_key = api_key or None
        
        if api_key:
            st.success("API Key configurada!")
        
        st.divider()
        st.subheader("Opções do Ebook")
        ebook_style = st.selectbox("Estilo", ["Profissional", "Descontraído", "Técnico"])
        ebook_length = st.slider("Tamanho (páginas)", 3, 20, 5)
        output_format = st.selectbox("Formato de Saída", ["PDF", "Markdown"])
    
    with st.form("ebook_form"):
        ebook_topic = st.text_area("Tópico Principal do Ebook", 
                                 placeholder="Ex: Inteligência Artificial para Iniciantes",
                                 height=100)
        submit_button = st.form_submit_button("Gerar Ebook")
    
    if submit_button and ebook_topic:
        if not st.session_state.get("api_key"):
            st.warning("Por favor, insira sua OpenAI API Key")
            return
            
        with st.spinner("Criando seu ebook profissional..."):
            try:
                llm = OpenAI(
                    openai_api_key=st.session_state.api_key,
                    temperature=0.7,
                    max_tokens=2000
                )
                
                ebook_content = create_ebook_chain(llm)(
                    topic=ebook_topic,
                    style=ebook_style,
                    length=ebook_length
                )
                
                st.success("Ebook gerado com sucesso!")
                with st.expander("Visualizar Conteúdo"):
                    st.markdown(ebook_content)
                
                ebook_path = save_ebook(
                    content=ebook_content,
                    title=ebook_topic,
                    format=output_format.lower()
                )
                
                with open(ebook_path, "rb") as f:
                    btn_label = "Baixar Ebook (PDF)" if output_format == "PDF" else "Baixar Markdown"
                    st.download_button(
                        label=btn_label,
                        data=f,
                        file_name=f"ebook_{ebook_topic[:50]}.{output_format.lower()}",
                        mime="application/pdf" if output_format == "PDF" else "text/markdown"
                    )
                    
            except Exception as e:
                st.error(f"Erro ao gerar ebook: {str(e)}")

if __name__ == "__main__":
    main()