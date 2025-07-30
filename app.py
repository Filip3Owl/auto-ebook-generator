import streamlit as st
from langchain.llms import OpenAI
import sys
from pathlib import Path
from PIL import Image
import base64
import json
from datetime import datetime
import traceback
import time
from io import BytesIO
import markdown
import pdfkit
from ebooklib import epub
from bs4 import BeautifulSoup

# Configura paths para imports
sys.path.append(str(Path(__file__).parent))

def load_config():
    """Configuração básica"""
    pass

# Configuração inicial
load_config()

def apply_minimal_theme():
    """
    Aplica tema minimalista com bom contraste
    """
    st.markdown("""
    <style>
        /* Reset básico */
        .stApp {
            background-color: #ffffff;
            color: #333333;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* Header limpo */
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1a1a1a;
            text-align: center;
            margin: 1.5rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #f0f0f0;
        }
        
        /* Sidebar simplificada */
        .css-1d391kg, .css-6qob1r {
            background-color: #f8f8f8;
            border-right: 1px solid #e0e0e0;
        }
        
        /* Cards limpos */
        .custom-card {
            background: #ffffff;
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1rem 0;
            border: 1px solid #e0e0e0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        
        /* Botões simplificados */
        .stButton > button {
            background-color: #1a73e8;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 0.75rem 1.5rem;
            font-weight: 500;
            transition: all 0.2s;
        }
        
        .stButton > button:hover {
            background-color: #1765cc;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }
        
        /* Inputs limpos */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {
            background-color: #ffffff !important;
            border: 1px solid #e0e0e0 !important;
            border-radius: 4px !important;
            padding: 0.75rem !important;
        }
        
        /* Espaçamento melhorado */
        .stTextInput, .stTextArea, .stSelectbox {
            margin-bottom: 1rem;
        }
        
        /* Tabs simplificadas */
        .stTabs [data-baseweb="tab"] {
            padding: 0.75rem 1rem;
            margin: 0 0.25rem;
        }
        
        /* Progress bar */
        .stProgress > div > div > div {
            background-color: #1a73e8 !important;
        }
        
        /* Mensagens mais limpas */
        .stAlert {
            border-radius: 8px;
            padding: 1rem;
        }
        
        /* Links */
        a {
            color: #1a73e8 !important;
            text-decoration: none;
        }
        
        /* Container principal */
        .main-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

def create_header():
    """Cabeçalho minimalista"""
    st.markdown("""
    <div class="main-header">Ebook Generator</div>
    <p style="text-align: center; color: #666; margin-bottom: 2rem;">Transforme ideias em ebooks profissionais</p>
    """, unsafe_allow_html=True)

def create_sidebar():
    """Sidebar simplificada"""
    with st.sidebar:
        st.markdown("## Configurações")
        
        # API Key
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=st.session_state.get("api_key", ""),
            placeholder="sk-..."
        )
        st.session_state.api_key = api_key or None
        
        # Configurações do ebook
        book_type = st.selectbox(
            "Tipo de Livro",
            ["Negócios", "Técnico", "Autoajuda", "Educacional", "Narrativo"],
            index=0
        )
        
        ebook_style = st.selectbox(
            "Estilo de Escrita",
            ["Profissional", "Didático", "Conversacional", "Técnico"],
            index=0
        )
        
        ebook_pages = st.slider(
            "Número de Páginas",
            min_value=10,
            max_value=200,
            value=50,
            step=10
        )
        
        language = st.selectbox(
            "Idioma",
            ["Português", "Inglês", "Espanhol", "Francês"],
            index=0
        )
        
        output_format = st.multiselect(
            "Formatos de Saída",
            ["PDF", "EPUB", "Markdown"],
            default=["PDF"]
        )
        
        st.markdown("---")
        st.markdown("**Estatísticas**")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Ebooks", st.session_state.get("ebooks_generated", 0))
        with col2:
            st.metric("Páginas", st.session_state.get("total_pages", 0))
        
        return {
            "api_key": api_key,
            "book_type": book_type,
            "style": ebook_style,
            "pages": ebook_pages,
            "language": language,
            "formats": output_format
        }

def create_main_form():
    """Formulário principal simplificado"""
    with st.form("ebook_form"):
        ebook_topic = st.text_area(
            "Tópico do Ebook",
            placeholder="Ex: Inteligência Artificial para Iniciantes\nMarketing Digital para Pequenas Empresas",
            height=100
        )
        
        with st.expander("Opções Avançadas"):
            target_audience = st.text_input(
                "Público-alvo",
                value="Adultos interessados no tema"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                difficulty_level = st.selectbox(
                    "Nível",
                    ["Iniciante", "Intermediário", "Avançado"],
                    index=1
                )
            with col2:
                tone = st.selectbox(
                    "Tom",
                    ["Formal", "Conversacional", "Técnico"],
                    index=1
                )
            
            key_points = st.text_area(
                "Pontos-chave",
                placeholder="Liste os principais tópicos a serem abordados",
                height=80
            )
        
        submit_button = st.form_submit_button("Gerar Ebook")
    
    return {
        "topic": ebook_topic,
        "audience": target_audience,
        "difficulty": difficulty_level,
        "tone": tone,
        "key_points": key_points,
        "submit": submit_button
    }

def generate_section_content(llm, prompt, max_retries=3, delay=5):
    """Gera conteúdo com tratamento de erros"""
    for attempt in range(max_retries):
        try:
            return llm(prompt)
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                raise e

def markdown_to_html(markdown_text):
    """Converte markdown para HTML"""
    try:
        html = markdown.markdown(markdown_text)
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Ebook Gerado</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
                h1, h2, h3 {{ color: #1a73e8; }}
                pre {{ background: #f5f5f5; padding: 10px; border-radius: 4px; }}
                code {{ background: #f5f5f5; padding: 2px 4px; }}
            </style>
        </head>
        <body>
            {html}
        </body>
        </html>
        """
    except Exception as e:
        st.error(f"Erro na conversão para HTML: {str(e)}")
        return None

def create_epub(ebook_content, title, author="Ebook Generator"):
    """Cria um arquivo EPUB a partir do conteúdo"""
    book = epub.EpubBook()
    
    # Metadados
    book.set_identifier(str(time.time()))
    book.set_title(title)
    book.set_language('pt')
    book.add_author(author)
    
    # Capítulo principal
    c1 = epub.EpubHtml(title='Conteúdo', file_name='chap_01.xhtml', lang='pt')
    c1.content = markdown_to_html(ebook_content)
    
    # Adiciona ao livro
    book.add_item(c1)
    book.spine = [c1]
    book.toc = [c1]
    
    # CSS básico
    style = '''
    body { font-family: Arial, sans-serif; line-height: 1.6; }
    h1, h2, h3 { color: #1a73e8; }
    '''
    
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)
    
    # Cria o arquivo EPUB
    buffer = BytesIO()
    epub.write_epub(buffer, book, {})
    buffer.seek(0)
    
    return buffer

def create_pdf(ebook_content, title):
    """Cria um PDF a partir do conteúdo HTML"""
    try:
        html_content = markdown_to_html(ebook_content)
        
        options = {
            'page-size': 'A4',
            'margin-top': '15mm',
            'margin-right': '15mm',
            'margin-bottom': '15mm',
            'margin-left': '15mm',
            'encoding': "UTF-8",
            'title': title,
            'quiet': ''
        }
        
        pdf = pdfkit.from_string(html_content, False, options=options)
        return BytesIO(pdf)
    except Exception as e:
        st.error(f"Erro ao gerar PDF: {str(e)}")
        return None

def generate_ebook(llm, topic, config, form_data):
    """Gera o conteúdo do ebook"""
    prompt = f"""
    Crie um ebook completo sobre: {topic}
    
    Diretrizes:
    - Público: {form_data['audience']}
    - Nível: {form_data['difficulty']}
    - Tom: {form_data['tone']}
    - Estilo: {config['style']}
    - Idioma: {config['language']}
    - Tamanho: ~{config['pages'] * 400} palavras
    
    Estrutura:
    1. Título atraente
    2. Introdução (contexto e importância)
    3. 4-6 capítulos com subtópicos
    4. Conclusão com resumo e próximos passos
    5. Recursos adicionais (opcional)
    
    Inclua exemplos práticos quando relevante.
    """
    
    with st.spinner("Gerando conteúdo..."):
        try:
            content = generate_section_content(llm, prompt)
            return f"# {topic}\n\n{content}"
        except Exception as e:
            st.error(f"Erro na geração: {str(e)}")
            return None

def display_results(ebook_content, config, form_data):
    """Exibe os resultados e opções de download"""
    st.session_state.ebooks_generated = st.session_state.get("ebooks_generated", 0) + 1
    st.session_state.total_pages = st.session_state.get("total_pages", 0) + config["pages"]
    
    st.success("Ebook gerado com sucesso!")
    
    # Tabs para visualização e download
    tab1, tab2 = st.tabs(["Visualizar", "Download"])
    
    with tab1:
        st.markdown(ebook_content)
    
    with tab2:
        st.markdown("### Formatos Disponíveis")
        
        # Preparar nome do arquivo
        safe_title = "".join(c for c in form_data['topic'][:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"ebook_{safe_title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}"
        
        # Opções de download
        col1, col2, col3 = st.columns(3)
        
        if "PDF" in config["formats"]:
            with col1:
                pdf_file = create_pdf(ebook_content, form_data['topic'])
                if pdf_file:
                    st.download_button(
                        label="Download PDF",
                        data=pdf_file,
                        file_name=f"{filename}.pdf",
                        mime="application/pdf"
                    )
        
        if "EPUB" in config["formats"]:
            with col2:
                epub_file = create_epub(ebook_content, form_data['topic'])
                st.download_button(
                    label="Download EPUB",
                    data=epub_file,
                    file_name=f"{filename}.epub",
                    mime="application/epub+zip"
                )
        
        if "Markdown" in config["formats"]:
            with col3:
                st.download_button(
                    label="Download Markdown",
                    data=ebook_content.encode('utf-8'),
                    file_name=f"{filename}.md",
                    mime="text/markdown"
                )

def main():
    """Função principal"""
    st.set_page_config(
        page_title="Ebook Generator",
        page_icon="📚",
        layout="centered",
        initial_sidebar_state="expanded"
    )
    
    apply_minimal_theme()
    
    # Inicializar session state
    if "ebooks_generated" not in st.session_state:
        st.session_state.ebooks_generated = 0
    if "total_pages" not in st.session_state:
        st.session_state.total_pages = 0
    
    create_header()
    
    # Layout principal
    config = create_sidebar()
    form_data = create_main_form()
    
    if form_data["submit"] and form_data["topic"]:
        if not config["api_key"]:
            st.error("Por favor, configure sua OpenAI API Key")
            st.stop()
        
        if len(form_data["topic"].strip()) < 10:
            st.warning("Forneça uma descrição mais detalhada do tópico")
            st.stop()
        
        try:
            llm = OpenAI(
                openai_api_key=config["api_key"],
                temperature=0.7,
                max_tokens=3000,
                request_timeout=120
            )
            
            ebook_content = generate_ebook(
                llm=llm,
                topic=form_data["topic"],
                config=config,
                form_data=form_data
            )
            
            if ebook_content:
                display_results(ebook_content, config, form_data)
            
        except Exception as e:
            st.error(f"Erro: {str(e)}")
            with st.expander("Detalhes do erro"):
                st.code(traceback.format_exc())

if __name__ == "__main__":
    main()