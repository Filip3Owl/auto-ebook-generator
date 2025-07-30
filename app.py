import streamlit as st
from langchain.chains import LLMChain
from langchain.llms import OpenAI  # Modificado para usar a importação direta
from core.prompts import EBOOK_PROMPTS
from core.chains import create_ebook_chain
from utils.config import load_config
from utils.file_io import save_ebook

# Configuração inicial
load_config()
st.set_page_config(page_title="📘 Ebook Generator Pro", layout="wide")

def main():
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
    
    # Formulário principal
    with st.form("ebook_form"):
        ebook_topic = st.text_area("Tópico Principal do Ebook", placeholder="Ex: Inteligência Artificial para Iniciantes")
        submit_button = st.form_submit_button("Gerar Ebook")
    
    if submit_button and ebook_topic:
        if not st.session_state.get("api_key"):
            st.warning("Por favor, insira sua OpenAI API Key")
            return
            
        with st.spinner("Criando seu ebook profissional..."):
            try:
                # Configuração do LLM
                llm = OpenAI(
                    openai_api_key=st.session_state.api_key,
                    temperature=0.7,
                    max_tokens=2000
                )
                
                # Criação da cadeia LangChain
                ebook_chain = create_ebook_chain(llm)
                
                # Execução
                ebook_content = ebook_chain.run(
                    topic=ebook_topic,
                    style=ebook_style,
                    length=ebook_length
                )
                
                # Exibição e download
                st.success("Ebook gerado com sucesso!")
                st.markdown(ebook_content)
                
                # Salvar ebook
                ebook_path = save_ebook(ebook_content, ebook_topic)
                with open(ebook_path, "rb") as f:
                    st.download_button(
                        "Baixar Ebook (PDF)",
                        data=f,
                        file_name=f"{ebook_topic[:50]}.pdf"
                    )
                    
            except Exception as e:
                st.error(f"Erro ao gerar ebook: {str(e)}")

if __name__ == "__main__":
    main()