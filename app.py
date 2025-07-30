import streamlit as st
from langchain.llms import OpenAI
import sys
from pathlib import Path
from PIL import Image
import base64
import json
from datetime import datetime

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

def apply_dark_theme():
    """
    Aplica tema escuro personalizado para fundo preto
    """
    st.markdown("""
    <style>
        /* Reset e configurações globais */
        .stApp {
            background-color: #0e1117;
            color: #ffffff;
        }
        
        /* Header personalizado */
        .main-header {
            font-size: 3.5em;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center;
            margin: 20px 0;
            text-shadow: 0 0 30px rgba(102, 126, 234, 0.5);
        }
        
        .sub-header {
            font-size: 1.3em;
            color: #8b92a5;
            text-align: center;
            margin-bottom: 40px;
            font-weight: 300;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #1a1d29;
            border-right: 2px solid #2d3748;
        }
        
        .sidebar .sidebar-content {
            background-color: #1a1d29;
            color: #ffffff;
        }
        
        /* Cards e containers */
        .custom-card {
            background: linear-gradient(145deg, #1e2139, #2d3748);
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
            border: 1px solid #4a5568;
            box-shadow: 
                0 10px 30px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }
        
        .feature-card {
            background: linear-gradient(135deg, #667eea15, #764ba215);
            border-radius: 12px;
            padding: 20px;
            margin: 15px 0;
            border: 1px solid #667eea40;
            transition: all 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(102, 126, 234, 0.2);
            border-color: #667eea80;
        }
        
        /* Botões personalizados */
        .stButton > button {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 12px 30px;
            font-weight: 600;
            font-size: 16px;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
            background: linear-gradient(135deg, #5a6fd8, #6b42a0);
        }
        
        /* Form inputs */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {
            background-color: #2d3748;
            color: #ffffff;
            border: 2px solid #4a5568;
            border-radius: 10px;
            padding: 12px;
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stSelectbox > div > div > select:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        /* Progress bar */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #667eea, #764ba2);
        }
        
        /* Success/Error messages */
        .stSuccess {
            background: linear-gradient(135deg, #10b981, #059669);
            border: none;
            border-radius: 10px;
            color: white;
        }
        
        .stError {
            background: linear-gradient(135deg, #ef4444, #dc2626);
            border: none;
            border-radius: 10px;
            color: white;
        }
        
        .stWarning {
            background: linear-gradient(135deg, #f59e0b, #d97706);
            border: none;
            border-radius: 10px;
            color: white;
        }
        
        .stInfo {
            background: linear-gradient(135deg, #3b82f6, #2563eb);
            border: none;
            border-radius: 10px;
            color: white;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            background-color: #2d3748;
            border-radius: 10px;
            color: #ffffff;
            font-weight: 600;
        }
        
        .streamlit-expanderContent {
            background-color: #1a1d29;
            border-radius: 0 0 10px 10px;
        }
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: #2d3748;
            border-radius: 10px 10px 0 0;
            color: #8b92a5;
            font-weight: 600;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }
        
        /* Slider customization */
        .stSlider > div > div > div > div {
            background: linear-gradient(90deg, #667eea, #764ba2);
        }
        
        /* Radio buttons */
        .stRadio > div {
            background-color: #2d3748;
            border-radius: 10px;
            padding: 15px;
        }
        
        /* Metrics styling */
        .metric-card {
            background: linear-gradient(145deg, #1e2139, #2d3748);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            border: 1px solid #4a5568;
            margin: 10px 0;
        }
        
        .metric-value {
            font-size: 2.5em;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .metric-label {
            color: #8b92a5;
            font-size: 0.9em;
            margin-top: 5px;
        }
        
        /* Animation classes */
        .fade-in {
            animation: fadeInUp 0.8s ease-out;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Glassmorphism effect */
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 25px;
            margin: 20px 0;
        }
        
        /* Loading spinner */
        .custom-spinner {
            border: 4px solid rgba(102, 126, 234, 0.3);
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Scrollbar customization */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #1a1d29;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #5a6fd8, #6b42a0);
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
            <h2 style="color: #667eea; margin: 10px 0;">Configurações</h2>
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
                min_value=5,
                max_value=200,
                value=25,
                step=5,
                help="Tamanho aproximado do ebook"
            )
            
            # Estimativa de palavras
            estimated_words = ebook_pages * 250  # ~250 palavras por página
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
                ["📄 PDF", "📝 Markdown", "🌐 HTML", "📊 EPUB"],
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

def create_example_section():
    """Cria seção com exemplos e dicas"""
    st.markdown("""
    <div class="glass-card fade-in">
        <h3 style="color: #667eea; margin-bottom: 20px;">💡 Exemplos de Temas Populares</h3>
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
        <h3 style="color: #667eea; margin-bottom: 20px;">🎯 Dicas para Resultados Excepcionais</h3>
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
                <strong style="color: #667eea;">{title}</strong>
            </div>
            <p style="margin: 0; color: #8b92a5;">{description}</p>
        </div>
        """, unsafe_allow_html=True)

def validate_and_prepare_params(form_data, config):
    """Valida e prepara parâmetros para evitar erros de chaves faltantes"""
    
    # Mapear tipos de livro para objetivos principais
    objective_mapping = {
        "📈 Negócios": "Ensinar estratégias e práticas de negócios eficazes",
        "🛠️ Técnico": "Explicar conceitos técnicos de forma clara e aplicável",
        "💡 Autoajuda": "Inspirar e guiar o desenvolvimento pessoal",
        "🎓 Educacional": "Educar e informar sobre o tema de forma didática",
        "📝 Narrativo": "Contar uma história envolvente e significativa"
    }
    
    # Mapear dificuldade para depth_level
    depth_mapping = {
        "Iniciante": "Básico e acessível",
        "Intermediário": "Intermediário com exemplos práticos",
        "Avançado": "Avançado com análises profundas",
        "Especialista": "Especialista com insights técnicos"
    }
    
    # Preparar parâmetros completos
    params = {
        "topic": form_data["topic"],
        "style": config["style"],
        "pages": config["pages"],
        "target_audience": form_data["audience"],
        "depth_level": depth_mapping.get(form_data["difficulty"], "Intermediário com exemplos práticos"),
        "main_objective": objective_mapping.get(config["book_type"], "Educar sobre o tema de forma clara"),
        "tone": form_data["tone"],
        "focus": form_data["focus"],
        "key_points": form_data["key_points"],
        "special_requirements": form_data["special_requirements"],
        "language": config["language"],
        "include_images": config["include_images"],
        "include_exercises": config["include_exercises"],
        "book_type": config["book_type"],
        "difficulty": form_data["difficulty"],
        "audience": form_data["audience"]
    }
    
    return params

def create_ebook_chain(llm):
    """Cria a cadeia completa de geração de ebooks"""
    outline_chain = create_outline_chain(llm)
    writing_chain = create_writing_chain(llm)
    
    def combined_chain(**params):
        # Garantir que todos os parâmetros necessários estão presentes
        required_params = {
            "topic": params.get("topic", "Tópico não especificado"),
            "style": params.get("style", "Profissional"),
            "length": params.get("pages", 25),
            "target_audience": params.get("target_audience", "Adultos interessados no tema"),
            "depth_level": params.get("depth_level", "Intermediário com exemplos práticos"),
            "main_objective": params.get("main_objective", "Educar sobre o tema de forma clara")
        }
        
        # Adicionar parâmetros extras
        extra_params = {k: v for k, v in params.items() 
                       if k not in ["pages"] and v is not None}
        
        outline_params = {**required_params, **extra_params}
        
        try:
            outline = outline_chain.run(**outline_params)
        except Exception as e:
            st.error(f"Erro ao gerar estrutura: {str(e)}")
            # Fallback com parâmetros mínimos
            outline = outline_chain.run(
                topic=params["topic"],
                style=params["style"],
                length=params["pages"]
            )
        
        # Parâmetros para escrita
        writing_params = {
            "outline": outline,
            "topic": params["topic"],
            "style": params["style"],
            "target_audience": params["target_audience"],
            "depth_level": params["depth_level"],
            "main_objective": params["main_objective"]
        }
        
        # Adicionar outros parâmetros se existirem
        for key in ["tone", "focus", "key_points", "special_requirements", 
                   "language", "include_images", "include_exercises"]:
            if key in params and params[key]:
                writing_params[key] = params[key]
        
        try:
            ebook = writing_chain.run(**writing_params)
        except Exception as e:
            st.error(f"Erro ao gerar conteúdo: {str(e)}")
            # Fallback com parâmetros mínimos
            ebook = writing_chain.run(
                outline=outline,
                topic=params["topic"],
                style=params["style"]
            )
        
        return ebook
    
    return combined_chain

def display_generation_progress():
    """Exibe progresso da geração com animação"""
    progress_steps = [
        ("🔍", "Analisando o tópico..."),
        ("📋", "Criando estrutura do ebook..."),
        ("✍️", "Gerando conteúdo dos capítulos..."),
        ("🎨", "Formatando e organizando..."),
        ("📄", "Finalizando o documento..."),
        ("✅", "Ebook concluído!")
    ]
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, (icon, message) in enumerate(progress_steps):
        progress = (i + 1) / len(progress_steps)
        progress_bar.progress(progress)
        status_text.markdown(f"""
        <div style="text-align: center; padding: 10px;">
            <span style="font-size: 2em;">{icon}</span>
            <p style="margin: 10px 0; color: #667eea; font-weight: 600;">{message}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Simula tempo de processamento
        import time
        time.sleep(1)
    
    return progress_bar, status_text

def display_results(ebook_content, config, form_data):
    """Exibe os resultados da geração"""
    # Atualizar estatísticas
    st.session_state.ebooks_generated = st.session_state.get("ebooks_generated", 0) + 1
    st.session_state.total_pages = st.session_state.get("total_pages", 0) + config["pages"]
    
    # Mensagem de sucesso
    st.markdown("""
    <div class="glass-card fade-in" style="text-align: center;">
        <h2 style="color: #10b981; margin-bottom: 20px;">🎉 Ebook Gerado com Sucesso!</h2>
        <p style="color: #8b92a5;">Seu ebook profissional está pronto para download e visualização.</p>
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
            # Gerar arquivo para download
            try:
                ebook_path = save_ebook(
                    content=ebook_content,
                    title=form_data["topic"][:50],
                    format=config["format"].lower().split()[1]
                )
                
                with open(ebook_path, "rb") as f:
                    file_data = f.read()
                
                filename = f"ebook_{form_data['topic'][:30].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}"
                file_extension = config["format"].lower().split()[1]
                
                mime_types = {
                    "pdf": "application/pdf",
                    "markdown": "text/markdown",
                    "html": "text/html",
                    "epub": "application/epub+zip"
                }
                
                st.download_button(
                    label=f"📥 Baixar Ebook ({config['format']})",
                    data=file_data,
                    file_name=f"{filename}.{file_extension}",
                    mime=mime_types.get(file_extension, "text/plain"),
                    use_container_width=True
                )
                
                st.success(f"✅ Arquivo salvo como: {filename}.{file_extension}")
                
            except Exception as e:
                st.error(f"❌ Erro ao preparar download: {str(e)}")
        
        with col2:
            st.info("""
            **📋 Formatos Disponíveis:**
            
            • **PDF**: Melhor para leitura
            • **Markdown**: Editável 
            • **HTML**: Web-friendly
            • **EPUB**: E-readers
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
            "⏱️ Tempo de Leitura": f"{estimated_reading_time} minutos",
            "📅 Gerado em": datetime.now().strftime("%d/%m/%Y às %H:%M")
        }
        
        for key, value in details.items():
            st.markdown(f"**{key}:** {value}")

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
    
    # Aplicar tema escuro
    apply_dark_theme()
    
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
            
            try:
                # Container para o progresso
                with st.container():
                    st.markdown("""
                    <div class="glass-card fade-in">
                        <h3 style="color: #667eea; text-align: center;">🚀 Gerando seu Ebook...</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Mostrar progresso
                    progress_bar, status_text = display_generation_progress()
                    
                    # Configurar LLM
                    llm = OpenAI(
                        openai_api_key=config["api_key"],
                        temperature=0.7,
                        max_tokens=4000
                    )
                    
                    # Criar cadeia de geração
                    ebook_chain = create_ebook_chain(llm)
                    
                    # Preparar parâmetros com validação completa
                    generation_params = validate_and_prepare_params(form_data, config)
                    
                    # Gerar ebook com parâmetros validados
                    ebook_content = ebook_chain(**generation_params)
                    
                    # Limpar progresso
                    progress_bar.empty()
                    status_text.empty()
                    
                    # Exibir resultados
                    display_results(ebook_content, config, form_data)
                    
            except Exception as e:
                st.error(f"❌ Erro durante a geração do ebook: {str(e)}")
                st.exception(e)
                
                # Sugestões de solução
                st.markdown("""
                <div class="glass-card">
                    <h4 style="color: #ef4444;">🔧 Possíveis Soluções:</h4>
                    <ul>
                        <li>Verifique se sua API Key está correta</li>
                        <li>Tente reduzir o tamanho do ebook</li>
                        <li>Simplifique a descrição do tópico</li>
                        <li>Verifique sua conexão com a internet</li>
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
            <h3 style="color: #667eea; margin-bottom: 20px;">🎁 Recursos Inclusos</h3>
            <div class="feature-card">
                <h4>✨ Conteúdo Profissional</h4>
                <p style="color: #8b92a5;">Estrutura completa com introdução, capítulos organizados e conclusão impactante.</p>
            </div>
            <div class="feature-card">
                <h4>🖼️ Sugestões Visuais</h4>
                <p style="color: #8b92a5;">Descrições de imagens e gráficos para enriquecer seu ebook.</p>
            </div>
            <div class="feature-card">
                <h4>📚 Exercícios Práticos</h4>
                <p style="color: #8b92a5;">Atividades e reflexões para engajar seus leitores.</p>
            </div>
            <div class="feature-card">
                <h4>📄 Múltiplos Formatos</h4>
                <p style="color: #8b92a5;">PDF, Markdown, HTML e EPUB para máxima compatibilidade.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Seção de suporte
        st.markdown("""
        <div class="glass-card fade-in">
            <h3 style="color: #667eea; margin-bottom: 20px;">💬 Suporte & Ajuda</h3>
            <div style="text-align: center;">
                <p style="color: #8b92a5; margin-bottom: 20px;">Precisa de ajuda ou tem sugestões?</p>
                <div style="display: flex; justify-content: space-around; margin: 20px 0;">
                    <a href="mailto:suporte@ebookgenerator.com" style="color: #667eea; text-decoration: none;">
                        📧 Email
                    </a>
                    <a href="https://github.com/seu-usuario/ebook-generator" style="color: #667eea; text-decoration: none;">
                        🐱 GitHub
                    </a>
                    <a href="https://discord.gg/seu-servidor" style="color: #667eea; text-decoration: none;">
                        💬 Discord
                    </a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 20px 0; color: #8b92a5;">
        <p>📚 <strong>EBook Generator Pro</strong> - Powered by OpenAI GPT</p>
        <p style="font-size: 0.8em;">Versão 2.0 | © 2024 | Feito com ❤️ para criadores de conteúdo</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()