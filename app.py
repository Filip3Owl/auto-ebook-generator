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
    2. Índice completo com pelo menos 8-12 capítulos
    3. Para cada capítulo: nome, objetivo, subtópicos (3-5 por capítulo)
    4. Estimativa de palavras por capítulo
    5. Elementos especiais (caixas de texto, exercícios, exemplos)
    
    FORMATO DE RESPOSTA:
    # TÍTULO: [Título principal]
    ## SUBTÍTULO: [Subtítulo explicativo]
    
    ## ÍNDICE DETALHADO:
    
    **Introdução** (800 palavras)
    - Apresentação do tema
    - Importância do assunto
    - O que o leitor aprenderá
    
    **Capítulo 1: [Nome]** (1200 palavras)
    - Subtópico 1.1: [nome]
    - Subtópico 1.2: [nome]
    - Subtópico 1.3: [nome]
    - Exemplo prático
    - Exercício
    
    [Continue para todos os capítulos]
    
    **Conclusão** (600 palavras)
    - Resumo dos pontos principais
    - Próximos passos
    - Recursos adicionais
    
    **Apêndices** (400 palavras)
    - Glossário
    - Recursos extras
    - Bibliografia
    
    TOTAL ESTIMADO: {config['pages'] * 400} palavras
    """
    
    try:
        st.info("📋 Gerando estrutura detalhada do ebook...")
        outline = llm(outline_prompt)
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
    
    Escreva uma INTRODUÇÃO COMPLETA E DETALHADA de pelo menos 800 palavras.
    
    A introdução deve:
    1. Apresentar o tema de forma cativante
    2. Explicar a importância e relevância do assunto
    3. Apresentar os benefícios que o leitor obterá
    4. Dar uma visão geral do que será abordado
    5. Estabelecer conexão com o público-alvo: {form_data['audience']}
    6. Usar tom {form_data['tone']} e estilo {config['style']}
    
    Inclua pelo menos 3 parágrafos substanciais com exemplos ou estatísticas quando relevante.
    """
    
    try:
        st.info("✍️ Escrevendo introdução...")
        introduction = llm(intro_prompt)
        st.success("✅ Introdução concluída!")
    except Exception as e:
        st.error(f"Erro na introdução: {str(e)}")
        introduction = f"# Introdução\n\nBem-vindo ao nosso ebook sobre {topic}..."
    
    # 3. Gerar capítulos principais (em lotes)
    chapters = []
    chapter_count = min(8, max(6, config['pages'] // 8))  # Entre 6-8 capítulos
    
    for i in range(1, chapter_count + 1):
        chapter_prompt = f"""
        Com base na estrutura do ebook sobre "{topic}":
        
        {outline}
        
        Escreva o CAPÍTULO {i} COMPLETO com pelo menos 1200-1500 palavras.
        
        REQUISITOS:
        1. Siga a estrutura definida no índice
        2. Desenvolva todos os subtópicos indicados
        3. Use estilo {config['style']} e tom {form_data['tone']}
        4. Inclua exemplos práticos e detalhados
        5. Adicione pelo menos uma caixa de destaque ou dica
        6. Termine com um resumo do capítulo
        7. Foque no público: {form_data['audience']}
        8. Nível: {form_data['difficulty']}
        
        {f"PONTOS IMPORTANTES A INCLUIR: {form_data['key_points']}" if form_data['key_points'] else ""}
        {f"REQUISITOS ESPECIAIS: {form_data['special_requirements']}" if form_data['special_requirements'] else ""}
        
        ESTRUTURA DO CAPÍTULO:
        # Capítulo {i}: [Título]
        
        ## Introdução do Capítulo
        [2-3 parágrafos introdutórios]
        
        ## [Subtópico 1]
        [Desenvolvimento detalhado com exemplos]
        
        ## [Subtópico 2]
        [Desenvolvimento detalhado com exemplos]
        
        ## [Subtópico 3]
        [Desenvolvimento detalhado com exemplos]
        
        ## 💡 Dica Especial / Caixa de Destaque
        [Conteúdo relevante e prático]
        
        ## Exemplo Prático
        [Caso real ou simulado detalhado]
        
        ## Resumo do Capítulo
        [Pontos principais em 2-3 parágrafos]
        
        ## ✏️ Exercício / Reflexão
        [Atividade prática para o leitor]
        """
        
        try:
            st.info(f"✍️ Escrevendo Capítulo {i}...")
            progress = st.progress((i-1) / chapter_count)
            
            chapter = llm(chapter_prompt)
            chapters.append(chapter)
            
            progress.progress(i / chapter_count)
            st.success(f"✅ Capítulo {i} concluído!")
            
            # Pequena pausa para evitar rate limiting
            time.sleep(2)
            
        except Exception as e:
            st.error(f"Erro no Capítulo {i}: {str(e)}")
            chapters.append(f"# Capítulo {i}: Em Desenvolvimento\n\nEste capítulo será desenvolvido...")
    
    # 4. Gerar conclusão
    conclusion_prompt = f"""
    Com base no ebook completo sobre "{topic}" com a seguinte estrutura:
    
    {outline}
    
    E considerando os capítulos desenvolvidos, escreva uma CONCLUSÃO COMPLETA de pelo menos 600-800 palavras.
    
    A conclusão deve:
    1. Resumir os principais pontos abordados no ebook
    2. Reforçar os benefícios e aprendizados
    3. Motivar o leitor à ação
    4. Sugerir próximos passos práticos
    5. Incluir recursos adicionais para aprofundamento
    6. Terminar com uma mensagem inspiradora
    7. Manter tom {form_data['tone']} e estilo {config['style']}
    
    ESTRUTURA:
    # Conclusão
    
    ## Recapitulando Nossa Jornada
    [Resumo dos principais pontos]
    
    ## Seus Próximos Passos
    [Ações práticas e recomendações]
    
    ## Recursos Adicionais
    [Sugestões de livros, sites, cursos]
    
    ## Palavras Finais
    [Mensagem motivacional e inspiradora]
    """
    
    try:
        st.info("🎯 Finalizando com conclusão...")
        conclusion = llm(conclusion_prompt)
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
        appendix_prompt = f"""
        Crie apêndices complementares para o ebook sobre "{topic}":
        
        1. **Glossário:** 15-20 termos importantes com definições
        2. **Recursos Adicionais:** Lista de livros, sites, ferramentas recomendadas
        3. **Templates/Checklists:** Materiais práticos para aplicação
        4. {"**Sugestões de Imagens:** Descrições de imagens relevantes para cada capítulo" if config.get('include_images') else ""}
        5. {"**Exercícios Extras:** Atividades complementares de aprofundamento" if config.get('include_exercises') else ""}
        
        Mantenha o mesmo tom {form_data['tone']} e seja prático e útil.
        """
        
        try:
            st.info("📚 Adicionando apêndices e recursos extras...")
            appendices = llm(appendix_prompt)
            full_ebook += f"{appendices}\n\n"
            st.success("✅ Apêndices adicionados!")
        except Exception as e:
            st.warning(f"Apêndices não puderam ser gerados: {str(e)}")
    
    # Adicionar footer
    full_ebook += f"""---

## Sobre o Autor

Este ebook foi gerado com inteligência artificial para fornecer conteúdo educativo e prático sobre {topic}.

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

def display_generation_progress(total_steps):
    """Exibe progresso da geração com animação"""
    progress_steps = [
        ("🔍", "Analisando o tópico..."),
        ("📋", "Criando estrutura detalhada..."),
        ("📝", "Escrevendo introdução..."),
        ("✍️", "Gerando capítulos principais..."),
        ("🎯", "Desenvolvendo conclusão..."),
        ("📚", "Adicionando apêndices..."),
        ("🎨", "Formatando documento..."),
        ("✅", "Ebook concluído!")
    ]
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    return progress_bar, status_text, progress_steps

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
            # Preparar arquivo para download
            try:
                filename = f"ebook_{form_data['topic'][:30].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}"
                file_extension = config["format"].lower().split()[1]
                
                # Diferentes tipos de arquivo
                if file_extension == "markdown":
                    file_data = ebook_content.encode('utf-8')
                    mime_type = "text/markdown"
                elif file_extension == "html":
                    html_content = f"""
                    <!DOCTYPE html>
                    <html lang="pt-BR">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>{form_data['topic']}</title>
                        <style>
                            body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
                            h1, h2, h3 {{ color: #333; }}
                            h1 {{ border-bottom: 3px solid #667eea; padding-bottom: 10px; }}
                            h2 {{ border-bottom: 1px solid #ddd; padding-bottom: 5px; }}
                            .highlight {{ background: #f0f8ff; padding: 15px; border-left: 4px solid #667eea; margin: 20px 0; }}
                            code {{ background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }}
                            blockquote {{ background: #f9f9f9; border-left: 4px solid #ddd; margin: 0; padding: 10px 20px; }}
                        </style>
                    </head>
                    <body>
                    {ebook_content.replace('#', '<h1>').replace('##', '<h2>').replace('###', '<h3>')}
                    </body>
                    </html>
                    """
                    file_data = html_content.encode('utf-8')
                    mime_type = "text/html"
                else:
                    file_data = ebook_content.encode('utf-8')
                    mime_type = "text/plain"
                
                st.download_button(
                    label=f"📥 Baixar Ebook ({config['format']})",
                    data=file_data,
                    file_name=f"{filename}.{file_extension}",
                    mime=mime_type,
                    use_container_width=True
                )
                
                st.success(f"✅ Pronto para download: {filename}.{file_extension}")
                
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
            
            • **PDF**: Melhor para leitura
            • **Markdown**: Editável 
            • **HTML**: Web-friendly
            • **EPUB**: E-readers
            
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
            
            # Validação básica do tópico
            if len(form_data["topic"].strip()) < 10:
                st.warning("⚠️ Por favor, forneça uma descrição mais detalhada do tópico (mínimo 10 caracteres)")
                st.stop()
            
            try:
                # Container para o progresso
                with st.container():
                    st.markdown("""
                    <div class="glass-card fade-in">
                        <h3 style="color: #667eea; text-align: center;">🚀 Gerando seu Ebook Completo...</h3>
                        <p style="text-align: center; color: #8b92a5;">Este processo pode levar alguns minutos para garantir qualidade máxima</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Configurar LLM com parâmetros para conteúdo extenso
                    try:
                        llm = OpenAI(
                            openai_api_key=config["api_key"],
                            temperature=0.7,
                            max_tokens=20000,  # Aumentado para mais conteúdo
                            request_timeout=180  # 3 minutos de timeout
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
            <h3 style="color: #667eea; margin-bottom: 20px;">🎁 Recursos Inclusos</h3>
            <div class="feature-card">
                <h4>✨ Conteúdo Extenso</h4>
                <p style="color: #8b92a5;">Ebooks de 10-200 páginas com conteúdo rico e detalhado.</p>
            </div>
            <div class="feature-card">
                <h4>📋 Estrutura Profissional</h4>
                <p style="color: #8b92a5;">Introdução, múltiplos capítulos, conclusão e apêndices.</p>
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
                <p style="color: #8b92a5;">Markdown, HTML e texto puro para máxima compatibilidade.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Seção de performance
        st.markdown("""
        <div class="glass-card fade-in">
            <h3 style="color: #667eea; margin-bottom: 20px;">⚡ Performance Melhorada</h3>
            <div class="feature-card">
                <h4>🚀 Sistema Otimizado</h4>
                <p style="color: #8b92a5;">Geração em múltiplas etapas para conteúdo mais extenso e detalhado.</p>
            </div>
            <div class="feature-card">
                <h4>📊 Controle de Qualidade</h4>
                <p style="color: #8b92a5;">Validação automática de estrutura e tamanho do conteúdo.</p>
            </div>
            <div class="feature-card">
                <h4>🔧 Recuperação de Erros</h4>
                <p style="color: #8b92a5;">Sistema robusto que continua funcionando mesmo com falhas parciais.</p>
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
        <p style="font-size: 0.8em;">Versão 2.1 | © 2024 | Feito com ❤️ para criadores de conteúdo</p>
        <p style="font-size: 0.7em;">✨ Agora com geração de conteúdo extenso e detalhado!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()