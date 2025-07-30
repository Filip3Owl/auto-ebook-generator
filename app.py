import streamlit as st
from langchain.llms import OpenAI
import sys
from pathlib import Path
from PIL import Image
import base64

# Configura paths para imports
sys.path.append(str(Path(__file__).parent))

# Importações locais
from core.prompts import EBOOK_PROMPTS
from agents.outline import create_outline_chain
from agents.writer import create_writing_chain
from utils.file_io import save_ebook
from utils.config import load_config

# Configuração inicial
load_config()

def set_background(image_file):
    """
    Define uma imagem de fundo para o aplicativo
    """
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    style = f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{b64_encoded});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-color: rgba(255, 255, 255, 0.9);
            background-blend-mode: lighten;
        }}
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)

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
    # Configuração da página
    st.set_page_config(
        page_title="📘 Ebook Generator Pro",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Estilo CSS personalizado
    st.markdown("""
    <style>
        .header {
            font-size: 2.5em;
            color: #2c3e50;
            text-align: center;
            margin-bottom: 20px;
        }
        .subheader {
            font-size: 1.2em;
            color: #7f8c8d;
            text-align: center;
            margin-bottom: 30px;
        }
        .sidebar .sidebar-content {
            background-color: #f8f9fa;
        }
        .stTextArea textarea {
            min-height: 150px;
        }
        .success-box {
            padding: 15px;
            background-color: #d4edda;
            border-radius: 5px;
            margin: 20px 0;
        }
        .progress-bar {
            margin: 20px 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Título e introdução
    st.markdown('<div class="header">📘 Ebook Generator Pro</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Transforme suas ideias em ebooks profissionais em minutos</div>', unsafe_allow_html=True)
    
    # Barra lateral com configurações
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2232/2232688.png", width=80)
        st.title("Configurações")
        
        # Seção de API Key
        with st.expander("🔑 Configuração da API", expanded=True):
            api_key = st.text_input(
                "OpenAI API Key",
                type="password",
                value=st.session_state.get("api_key", ""),
                help="Obtenha sua chave em platform.openai.com"
            )
            st.session_state.api_key = api_key or None
            
            if api_key:
                st.success("API Key configurada com sucesso!")
        
        # Seção de opções do ebook
        with st.expander("📖 Opções do Ebook", expanded=True):
            ebook_style = st.selectbox(
                "Estilo de Escrita",
                ["Profissional", "Descontraído", "Técnico", "Persuasivo", "Narrativo"],
                index=0,
                help="Selecione o tom do conteúdo"
            )
            
            ebook_length = st.slider(
                "Tamanho do Ebook",
                3, 30, 10,
                help="Número aproximado de páginas"
            )
            
            output_format = st.radio(
                "Formato de Saída",
                ["PDF", "Markdown", "HTML"],
                index=0,
                horizontal=True
            )
            
            language = st.selectbox(
                "Idioma",
                ["Português", "Inglês", "Espanhol"],
                index=0
            )
    
    # Área principal
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Formulário principal
        with st.form("ebook_form", clear_on_submit=False):
            ebook_topic = st.text_area(
                "**Sobre qual tema será seu ebook?**",
                placeholder="Ex: Inteligência Artificial para Iniciantes\nBlockchain e seu impacto na economia\nComo escrever um livro best-seller",
                height=150,
                help="Descreva o tópico principal com clareza"
            )
            
            # Opções avançadas
            with st.expander("⚙️ Opções Avançadas"):
                target_audience = st.text_input(
                    "Público-alvo",
                    value="Adultos interessados no tema",
                    help="Ex: Adolescentes, Profissionais de TI, Estudantes universitários"
                )
                
                key_points = st.text_area(
                    "Pontos-chave para incluir",
                    placeholder="Liste os principais tópicos que devem ser abordados...",
                    height=100
                )
            
            submit_button = st.form_submit_button(
                "✨ Gerar Ebook",
                use_container_width=True
            )
    
    with col2:
        # Seção de exemplos
        st.info("💡 **Exemplos de temas:**")
        st.write("- Marketing Digital para Pequenas Empresas")
        st.write("- História da Inteligência Artificial")
        st.write("- Guia Prático de Meditação")
        st.write("- Fundamentos de Criptomoedas")
        
        # Seção de dicas
        st.info("🔍 **Dicas para melhores resultados:**")
        st.write("- Seja específico no tópico")
        st.write("- Defina bem o público-alvo")
        st.write("- Use as opções avançadas para direcionar o conteúdo")
    
    # Processamento da geração do ebook
    if submit_button and ebook_topic:
        if not st.session_state.get("api_key"):
            st.warning("⚠️ Por favor, insira sua OpenAI API Key na barra lateral")
            st.stop()
            
        with st.spinner("🔍 Analisando seu tópico e criando estrutura..."):
            try:
                # Barra de progresso
                progress_bar = st.progress(0)
                
                # Configuração do LLM
                llm = OpenAI(
                    openai_api_key=st.session_state.api_key,
                    temperature=0.7,
                    max_tokens=3000
                )
                
                progress_bar.progress(20)
                
                # Geração do ebook
                ebook_chain = create_ebook_chain(llm)
                
                progress_bar.progress(40)
                
                ebook_content = ebook_chain.run(
                    topic=ebook_topic,
                    style=ebook_style,
                    length=ebook_length,
                    audience=target_audience,
                    points=key_points
                )
                
                progress_bar.progress(80)
                
                # Salvamento do ebook
                ebook_path = save_ebook(
                    content=ebook_content,
                    title=ebook_topic,
                    format=output_format.lower()
                )
                
                progress_bar.progress(100)
                
                # Seção de resultados
                st.markdown('<div class="success-box">🎉 Seu ebook foi gerado com sucesso!</div>', unsafe_allow_html=True)
                
                # Visualização e download
                tab1, tab2 = st.tabs(["📄 Visualizar Conteúdo", "⬇️ Download"])
                
                with tab1:
                    st.markdown(ebook_content)
                
                with tab2:
                    with open(ebook_path, "rb") as f:
                        btn_label = f"Baixar Ebook ({output_format})"
                        st.download_button(
                            label=btn_label,
                            data=f,
                            file_name=f"ebook_{ebook_topic[:50]}.{output_format.lower()}",
                            mime=(
                                "application/pdf" if output_format == "PDF" 
                                else "text/markdown" if output_format == "Markdown" 
                                else "text/html"
                            ),
                            use_container_width=True
                        )
                
            except Exception as e:
                st.error(f"❌ Ocorreu um erro ao gerar seu ebook: {str(e)}")
                st.exception(e)

if __name__ == "__main__":
    main()