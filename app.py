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

# Configura paths para imports
sys.path.append(str(Path(__file__).parent))

# Importações locais (comentadas pois não temos os arquivos)
# from core.prompts import EBOOK_PROMPTS
# from agents.outline import create_outline_chain
# from agents.writer import create_writing_chain
# from utils.file_io import save_ebook
# from utils.config import load_config

def load_config():
    """Configuração básica (substitui o import)"""
    pass

# Configuração inicial
load_config()

def apply_modern_theme():
    """
    Aplica tema moderno com melhor contraste e visibilidade
    """
    st.markdown("""
    <style>
        /* Reset e configurações globais */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #f8fafc;
        }
        
        /* Header personalizado */
        .main-header {
            font-size: 3.5em;
            font-weight: 800;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #06b6d4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center;
            margin: 30px 0;
            text-shadow: 0 0 40px rgba(59, 130, 246, 0.6);
            animation: glow 2s ease-in-out infinite alternate;
        }
        
        @keyframes glow {
            from { filter: drop-shadow(0 0 20px rgba(59, 130, 246, 0.4)); }
            to { filter: drop-shadow(0 0 30px rgba(139, 92, 246, 0.6)); }
        }
        
        .sub-header {
            font-size: 1.4em;
            color: #cbd5e1;
            text-align: center;
            margin-bottom: 40px;
            font-weight: 300;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        /* Sidebar styling */
        .css-1d391kg, .css-6qob1r {
            background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
            border-right: 2px solid #475569;
        }
        
        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
            color: #f8fafc;
        }
        
        /* Cards e containers com melhor contraste */
        .custom-card {
            background: linear-gradient(145deg, #334155, #475569);
            border-radius: 20px;
            padding: 30px;
            margin: 25px 0;
            border: 2px solid #64748b;
            box-shadow: 
                0 20px 40px rgba(0, 0, 0, 0.4),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            color: #f8fafc;
        }
        
        .feature-card {
            background: linear-gradient(135deg, #1e40af20, #7c3aed20);
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
            border: 2px solid #3b82f6;
            transition: all 0.3s ease;
            color: #f8fafc;
            backdrop-filter: blur(10px);
        }
        
        .feature-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 25px 50px rgba(59, 130, 246, 0.3);
            border-color: #60a5fa;
            background: linear-gradient(135deg, #1e40af30, #7c3aed30);
        }
        
        .feature-card h4 {
            color: #60a5fa;
            margin-bottom: 15px;
            font-weight: 700;
        }
        
        .feature-card p, .feature-card ul, .feature-card li {
            color: #e2e8f0 !important;
            line-height: 1.6;
        }
        
        /* Botões personalizados */
        .stButton > button {
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            color: white !important;
            border: none;
            border-radius: 30px;
            padding: 15px 35px;
            font-weight: 700;
            font-size: 16px;
            transition: all 0.3s ease;
            box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 30px rgba(59, 130, 246, 0.5);
            background: linear-gradient(135deg, #2563eb, #7c3aed);
        }
        
        /* Form inputs com melhor visibilidade */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {
            background-color: #475569 !important;
            color: #f8fafc !important;
            border: 2px solid #64748b !important;
            border-radius: 12px !important;
            padding: 15px !important;
            transition: all 0.3s ease;
            font-size: 16px !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stSelectbox > div > div > select:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
            background-color: #334155 !important;
        }
        
        .stTextInput label, .stTextArea label, .stSelectbox label {
            color: #e2e8f0 !important;
            font-weight: 600 !important;
            margin-bottom: 8px !important;
        }
        
        /* Placeholders */
        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder {
            color: #94a3b8 !important;
            opacity: 1;
        }
        
        /* Progress bar */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #3b82f6, #8b5cf6) !important;
        }
        
        /* Messages com melhor contraste */
        .stSuccess {
            background: linear-gradient(135deg, #059669, #10b981) !important;
            border: none !important;
            border-radius: 12px !important;
            color: white !important;
            padding: 15px !important;
        }
        
        .stError {
            background: linear-gradient(135deg, #dc2626, #ef4444) !important;
            border: none !important;
            border-radius: 12px !important;
            color: white !important;
            padding: 15px !important;
        }
        
        .stWarning {
            background: linear-gradient(135deg, #d97706, #f59e0b) !important;
            border: none !important;
            border-radius: 12px !important;
            color: white !important;
            padding: 15px !important;
        }
        
        .stInfo {
            background: linear-gradient(135deg, #2563eb, #3b82f6) !important;
            border: none !important;
            border-radius: 12px !important;
            color: white !important;
            padding: 15px !important;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            background-color: #475569 !important;
            border-radius: 12px !important;
            color: #f8fafc !important;
            font-weight: 700 !important;
            padding: 15px !important;
        }
        
        .streamlit-expanderContent {
            background-color: #334155 !important;
            border-radius: 0 0 12px 12px !important;
            color: #f8fafc !important;
        }
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: #475569 !important;
            border-radius: 12px 12px 0 0 !important;
            color: #cbd5e1 !important;
            font-weight: 600 !important;
            padding: 15px 25px !important;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
            color: white !important;
        }
        
        /* Slider customization */
        .stSlider > div > div > div > div {
            background: linear-gradient(90deg, #3b82f6, #8b5cf6) !important;
        }
        
        /* Radio buttons */
        .stRadio > div {
            background-color: #475569 !important;
            border-radius: 12px !important;
            padding: 20px !important;
            color: #f8fafc !important;
        }
        
        .stRadio label {
            color: #f8fafc !important;
        }
        
        /* Checkbox */
        .stCheckbox > label {
            color: #f8fafc !important;
        }
        
        /* Metrics styling */
        .metric-card {
            background: linear-gradient(145deg, #334155, #475569);
            border-radius: 20px;
            padding: 25px;
            text-align: center;
            border: 2px solid #64748b;
            margin: 15px 0;
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(59, 130, 246, 0.2);
        }
        
        .metric-value {
            font-size: 2.8em;
            font-weight: bold;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .metric-label {
            color: #cbd5e1;
            font-size: 1em;
            margin-top: 8px;
            font-weight: 600;
        }
        
        /* Animation classes */
        .fade-in {
            animation: fadeInUp 1s ease-out;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(40px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Glassmorphism effect com melhor contraste */
        .glass-card {
            background: rgba(71, 85, 105, 0.7);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            border: 2px solid rgba(148, 163, 184, 0.3);
            padding: 30px;
            margin: 25px 0;
            color: #f8fafc;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }
        
        .glass-card h3, .glass-card h4 {
            color: #60a5fa !important;
        }
        
        /* Loading spinner */
        .custom-spinner {
            border: 4px solid rgba(59, 130, 246, 0.3);
            border-top: 4px solid #3b82f6;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 30px auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Scrollbar customization */
        ::-webkit-scrollbar {
            width: 12px;
        }
        
        ::-webkit-scrollbar-track {
            background: #1e293b;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            border-radius: 6px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #2563eb, #7c3aed);
        }
        
        /* Texto geral com melhor contraste */
        p, span, div, li {
            color: #e2e8f0;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #f8fafc !important;
        }
        
        /* Links */
        a {
            color: #60a5fa !important;
            text-decoration: none;
        }
        
        a:hover {
            color: #93c5fd !important;
        }
        
        /* Footer styling */
        .footer-style {
            background: linear-gradient(135deg, #1e293b, #334155);
            padding: 30px;
            border-radius: 20px;
            border: 1px solid #475569;
            text-align: center;
            margin-top: 40px;
        }
    </style>
    """, unsafe_allow_html=True)

def create_header():
    """Cria o cabeçalho principal"""
    st.markdown("""
    <div class="fade-in">
        <div class="main-header">📚 EBook Generator Pro</div>
        <div class="sub-header">Transforme suas ideias em ebooks profissionais com inteligência artificial</div>
    </div>
    """, unsafe_allow_html=True)

def create_sidebar():
    """Cria a sidebar com configurações"""
    with st.sidebar:
        # Logo e título da sidebar
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <div style="font-size: 4em;">⚙️</div>
            <h2 style="color: #60a5fa; margin: 10px 0;">Configurações</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Configuração da API Key
        with st.expander("🔑 Configuração da API", expanded=True):
            api_key = st.text_input(
                "OpenAI API Key",
                type="password",
                value=st.session_state.get("api_key", ""),
                help="Obtenha sua chave em platform.openai.com",
                placeholder="sk-..."
            )
            st.session_state.api_key = api_key or None
            
            if api_key:
                st.success("✅ API Key configurada!")
            else:
                st.warning("⚠️ API Key necessária")
        
        # Configurações do ebook
        with st.expander("📖 Configurações do Ebook", expanded=True):
            # Tipo de livro
            book_type = st.selectbox(
                "Tipo de Livro",
                ["📈 Negócios", "🛠️ Técnico", "💡 Autoajuda", "🎓 Educacional", "📝 Narrativo"],
                index=0,
                help="Selecione o tipo de ebook para otimização"
            )
            
            # Estilo de escrita
            style_options = {
                "📈 Negócios": ["Executivo", "Estratégico", "Prático", "Analítico"],
                "🛠️ Técnico": ["Didático", "Profissional", "Detalhado", "Científico"],
                "💡 Autoajuda": ["Inspiracional", "Motivacional", "Empático", "Transformador"],
                "🎓 Educacional": ["Didático", "Claro", "Estruturado", "Progressivo"],
                "📝 Narrativo": ["Envolvente", "Descritivo", "Criativo", "Emocional"]
            }
            
            ebook_style = st.selectbox(
                "Estilo de Escrita",
                style_options[book_type],
                help="Tom e abordagem do conteúdo"
            )
            
            # Tamanho do ebook (até 200 páginas)
            ebook_pages = st.slider(
                "📄 Número de Páginas",
                min_value=10,
                max_value=200,
                value=50,
                step=10,
                help="Tamanho aproximado do ebook"
            )
            
            # Estimativa de palavras
            estimated_words = ebook_pages * 400  # ~400 palavras por página para ebooks
            st.info(f"📊 Estimativa: ~{estimated_words:,} palavras")
            
            # Idioma
            language = st.selectbox(
                "🌍 Idioma",
                ["🇧🇷 Português", "🇺🇸 Inglês", "🇪🇸 Espanhol", "🇫🇷 Francês"],
                index=0
            )
        
        # Opções de formato
        with st.expander("💾 Formato de Saída"):
            output_format = st.radio(
                "Escolha o formato:",
                ["📝 Markdown", "🌐 HTML", "📄 Texto"],
                index=0,
                horizontal=False
            )
            
            include_images = st.checkbox(
                "🖼️ Incluir sugestões de imagens",
                value=True,
                help="Adiciona descrições de imagens relevantes"
            )
            
            include_exercises = st.checkbox(
                "✏️ Incluir exercícios práticos",
                value=True,
                help="Adiciona atividades e reflexões"
            )
        
        # Estatísticas da sessão
        st.markdown("---")
        st.markdown("### 📊 Estatísticas")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Ebooks Gerados",
                st.session_state.get("ebooks_generated", 0),
                delta=None
            )
        with col2:
            st.metric(
                "Páginas Totais",
                st.session_state.get("total_pages", 0),
                delta=None
            )
        
        return {
            "api_key": api_key,
            "book_type": book_type,
            "style": ebook_style,
            "pages": ebook_pages,
            "language": language,
            "format": output_format,
            "include_images": include_images,
            "include_exercises": include_exercises
        }

def create_main_form():
    """Cria o formulário principal"""
    st.markdown('<div class="custom-card fade-in">', unsafe_allow_html=True)
    
    with st.form("ebook_form", clear_on_submit=False):
        # Título do tópico
        st.markdown("### 💭 Sobre o que será seu ebook?")
        ebook_topic = st.text_area(
            "",
            placeholder="📝 Exemplo:\n• Inteligência Artificial para Iniciantes\n• Marketing Digital para Pequenas Empresas\n• Guia Completo de Investimentos\n• História do Brasil Contemporâneo",
            height=120,
            help="Seja específico sobre o tema principal"
        )
        
        # Opções avançadas
        with st.expander("🎯 Opções Avançadas", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                target_audience = st.text_input(
                    "👥 Público-alvo",
                    value="Adultos interessados no tema",
                    help="Ex: Profissionais de TI, Estudantes, Empreendedores"
                )
                
                difficulty_level = st.selectbox(
                    "📊 Nível de Dificuldade",
                    ["Iniciante", "Intermediário", "Avançado", "Especialista"],
                    index=1
                )
            
            with col2:
                tone = st.selectbox(
                    "🎭 Tom do Conteúdo",
                    ["Formal", "Conversacional", "Técnico", "Inspiracional"],
                    index=1
                )
                
                focus_area = st.selectbox(
                    "🎯 Foco Principal",
                    ["Teórico", "Prático", "Balanceado", "Case Studies"],
                    index=2
                )
            
            key_points = st.text_area(
                "📋 Pontos-chave para incluir",
                placeholder="• Conceitos fundamentais\n• Exemplos práticos\n• Dicas de implementação\n• Erros comuns a evitar",
                height=100,
                help="Liste os principais tópicos que devem ser abordados"
            )
            
            special_requirements = st.text_area(
                "⭐ Requisitos Especiais",
                placeholder="• Incluir estatísticas atuais\n• Focar em mercado brasileiro\n• Adicionar templates\n• Casos de sucesso reais",
                height=80,
                help="Requisitos específicos ou preferências especiais"
            )
        
        # Botão de geração
        st.markdown("<br>", unsafe_allow_html=True)
        submit_button = st.form_submit_button(
            "✨ Gerar Ebook Profissional",
            use_container_width=True
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return {
        "topic": ebook_topic,
        "audience": target_audience,
        "difficulty": difficulty_level,
        "tone": tone,
        "focus": focus_area,
        "key_points": key_points,
        "special_requirements": special_requirements,
        "submit": submit_button
    }

def generate_section_content(llm, prompt, max_retries=3, delay=5):
    """Gera conteúdo para uma seção com tratamento de erros e retries"""
    for attempt in range(max_retries):
        try:
            return llm(prompt)
        except Exception as e:
            if attempt < max_retries - 1:
                st.warning(f"⚠️ Tentativa {attempt + 1} falhou. Tentando novamente em {delay} segundos...")
                time.sleep(delay)
            else:
                raise e

def markdown_to_html(markdown_text):
    """Converte markdown para HTML"""
    try:
        html = markdown.markdown(
            markdown_text,
            extensions=['extra', 'codehilite', 'toc']
        )
        
        # Template HTML completo
        html_template = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Ebook Gerado</title>
            <style>
                body {{
                    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
                    line-height: 1.7;
                    max-width: 900px;
                    margin: 0 auto;
                    padding: 40px 20px;
                    background: #f8fafc;
                    color: #1e293b;
                }}
                
                h1 {{
                    color: #1e40af;
                    border-bottom: 4px solid #3b82f6;
                    padding-bottom: 15px;
                    margin-top: 40px;
                    font-size: 2.5em;
                }}
                
                h2 {{
                    color: #1e40af;
                    border-bottom: 2px solid #60a5fa;
                    padding-bottom: 10px;
                    margin-top: 35px;
                    font-size: 2em;
                }}
                
                h3 {{
                    color: #1e40af;
                    margin-top: 30px;
                    font-size: 1.5em;
                }}
                
                .highlight {{
                    background: linear-gradient(135deg, #dbeafe, #e0f2fe);
                    padding: 20px;
                    border-left: 5px solid #3b82f6;
                    margin: 25px 0;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
                }}
                
                code {{
                    background: #f1f5f9;
                    padding: 3px 6px;
                    border-radius: 4px;
                    font-family: 'Monaco', 'Consolas', monospace;
                    color: #7c3aed;
                }}
                
                pre {{
                    background: #0f172a;
                    color: #e2e8f0;
                    padding: 20px;
                    border-radius: 8px;
                    overflow-x: auto;
                }}
                
                blockquote {{
                    background: #f8fafc;
                    border-left: 4px solid #64748b;
                    margin: 20px 0;
                    padding: 15px 25px;
                    font-style: italic;
                    color: #475569;
                }}
                
                ul, ol {{
                    padding-left: 25px;
                }}
                
                li {{
                    margin-bottom: 8px;
                }}
                
                .page-break {{
                    page-break-before: always;
                }}
                
                @media print {{
                    body {{ margin: 0; padding: 20px; }}
                    .page-break {{ page-break-before: always; }}
                }}
            </style>
        </head>
        <body>
            {html}
        </body>
        </html>
        """
        
        return html_template
    except Exception as e:
        st.error(f"Erro na conversão para HTML: {str(e)}")
        return None

def generate_comprehensive_ebook(llm, topic, config, form_data):
    """Gera um ebook completo usando múltiplas chamadas para conteúdo extenso"""
    
    # 1. Gerar estrutura detalhada do ebook
    outline_prompt = f"""
    Crie uma estrutura DETALHADA para um ebook de {config['pages']} páginas sobre:
    TEMA: {topic}
    
    ESPECIFICAÇÕES:
    - Tipo: {config['book_type']}
    - Estilo: {config['style']}
    - Público: {form_data['audience']}
    - Nível: {form_data['difficulty']}
    - Tom: {form_data['tone']}
    - Foco: {form_data['focus']}
    
    ESTRUTURA REQUERIDA:
    1. Título principal e subtítulo
    2. Índice com 6-8 capítulos principais
    3. Para cada capítulo: nome, objetivo e 2-3 subtópicos principais
    4. Elementos especiais (caixas de texto, exercícios, exemplos)
    
    FORMATO DE RESPOSTA:
    # TÍTULO: [Título principal]
    ## SUBTÍTULO: [Subtítulo explicativo]
    
    ## ÍNDICE DETALHADO:
    
    **Introdução** (800 palavras)
    - Apresentação do tema
    - Importância do assunto
    
    **Capítulo 1: [Nome]** (1200 palavras)
    - Subtópico 1.1: [nome]
    - Subtópico 1.2: [nome]
    - Exemplo prático
    
    [Continue para todos os capítulos]
    
    **Conclusão** (600 palavras)
    - Resumo dos pontos principais
    - Próximos passos
    
    TOTAL ESTIMADO: {config['pages'] * 400} palavras
    """
    
    try:
        st.info("📋 Gerando estrutura detalhada do ebook...")
        outline = generate_section_content(llm, outline_prompt)
        st.success("✅ Estrutura criada!")
        
        # Mostrar estrutura para o usuário
        with st.expander("📋 Estrutura do Ebook", expanded=False):
            st.markdown(outline)
        
    except Exception as e:
        st.error(f"Erro na geração da estrutura: {str(e)}")
        return None
    
    # 2. Gerar introdução
    intro_prompt = f"""
    Com base na seguinte estrutura de ebook:
    
    {outline}
    
    Escreva uma INTRODUÇÃO de 500-800 palavras seguindo estas diretrizes:
    
    1. Apresente o tema de forma cativante
    2. Explique a importância do assunto
    3. Apresente os benefícios para o leitor
    4. Visão geral do que será abordado
    5. Conexão com o público-alvo: {form_data['audience']}
    6. Use tom {form_data['tone']} e estilo {config['style']}
    """
    
    try:
        st.info("✍️ Escrevendo introdução...")
        introduction = generate_section_content(llm, intro_prompt)
        st.success("✅ Introdução concluída!")
    except Exception as e:
        st.error(f"Erro na introdução: {str(e)}")
        introduction = f"# Introdução\n\nBem-vindo ao nosso ebook sobre {topic}..."
    
    # 3. Gerar capítulos principais (em lotes menores)
    chapters = []
    chapter_count = min(6, max(4, config['pages'] // 10))  # 4-6 capítulos
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(1, chapter_count + 1):
        try:
            status_text.text(f"✍️ Gerando Capítulo {i}/{chapter_count}...")
            progress_bar.progress((i-1) / chapter_count)
            
            chapter_prompt = f"""
            Com base na estrutura do ebook sobre "{topic}":
            
            {outline}
            
            Escreva o CAPÍTULO {i} com 800-1200 palavras seguindo:
            
            1. Desenvolva os subtópicos indicados
            2. Use estilo {config['style']} e tom {form_data['tone']}
            3. Inclua exemplos práticos
            4. Adicione uma caixa de destaque
            5. Foco no público: {form_data['audience']}
            6. Nível: {form_data['difficulty']}
            
            ESTRUTURA:
            # Capítulo {i}: [Título]
            
            ## Introdução do Capítulo
            [1-2 parágrafos]
            
            ## [Subtópico 1]
            [Desenvolvimento com exemplos]
            
            ## [Subtópico 2]
            [Desenvolvimento com exemplos]
            
            ## 💡 Dica Especial
            [Conteúdo relevante]
            
            ## Resumo do Capítulo
            [Pontos principais]
            """
            
            chapter = generate_section_content(llm, chapter_prompt)
            chapters.append(chapter)
            
            progress_bar.progress(i / chapter_count)
            st.success(f"✅ Capítulo {i} concluído!")
            
            # Pequena pausa para evitar rate limiting
            time.sleep(3)
            
        except Exception as e:
            st.error(f"Erro no Capítulo {i}: {str(e)}")
            chapters.append(f"# Capítulo {i}: Em Desenvolvimento\n\nEste capítulo será desenvolvido...")
    
    # 4. Gerar conclusão
    conclusion_prompt = f"""
    Com base no ebook sobre "{topic}" com esta estrutura:
    
    {outline}
    
    Escreva uma CONCLUSÃO de 500-800 palavras com:
    
    1. Resumo dos principais pontos
    2. Reforço dos benefícios
    3. Sugestões de próximos passos
    4. Recursos adicionais
    5. Mensagem final inspiradora
    6. Mantenha tom {form_data['tone']} e estilo {config['style']}
    """
    
    try:
        st.info("🎯 Finalizando com conclusão...")
        conclusion = generate_section_content(llm, conclusion_prompt)
        st.success("✅ Conclusão concluída!")
    except Exception as e:
        st.error(f"Erro na conclusão: {str(e)}")
        conclusion = f"# Conclusão\n\nEste ebook sobre {topic} apresentou conceitos fundamentais..."
    
    # 5. Montar ebook completo
    full_ebook = f"""# {topic}
*Um Guia Completo e Prático*

---

## Sobre Este Ebook

Este ebook foi desenvolvido especificamente para {form_data['audience']}, abordando {topic} de forma {form_data['difficulty'].lower()} e com foco {form_data['focus'].lower()}.

**Páginas:** {config['pages']}
**Estilo:** {config['style']}
**Tom:** {form_data['tone']}

---

{introduction}

---

"""
    
    # Adicionar todos os capítulos
    for i, chapter in enumerate(chapters, 1):
        full_ebook += f"{chapter}\n\n---\n\n"
    
    # Adicionar conclusão
    full_ebook += f"{conclusion}\n\n---\n\n"
    
    # Adicionar apêndices se solicitado
    if config.get('include_exercises') or config.get('include_images'):
        try:
            st.info("📚 Adicionando apêndices e recursos extras...")
            
            appendix_prompt = f"""
            Crie apêndices para o ebook sobre "{topic}":
            
            1. **Glossário:** 10-15 termos importantes
            2. **Recursos Adicionais:** Livros, sites recomendados
            3. {"**Sugestões de Imagens:** Descrições de imagens relevantes" if config.get('include_images') else ""}
            4. {"**Exercícios Extras:** Atividades complementares" if config.get('include_exercises') else ""}
            """
            
            appendices = generate_section_content(llm, appendix_prompt)
            full_ebook += f"{appendices}\n\n"
            st.success("✅ Apêndices adicionados!")
        except Exception as e:
            st.warning(f"Apêndices não puderam ser gerados: {str(e)}")
    
    # Adicionar footer
    full_ebook += f"""---

## Sobre o Autor

Este ebook foi gerado com inteligência artificial para fornecer conteúdo educativo sobre {topic}.

**Data de criação:** {datetime.now().strftime('%d/%m/%Y')}
**Versão:** 1.0
**Palavras:** ~{len(full_ebook.split()):,}

---

*Obrigado por ler este ebook! Esperamos que o conteúdo seja útil em sua jornada de aprendizado.*
"""
    
    return full_ebook

def create_example_section():
    """Cria seção com exemplos e dicas"""
    st.markdown("""
    <div class="glass-card fade-in">
        <h3 style="color: #60a5fa; margin-bottom: 20px;">💡 Exemplos de Temas Populares</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>📈 Negócios & Empreendedorismo</h4>
            <ul>
                <li>Marketing Digital para PMEs</li>
                <li>Gestão de Equipes Remotas</li>
                <li>Estratégias de Vendas B2B</li>
                <li>Planejamento Financeiro Empresarial</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h4>🛠️ Tecnologia & Desenvolvimento</h4>
            <ul>
                <li>Introdução à Programação Python</li>
                <li>Desenvolvimento de Apps Mobile</li>
                <li>Inteligência Artificial Aplicada</li>
                <li>Segurança em Sistemas Web</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>💡 Desenvolvimento Pessoal</h4>
            <ul>
                <li>Produtividade e Gestão do Tempo</li>
                <li>Comunicação Eficaz</li>
                <li>Liderança e Influência</li>
                <li>Mindfulness e Bem-estar</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h4>🎓 Educação & Conhecimento</h4>
            <ul>
                <li>História Mundial Contemporânea</li>
                <li>Ciências para Leigos</li>
                <li>Filosofia Aplicada ao Cotidiano</li>
                <li>Arte e Cultura Brasileira</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def create_tips_section():
    """Cria seção com dicas"""
    st.markdown("""
    <div class="glass-card fade-in">
        <h3 style="color: #60a5fa; margin-bottom: 20px;">🎯 Dicas para Resultados Excepcionais</h3>
    </div>
    """, unsafe_allow_html=True)
    
    tips = [
        ("🎯", "Seja Específico", "Quanto mais detalhado o tópico, melhor o resultado final"),
        ("👥", "Conheça seu Público", "Defina claramente quem são seus leitores ideais"),
        ("📊", "Use Dados Reais", "Mencione se precisa de estatísticas ou pesquisas atuais"),
        ("💼", "Inclua Casos Práticos", "Solicite exemplos reais e estudos de caso"),
        ("🔄", "Iteração é Chave", "Use as opções avançadas para refinar o conteúdo"),
        ("📱", "Pense Mobile", "Considere como o conteúdo será consumido pelos leitores")
    ]
    
    for icon, title, description in tips:
        st.markdown(f"""
        <div class="feature-card">
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <span style="font-size: 1.5em; margin-right: 15px;">{icon}</span>
                <strong style="color: #60a5fa;">{title}</strong>
            </div>
            <p style="margin: 0; color: #e2e8f0;">{description}</p>
        </div>
        """, unsafe_allow_html=True)

def display_results(ebook_content, config, form_data):
    """Exibe os resultados da geração"""
    # Atualizar estatísticas
    st.session_state.ebooks_generated = st.session_state.get("ebooks_generated", 0) + 1
    st.session_state.total_pages = st.session_state.get("total_pages", 0) + config["pages"]
    
    # Mensagem de sucesso
    st.markdown("""
    <div class="glass-card fade-in" style="text-align: center;">
        <h2 style="color: #10b981; margin-bottom: 20px;">🎉 Ebook Gerado com Sucesso!</h2>
        <p style="color: #cbd5e1;">Seu ebook profissional está pronto para download e visualização.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Métricas do ebook gerado
    col1, col2, col3, col4 = st.columns(4)
    
    word_count = len(ebook_content.split())
    char_count = len(ebook_content)
    estimated_reading_time = max(1, word_count // 200)  # ~200 palavras por minuto
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{config["pages"]}</div>
            <div class="metric-label">Páginas</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{word_count:,}</div>
            <div class="metric-label">Palavras</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{estimated_reading_time}</div>
            <div class="metric-label">Min. Leitura</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{config["format"].split()[1]}</div>
            <div class="metric-label">Formato</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabs para visualização e download
    tab1, tab2, tab3 = st.tabs(["📖 Visualizar", "⬇️ Download", "📊 Detalhes"])
    
    with tab1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown(ebook_content)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Preparar arquivo para download
            try:
                # Limpar o nome do arquivo
                safe_filename = "".join(c for c in form_data['topic'][:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
                filename = f"ebook_{safe_filename.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}"
                
                # Diferentes tipos de arquivo (removido PDF problemático)
                if config["format"] == "🌐 HTML":
                    html_content = markdown_to_html(ebook_content)
                    if html_content:
                        file_data = html_content.encode('utf-8')
                        file_ext = "html"
                        mime_type = "text/html"
                    else:
                        st.error("Erro na conversão para HTML. Usando formato texto.")
                        file_data = ebook_content.encode('utf-8')
                        file_ext = "txt"
                        mime_type = "text/plain"
                elif config["format"] == "📝 Markdown":
                    file_data = ebook_content.encode('utf-8')
                    file_ext = "md"
                    mime_type = "text/markdown"
                else:  # Texto
                    file_data = ebook_content.encode('utf-8')
                    file_ext = "txt"
                    mime_type = "text/plain"
                
                st.download_button(
                    label=f"📥 Baixar Ebook ({config['format']})",
                    data=file_data,
                    file_name=f"{filename}.{file_ext}",
                    mime=mime_type,
                    use_container_width=True
                )
                
                st.success(f"✅ Pronto para download: {filename}.{file_ext}")
                
            except Exception as e:
                st.error(f"❌ Erro ao preparar download: {str(e)}")
                
                # Fallback: oferecer download direto do texto
                st.download_button(
                    label="📝 Baixar como Texto",
                    data=ebook_content.encode('utf-8'),
                    file_name=f"ebook_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        with col2:
            st.info("""
            **📋 Formatos Disponíveis:**
            
            • **Markdown**: Editável e compatível
            • **HTML**: Para web e visualização
            • **Texto**: Simples e universal
            
            📊 **Qualidade:**
            ✅ Estrutura profissional
            ✅ Conteúdo extenso
            ✅ Formatação adequada
            ✅ Pronto para publicação
            """)
    
    with tab3:
        st.markdown("### 📊 Informações Detalhadas")
        
        details = {
            "🎯 Tópico": form_data["topic"],
            "📚 Tipo de Livro": config["book_type"],
            "✍️ Estilo": config["style"],
            "👥 Público-alvo": form_data["audience"],
            "📊 Nível": form_data["difficulty"],
            "🎭 Tom": form_data["tone"],
            "🎯 Foco": form_data["focus"],
            "🌍 Idioma": config["language"],
            "💾 Formato": config["format"],
            "📄 Páginas": config["pages"],
            "📝 Palavras": f"{word_count:,}",
            "📖 Caracteres": f"{char_count:,}",
            "⏱️ Tempo de Leitura": f"{estimated_reading_time} minutos",
            "📅 Gerado em": datetime.now().strftime("%d/%m/%Y às %H:%M")
        }
        
        for key, value in details.items():
            st.markdown(f"**{key}:** {value}")
        
        # Mostrar estrutura se solicitado
        if st.button("📋 Ver Análise de Estrutura"):
            chapters = ebook_content.count("# Capítulo")
            sections = ebook_content.count("## ")
            subsections = ebook_content.count("### ")
            
            st.markdown(f"""
            **📊 Análise Estrutural:**
            - Capítulos identificados: {chapters}
            - Seções principais: {sections}
            - Subseções: {subsections}
            - Densidade: {word_count // max(1, chapters)} palavras/capítulo
            - Profundidade: {'Alta' if subsections > sections else 'Média' if sections > 5 else 'Básica'}
            """)

def main():
    """Função principal da aplicação"""
    # Configuração da página
    st.set_page_config(
        page_title="📚 EBook Generator Pro",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/seu-usuario/ebook-generator',
            'Report a bug': "https://github.com/seu-usuario/ebook-generator/issues",
            'About': "# EBook Generator Pro\nGerador profissional de ebooks com IA"
        }
    )
    
    # Aplicar tema moderno
    apply_modern_theme()
    
    # Inicializar session state
    if "ebooks_generated" not in st.session_state:
        st.session_state.ebooks_generated = 0
    if "total_pages" not in st.session_state:
        st.session_state.total_pages = 0
    
    # Header principal
    create_header()
    
    # Layout principal
    # Sidebar com configurações
    config = create_sidebar()
    
    # Conteúdo principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Formulário principal
        form_data = create_main_form()
        
        # Processamento da geração
        if form_data["submit"] and form_data["topic"]:
            if not config["api_key"]:
                st.error("⚠️ Por favor, configure sua OpenAI API Key na barra lateral")
                st.stop()
            
            # Validação básica do tópico
            if len(form_data["topic"].strip()) < 10:
                st.warning("⚠️ Por favor, forneça uma descrição mais detalhada do tópico (mínimo 10 caracteres)")
                st.stop()
            
            try:
                # Container para o progresso
                with st.container():
                    st.markdown("""
                    <div class="glass-card fade-in">
                        <h3 style="color: #60a5fa; text-align: center;">🚀 Gerando seu Ebook Completo...</h3>
                        <p style="text-align: center; color: #cbd5e1;">Este processo pode levar alguns minutos para garantir qualidade máxima</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Configurar LLM com parâmetros para conteúdo extenso
                    try:
                        llm = OpenAI(
                            openai_api_key=config["api_key"],
                            temperature=0.7,
                            max_tokens=3000,  # Limite seguro por chamada
                            request_timeout=120  # 2 minutos de timeout
                        )
                        st.success("✅ Sistema de IA configurado!")
                    except Exception as e:
                        st.error(f"❌ Erro na configuração da API OpenAI: {str(e)}")
                        st.error("🔑 Verifique se sua API Key está correta e válida")
                        st.stop()
                    
                    # Gerar ebook usando o novo sistema
                    try:
                        ebook_content = generate_comprehensive_ebook(
                            llm=llm,
                            topic=form_data["topic"],
                            config=config,
                            form_data=form_data
                        )
                        
                        # Verificar se o conteúdo foi gerado com sucesso
                        if not ebook_content or len(ebook_content.strip()) < 1000:
                            st.error("❌ Conteúdo gerado é muito curto")
                            st.error("📝 Tente novamente ou reduza o número de páginas")
                            st.stop()
                        
                        # Mostrar estatísticas finais
                        final_word_count = len(ebook_content.split())
                        st.success(f"🎉 Ebook gerado com sucesso! ({final_word_count:,} palavras)")
                        
                    except Exception as e:
                        st.error(f"❌ Erro durante a geração do ebook: {str(e)}")
                        
                        # Mostrar detalhes do erro em modo debug
                        with st.expander("🔍 Detalhes do Erro (Debug)", expanded=False):
                            st.code(traceback.format_exc())
                        
                        st.error("🔄 Sugestões para resolver:")
                        st.error("• Verifique sua conexão com a internet")
                        st.error("• Tente reduzir o número de páginas")
                        st.error("• Simplifique a descrição do tópico")
                        st.error("• Verifique se sua API Key tem créditos suficientes")
                        st.stop()
                    
                    # Exibir resultados
                    display_results(ebook_content, config, form_data)
                    
            except Exception as e:
                st.error(f"❌ Erro crítico na aplicação: {str(e)}")
                
                # Debug completo
                with st.expander("🐛 Debug Completo", expanded=False):
                    st.code(traceback.format_exc())
                
                # Sugestões de solução
                st.markdown("""
                <div class="glass-card">
                    <h4 style="color: #ef4444;">🔧 Possíveis Soluções:</h4>
                    <ul>
                        <li><strong>API Key:</strong> Verifique se sua chave OpenAI está correta e tem créditos</li>
                        <li><strong>Conectividade:</strong> Teste sua conexão com a internet</li>
                        <li><strong>Parâmetros:</strong> Tente simplificar as configurações do ebook</li>
                        <li><strong>Tópico:</strong> Use uma descrição mais clara e específica</li>
                        <li><strong>Reiniciar:</strong> Recarregue a página e tente novamente</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
        
        elif form_data["submit"] and not form_data["topic"]:
            st.warning("📝 Por favor, descreva o tema do seu ebook antes de continuar.")
    
    with col2:
        # Seção de exemplos
        create_example_section()
        
        # Seção de dicas
        create_tips_section()
        
        # Seção de recursos
        st.markdown("""
        <div class="glass-card fade-in">
            <h3 style="color: #60a5fa; margin-bottom: 20px;">🎁 Recursos Inclusos</h3>
            <div class="feature-card">
                <h4>✨ Conteúdo Extenso</h4>
                <p style="color: #e2e8f0;">Ebooks de 10-200 páginas com conteúdo rico e detalhado.</p>
            </div>
            <div class="feature-card">
                <h4>📋 Estrutura Profissional</h4>
                <p style="color: #e2e8f0;">Introdução, múltiplos capítulos, conclusão e apêndices.</p>
            </div>
            <div class="feature-card">
                <h4>🖼️ Sugestões Visuais</h4>
                <p style="color: #e2e8f0;">Descrições de imagens e gráficos para enriquecer seu ebook.</p>
            </div>
            <div class="feature-card">
                <h4>📚 Exercícios Práticos</h4>
                <p style="color: #e2e8f0;">Atividades e reflexões para engajar seus leitores.</p>
            </div>
            <div class="feature-card">
                <h4>📄 Múltiplos Formatos</h4>
                <p style="color: #e2e8f0;">Markdown, HTML e texto puro para máxima compatibilidade.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Seção de suporte
        st.markdown("""
        <div class="glass-card fade-in">
            <h3 style="color: #60a5fa; margin-bottom: 20px;">💬 Suporte & Ajuda</h3>
            <div style="text-align: center;">
                <p style="color: #cbd5e1; margin-bottom: 20px;">Precisa de ajuda ou tem sugestões?</p>
                <div style="display: flex; justify-content: space-around; margin: 20px 0;">
                    <a href="mailto:solarcubix@gmail.com" style="color: #60a5fa; text-decoration: none;">
                        📧 Email
                    </a>
                    <a href="https://github.com/seu-usuario/ebook-generator" style="color: #60a5fa; text-decoration: none;">
                        🐱 GitHub
                    </a>
                    <a href="https://www.linkedin.com/in/filiperangelambrosio/" style="color: #60a5fa; text-decoration: none;">
                        💬 Linkedin
                    </a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer-style">
        <p style="color: #f8fafc;"><strong>📚 EBook Generator Pro</strong> - Powered by OpenAI GPT</p>
        <p style="font-size: 0.9em; color: #cbd5e1;">Versão 2.2 | © 2024 | Feito com ❤️ para criadores de conteúdo</p>
        <p style="font-size: 0.8em; color: #94a3b8;">✨ Interface otimizada e formatos compatíveis!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()