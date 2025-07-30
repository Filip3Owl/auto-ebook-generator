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
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import markdown
import io

# Configura paths para imports
sys.path.append(str(Path(__file__).parent))

# Importações locais (comentadas para evitar erros se não existirem)
# from core.prompts import EBOOK_PROMPTS
# from agents.outline import create_outline_chain
# from agents.writer import create_writing_chain
# from utils.file_io import save_ebook
# from utils.config import load_config

# Configuração inicial
# load_config()

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
            padding: 25px;
            margin: 15px 0;
            border: 1px solid #667eea40;
            transition: all 0.3s ease;
            min-height: 180px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(102, 126, 234, 0.2);
            border-color: #667eea80;
        }
        
        .feature-card h4 {
            color: #667eea;
            font-size: 1.1em;
            font-weight: 700;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .feature-card ul {
            list-style: none;
            padding: 0;
            margin: 0;
            flex-grow: 1;
        }
        
        .feature-card li {
            background: rgba(255, 255, 255, 0.05);
            padding: 8px 12px;
            margin: 6px 0;
            border-radius: 6px;
            border-left: 3px solid #667eea;
            color: #e2e8f0;
            font-size: 0.9em;
            transition: all 0.2s ease;
        }
        
        .feature-card li:hover {
            background: rgba(102, 126, 234, 0.1);
            transform: translateX(5px);
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
        
        /* Fix para responsividade */
        @media (max-width: 768px) {
            .feature-card {
                min-height: auto;
                padding: 20px;
            }
            
            .main-header {
                font-size: 2.5em;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def create_pdf_content(content, title):
    """
    Cria um PDF a partir do conteúdo markdown
    """
    try:
        # Criar um buffer de bytes para o PDF
        buffer = io.BytesIO()
        
        # Configurar o documento PDF
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Definir estilos
        styles = getSampleStyleSheet()
        
        # Estilo personalizado para título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=HexColor('#667eea'),
            alignment=1  # Centro
        )
        
        # Estilo para capítulos
        chapter_style = ParagraphStyle(
            'CustomChapter',
            parent=styles['Heading2'],
            fontSize=16,
            spaceBefore=20,
            spaceAfter=12,
            textColor=HexColor('#764ba2')
        )
        
        # Estilo para seções
        section_style = ParagraphStyle(
            'CustomSection',
            parent=styles['Heading3'],
            fontSize=14,
            spaceBefore=15,
            spaceAfter=8,
            textColor=HexColor('#667eea')
        )
        
        # Estilo para texto normal
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            textColor=HexColor('#333333'),
            alignment=0  # Justificado
        )
        
        # Lista para armazenar elementos do PDF
        story = []
        
        # Processar o conteúdo markdown linha por linha
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            
            if not line:
                story.append(Spacer(1, 6))
                continue
            
            # Títulos principais (# )
            if line.startswith('# ') and not line.startswith('## '):
                text = line[2:].strip()
                if 'Capítulo' in text:
                    story.append(PageBreak())
                story.append(Paragraph(text, chapter_style))
                story.append(Spacer(1, 12))
            
            # Subtítulos (## )
            elif line.startswith('## '):
                text = line[3:].strip()
                story.append(Paragraph(text, section_style))
                story.append(Spacer(1, 8))
            
            # Sub-subtítulos (### )
            elif line.startswith('### '):
                text = line[4:].strip()
                subsection_style = ParagraphStyle(
                    'CustomSubsection',
                    parent=styles['Heading4'],
                    fontSize=12,
                    spaceBefore=10,
                    spaceAfter=6,
                    textColor=HexColor('#555555')
                )
                story.append(Paragraph(text, subsection_style))
                story.append(Spacer(1, 6))
            
            # Linhas horizontais
            elif line.startswith('---'):
                story.append(Spacer(1, 20))
                # Adicionar uma linha visual
                from reportlab.platypus import Table
                line_table = Table([['']]*1, colWidths=[7*inch])
                line_table.setStyle([
                    ('LINEBELOW', (0,0), (-1,-1), 1, HexColor('#667eea')),
                ])
                story.append(line_table)
                story.append(Spacer(1, 20))
            
            # Texto normal
            elif line and not line.startswith('*') and not line.startswith('©'):
                # Processar formatação básica
                text = line.replace('**', '<b>').replace('**', '</b>')
                text = text.replace('*', '<i>').replace('*', '</i>')
                
                # Remover caracteres markdown não suportados
                text = text.replace('`', '"')
                
                story.append(Paragraph(text, normal_style))
                story.append(Spacer(1, 4))
        
        # Gerar o PDF
        doc.build(story)
        
        # Retornar os bytes do PDF
        buffer.seek(0)
        return buffer.getvalue()
        
    except Exception as e:
        st.error(f"Erro ao gerar PDF: {str(e)}")
        return None

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
            
            # Tamanho do ebook (reduzido para evitar erros de token)
            ebook_pages = st.slider(
                "📄 Número de Páginas",
                min_value=10,
                max_value=100,  # Reduzido de 200 para 100
                value=30,       # Reduzido de 50 para 30
                step=5,
                help="Tamanho aproximado do ebook"
            )
            
            # Número de capítulos
            num_chapters = st.slider(
                "📚 Número de Capítulos",
                min_value=3,
                max_value=10,
                value=5,
                step=1,
                help="Quantidade de capítulos principais"
            )
            
            # Estimativa de palavras
            estimated_words = ebook_pages * 300  # Reduzido de 400 para 300 palavras por página
            st.info(f"📊 Estimativa: ~{estimated_words:,} palavras em {num_chapters} capítulos")
            
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
                index=0,  # Padrão para PDF
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
            "num_chapters": num_chapters,
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
            placeholder="📝 Exemplo:\n• Introdução ao Marketing Digital\n• Python para Iniciantes\n• Gestão de Tempo e Produtividade\n• História do Brasil Colonial",
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
                    ["Iniciante", "Intermediário", "Avançado"],
                    index=0
                )
            
            with col2:
                tone = st.selectbox(
                    "🎭 Tom do Conteúdo",
                    ["Conversacional", "Formal", "Técnico", "Inspiracional"],
                    index=0
                )
                
                focus_area = st.selectbox(
                    "🎯 Foco Principal",
                    ["Prático", "Teórico", "Balanceado", "Case Studies"],
                    index=0
                )
            
            key_points = st.text_area(
                "📋 Pontos-chave para incluir (opcional)",
                placeholder="• Conceitos fundamentais\n• Exemplos práticos\n• Dicas de implementação",
                height=100,
                help="Liste os principais tópicos que devem ser abordados"
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
        "submit": submit_button
    }

def generate_optimized_ebook(llm, topic, config, form_data):
    """
    Gera um ebook completo com controle otimizado de tokens
    """
    
    # Calcular parâmetros baseados no tamanho desejado
    num_chapters = config['num_chapters']
    words_per_chapter = (config['pages'] * 300) // (num_chapters + 2)  # +2 para intro e conclusão
    
    # 1. Gerar estrutura concisa
    outline_prompt = f"""Crie uma estrutura para um ebook sobre: {topic}

ESPECIFICAÇÕES:
- {num_chapters} capítulos principais
- Público: {form_data['audience']}
- Nível: {form_data['difficulty']}
- Tom: {form_data['tone']}
- Estilo: {config['style']}

FORMATO:
TÍTULO: [título atrativo]

CAPÍTULOS:
1. [Nome do Capítulo 1] - [breve descrição]
2. [Nome do Capítulo 2] - [breve descrição]
[...continue até {num_chapters}]

Mantenha conciso (máximo 300 palavras)."""
    
    try:
        st.info("📋 Criando estrutura...")
        outline = llm.predict(outline_prompt, max_tokens=500)
        st.success("✅ Estrutura criada!")
        
        with st.expander("📋 Estrutura do Ebook", expanded=False):
            st.text(outline)
        
    except Exception as e:
        st.error(f"Erro na estrutura: {str(e)}")
        return None
    
    # 2. Gerar introdução
    intro_prompt = f"""Escreva uma introdução completa para o ebook "{topic}".

REQUISITOS:
- Público: {form_data['audience']}
- Tom: {form_data['tone']}
- 400-600 palavras
- Apresente o tema e sua importância
- Explique o que o leitor aprenderá
- Use linguagem {form_data['tone'].lower()}

Seja direto e envolvente."""
    
    try:
        st.info("✍️ Escrevendo introdução...")
        introduction = llm.predict(intro_prompt, max_tokens=800)
        st.success("✅ Introdução concluída!")
    except Exception as e:
        st.error(f"Erro na introdução: {str(e)}")
        introduction = f"# Introdução\n\nBem-vindo ao ebook sobre {topic}..."
    
    # 3. Gerar capítulos um por vez
    chapters = []
    
    for i in range(1, num_chapters + 1):
        chapter_prompt = f"""Escreva o Capítulo {i} do ebook sobre "{topic}".

BASEADO NA ESTRUTURA:
{outline}

REQUISITOS:
- {words_per_chapter}-{words_per_chapter + 200} palavras
- Tom: {form_data['tone']}
- Nível: {form_data['difficulty']}
- Inclua exemplos práticos
- Termine com resumo do capítulo

ESTRUTURA:
# Capítulo {i}: [Título]

[Conteúdo desenvolvido com exemplos]

## Resumo do Capítulo
[Pontos principais]

Foque na qualidade e aplicabilidade prática."""
        
        try:
            st.info(f"✍️ Capítulo {i}/{num_chapters}...")
            progress = st.progress(i / (num_chapters + 2))
            
            chapter = llm.predict(chapter_prompt, max_tokens=1200)
            chapters.append(chapter)
            
            st.success(f"✅ Capítulo {i} concluído!")
            time.sleep(1)  # Pausa para evitar rate limiting
            
        except Exception as e:
            st.error(f"Erro no Capítulo {i}: {str(e)}")
            chapters.append(f"# Capítulo {i}: Em Desenvolvimento\n\nEste capítulo será desenvolvido em breve...")
    
    # 4. Gerar conclusão
    conclusion_prompt = f"""Escreva uma conclusão impactante para o ebook "{topic}".

REQUISITOS:
- 300-500 palavras
- Resume os pontos principais
- Motiva à ação
- Tom: {form_data['tone']}
- Inclua próximos passos práticos

ESTRUTURA:
# Conclusão

[Resumo dos aprendizados]

## Seus Próximos Passos
[Ações práticas]

## Palavras Finais
[Mensagem inspiradora]"""
    
    try:
        st.info("🎯 Finalizando...")
        progress = st.progress(1.0)
        conclusion = llm.predict(conclusion_prompt, max_tokens=600)
        st.success("✅ Conclusão concluída!")
    except Exception as e:
        st.error(f"Erro na conclusão: {str(e)}")
        conclusion = f"# Conclusão\n\nEste ebook sobre {topic} apresentou conceitos fundamentais..."
    
    # 5. Montar ebook completo
    full_ebook = f"""# {topic}
*Um Guia Prático e Completo*

---

## Informações do Ebook

**Autor:** EBook Generator Pro  
**Páginas:** {config['pages']}  
**Capítulos:** {num_chapters}  
**Público-alvo:** {form_data['audience']}  
**Nível:** {form_data['difficulty']}  
**Data:** {datetime.now().strftime('%d/%m/%Y')}

---

{introduction}

---

"""
    
    # Adicionar capítulos
    for chapter in chapters:
        full_ebook += f"{chapter}\n\n---\n\n"
    
    # Adicionar conclusão
    full_ebook += f"{conclusion}\n\n"
    
    # Adicionar recursos extras se solicitado
    if config.get('include_exercises') or config.get('include_images'):
        extras_prompt = f"""Crie recursos complementares para "{topic}":

1. Glossário com 10 termos importantes
2. Lista de recursos adicionais (livros, sites, cursos)
{"3. Sugestões de imagens por capítulo" if config.get('include_images') else ""}
{"4. Exercícios práticos extras" if config.get('include_exercises') else ""}

Seja conciso e prático. Máximo 400 palavras."""
        
        try:
            st.info("📚 Adicionando recursos extras...")
            extras = llm.predict(extras_prompt, max_tokens=600)
            full_ebook += f"---\n\n# Recursos Adicionais\n\n{extras}\n\n"
            st.success("✅ Recursos adicionados!")
        except Exception as e:
            st.warning(f"Recursos extras não puderam ser gerados: {str(e)}")
    
    # Footer
    full_ebook += f"""---

## 📚 Sobre Este Ebook

Este ebook foi gerado com inteligência artificial para fornecer conteúdo educativo sobre {topic}.

- **Palavras:** ~{len(full_ebook.split()):,}
- **Tempo de leitura:** ~{max(1, len(full_ebook.split()) // 200)} minutos
- **Formato:** {config['format']}
- **Versão:** 1.0

---

*Obrigado por ler! Esperamos que este conteúdo seja útil em sua jornada de aprendizado.*

© 2024 EBook Generator Pro - Powered by OpenAI
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
                <li>Inovação e Criatividade nos Negócios</li>
                <li>Liderança e Motivação de Times</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h4>🛠️ Tecnologia & Programação</h4>
            <ul>
                <li>Python para Iniciantes Completos</li>
                <li>Desenvolvimento Web com React</li>
                <li>Inteligência Artificial Prática</li>
                <li>Segurança Digital e Privacidade</li>
                <li>Blockchain e Criptomoedas</li>
                <li>Data Science para Negócios</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>💡 Desenvolvimento Pessoal</h4>
            <ul>
                <li>Gestão do Tempo e Produtividade</li>
                <li>Comunicação Eficaz e Assertiva</li>
                <li>Liderança Pessoal e Profissional</li>
                <li>Hábitos Saudáveis e Mindfulness</li>
                <li>Inteligência Emocional Aplicada</li>
                <li>Planejamento de Carreira</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h4>🎓 Educação & Conhecimento</h4>
            <ul>
                <li>História do Brasil Contemporâneo</li>
                <li>Matemática Básica e Aplicada</li>
                <li>Ciências Naturais Explicadas</li>
                <li>Literatura Brasileira Moderna</li>
                <li>Filosofia para o Dia a Dia</li>
                <li>Geografia e Meio Ambiente</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def create_tips_section():
    """Cria seção com dicas"""
    st.markdown("""
    <div class="glass-card fade-in">
        <h3 style="color: #667eea; margin-bottom: 20px;">🎯 Dicas para Melhores Resultados</h3>
    </div>
    """, unsafe_allow_html=True)
    
    tips = [
        ("🎯", "Seja Específico", "Temas focados geram conteúdo mais útil e direcionado"),
        ("👥", "Defina o Público", "Conhecer o leitor melhora drasticamente a abordagem"),
        ("📊", "Escolha o Nível", "Ajuste entre iniciante, intermediário ou avançado"),
        ("💼", "Use Exemplos", "Solicite casos práticos e situações reais"),
        ("🔄", "Teste Configurações", "Experimente diferentes estilos e formatos"),
        ("📱", "Pense na Aplicação", "Considere como o leitor usará o conteúdo")
    ]
    
    for icon, title, description in tips:
        st.markdown(f"""
        <div class="feature-card">
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <span style="font-size: 1.5em; margin-right: 15px;">{icon}</span>
                <strong style="color: #667eea;">{title}</strong>
            </div>
            <p style="margin: 0; color: #8b92a5; line-height: 1.4;">{description}</p>
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
            # Preparar arquivo para download baseado no formato selecionado
            try:
                filename = f"ebook_{form_data['topic'][:30].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}"
                format_lower = config["format"].split()[1].lower()
                
                # PDF
                if format_lower == "pdf":
                    st.info("🔄 Gerando PDF...")
                    pdf_data = create_pdf_content(ebook_content, form_data['topic'])
                    
                    if pdf_data:
                        st.download_button(
                            label="📥 Baixar Ebook (PDF)",
                            data=pdf_data,
                            file_name=f"{filename}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                        st.success("✅ PDF pronto para download!")
                    else:
                        st.error("❌ Erro ao gerar PDF. Oferecendo download alternativo...")
                        # Fallback para texto
                        st.download_button(
                            label="📝 Baixar como Texto (Fallback)",
                            data=ebook_content.encode('utf-8'),
                            file_name=f"{filename}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                
                # Markdown
                elif format_lower == "markdown":
                    file_data = ebook_content.encode('utf-8')
                    st.download_button(
                        label="📥 Baixar Ebook (Markdown)",
                        data=file_data,
                        file_name=f"{filename}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                    st.success("✅ Markdown pronto para download!")
                
                # HTML
                elif format_lower == "html":
                    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{form_data['topic']}</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', 'Arial', sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f8f9fa;
            color: #333;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{ 
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            text-align: center;
        }}
        h2 {{ 
            color: #764ba2;
            border-bottom: 1px solid #ddd;
            padding-bottom: 5px;
            margin-top: 30px;
        }}
        h3 {{ 
            color: #667eea;
            margin-top: 25px;
        }}
        .highlight {{ 
            background: #f0f8ff;
            padding: 15px;
            border-left: 4px solid #667eea;
            margin: 20px 0;
            border-radius: 5px;
        }}
        code {{ 
            background: #f4f4f4;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        blockquote {{ 
            background: #f9f9f9;
            border-left: 4px solid #ddd;
            margin: 0;
            padding: 10px 20px;
            font-style: italic;
        }}
        .info-box {{
            background: linear-gradient(135deg, #667eea15, #764ba215);
            border: 1px solid #667eea40;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
        }}
        hr {{
            border: none;
            height: 2px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            margin: 30px 0;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        {markdown.markdown(ebook_content)}
        <div class="footer">
            <p>Gerado por EBook Generator Pro - {datetime.now().strftime('%d/%m/%Y às %H:%M')}</p>
        </div>
    </div>
</body>
</html>"""
                    
                    file_data = html_content.encode('utf-8')
                    st.download_button(
                        label="📥 Baixar Ebook (HTML)",
                        data=file_data,
                        file_name=f"{filename}.html",
                        mime="text/html",
                        use_container_width=True
                    )
                    st.success("✅ HTML pronto para download!")
                
                # EPUB (simplificado como ZIP com HTML)
                elif format_lower == "epub":
                    # Para EPUB real, seria necessária uma biblioteca específica
                    # Por enquanto, oferecemos HTML como alternativa
                    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>{form_data['topic']}</title>
    <style>
        body {{ font-family: serif; line-height: 1.6; margin: 0; padding: 20px; }}
        h1, h2, h3 {{ color: #333; }}
        h1 {{ text-align: center; border-bottom: 2px solid #333; }}
    </style>
</head>
<body>
    {markdown.markdown(ebook_content)}
</body>
</html>"""
                    
                    file_data = html_content.encode('utf-8')
                    st.download_button(
                        label="📥 Baixar Ebook (HTML - compatível com leitores)",
                        data=file_data,
                        file_name=f"{filename}_ebook.html",
                        mime="text/html",
                        use_container_width=True
                    )
                    st.info("📖 Formato EPUB simulado como HTML otimizado para leitura")
                
                else:
                    # Fallback para texto
                    file_data = ebook_content.encode('utf-8')
                    st.download_button(
                        label="📝 Baixar Ebook (Texto)",
                        data=file_data,
                        file_name=f"{filename}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                    st.success("✅ Texto pronto para download!")
                
            except Exception as e:
                st.error(f"❌ Erro ao preparar download: {str(e)}")
                
                # Fallback: oferecer download direto do texto
                st.download_button(
                    label="📝 Baixar como Texto (Emergência)",
                    data=ebook_content.encode('utf-8'),
                    file_name=f"ebook_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        with col2:
            st.info(f"""
            **📋 Formato Selecionado:**
            
            • **{config['format']}**: Escolhido nas configurações
            
            📊 **Características:**
            ✅ Estrutura profissional
            ✅ Conteúdo otimizado
            ✅ Formatação adequada
            ✅ Pronto para uso
            
            💡 **Dica:**
            PDFs são ideais para impressão e leitura offline.
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
            "📚 Capítulos": config["num_chapters"],
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
                        <h3 style="color: #667eea; text-align: center;">🚀 Gerando seu Ebook...</h3>
                        <p style="text-align: center; color: #8b92a5;">Otimizado para qualidade e velocidade</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Configurar LLM com parâmetros otimizados
                    try:
                        llm = OpenAI(
                            openai_api_key=config["api_key"],
                            temperature=0.7,
                            max_tokens=2000,  # Reduzido para evitar erros de token
                            request_timeout=120,  # 2 minutos de timeout
                            model_name="gpt-3.5-turbo-instruct"  # Modelo mais estável
                        )
                        st.success("✅ Sistema de IA configurado!")
                    except Exception as e:
                        st.error(f"❌ Erro na configuração da API OpenAI: {str(e)}")
                        
                        # Mostrar ajuda específica para erros comuns
                        if "api_key" in str(e).lower():
                            st.error("🔑 Erro na API Key - Verifique se ela está correta")
                        elif "quota" in str(e).lower():
                            st.error("💳 Cota excedida - Verifique seu saldo na OpenAI")
                        elif "rate" in str(e).lower():
                            st.error("⏱️ Muitas requisições - Tente novamente em alguns minutos")
                        
                        st.stop()
                    
                    # Gerar ebook usando o sistema otimizado
                    try:
                        ebook_content = generate_optimized_ebook(
                            llm=llm,
                            topic=form_data["topic"],
                            config=config,
                            form_data=form_data
                        )
                        
                        # Verificar se o conteúdo foi gerado com sucesso
                        if not ebook_content or len(ebook_content.strip()) < 500:
                            st.error("❌ Conteúdo gerado é muito curto ou vazio")
                            st.error("📝 Tente novamente com um tópico mais específico")
                            st.stop()
                        
                        # Mostrar estatísticas finais
                        final_word_count = len(ebook_content.split())
                        st.success(f"🎉 Ebook gerado com sucesso! ({final_word_count:,} palavras)")
                        
                    except Exception as e:
                        st.error(f"❌ Erro durante a geração do ebook: {str(e)}")
                        
                        # Ajuda específica para diferentes tipos de erro
                        error_str = str(e).lower()
                        if "context length" in error_str or "token" in error_str:
                            st.error("🔄 Erro de tokens - O conteúdo solicitado é muito longo")
                            st.error("💡 Sugestão: Reduza o número de páginas ou capítulos")
                        elif "rate limit" in error_str:
                            st.error("⏱️ Limite de taxa atingido - Aguarde alguns minutos")
                        elif "timeout" in error_str:
                            st.error("⏱️ Timeout - A geração demorou muito")
                            st.error("💡 Sugestão: Tente novamente com menos páginas")
                        
                        # Mostrar detalhes do erro em modo debug
                        with st.expander("🔍 Detalhes do Erro (Debug)", expanded=False):
                            st.code(traceback.format_exc())
                        
                        st.error("🔄 Sugestões gerais:")
                        st.error("• Reduza o número de páginas (tente 10-30)")
                        st.error("• Diminua o número de capítulos")
                        st.error("• Simplifique a descrição do tópico")
                        st.error("• Verifique sua conexão com a internet")
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
                    <h4 style="color: #ef4444;">🔧 Soluções Recomendadas:</h4>
                    <ul>
                        <li><strong>Reiniciar:</strong> Recarregue a página (F5)</li>
                        <li><strong>API Key:</strong> Verifique se sua chave OpenAI está válida</li>
                        <li><strong>Internet:</strong> Teste sua conexão</li>
                        <li><strong>Configurações:</strong> Use configurações mais simples</li>
                        <li><strong>Tópico:</strong> Seja mais específico e claro</li>
                        <li><strong>Tamanho:</strong> Comece com ebooks menores (10-20 páginas)</li>
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
                <h4>✨ Geração com PDF Real</h4>
                <p style="color: #8b92a5;">Sistema agora gera PDFs profissionais com formatação adequada para impressão e leitura.</p>
            </div>
            <div class="feature-card">
                <h4>📋 Estrutura Profissional</h4>
                <p style="color: #8b92a5;">Introdução, capítulos bem organizados, conclusão e recursos extras com design aprimorado.</p>
            </div>
            <div class="feature-card">
                <h4>🖼️ Sugestões Visuais</h4>
                <p style="color: #8b92a5;">Descrições de imagens e elementos visuais para enriquecer o conteúdo do ebook.</p>
            </div>
            <div class="feature-card">
                <h4>📚 Exercícios Práticos</h4>
                <p style="color: #8b92a5;">Atividades interativas e reflexões para aumentar o engajamento dos leitores.</p>
            </div>
            <div class="feature-card">
                <h4>📄 Múltiplos Formatos</h4>
                <p style="color: #8b92a5;">Download em PDF, Markdown, HTML e EPUB para máxima compatibilidade.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Seção de melhorias
        st.markdown("""
        <div class="glass-card fade-in">
            <h3 style="color: #667eea; margin-bottom: 20px;">⚡ Melhorias v2.2</h3>
            <div class="feature-card">
                <h4>📄 PDF Profissional</h4>
                <p style="color: #8b92a5;">Agora com geração real de PDF usando ReportLab, com formatação profissional e layout otimizado.</p>
            </div>
            <div class="feature-card">
                <h4>🎨 Interface Melhorada</h4>
                <p style="color: #8b92a5;">Containers de exemplos redesenhados com melhor espaçamento e legibilidade.</p>
            </div>
            <div class="feature-card">
                <h4>🚀 Performance Otimizada</h4>
                <p style="color: #8b92a5;">Sistema mais rápido e estável, com recuperação automática de erros e timeouts.</p>
            </div>
            <div class="feature-card">
                <h4>💡 Downloads Inteligentes</h4>
                <p style="color: #8b92a5;">Sistema adapta o formato de download baseado na seleção do usuário com fallbacks.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Status do sistema
        st.markdown("""
        <div class="glass-card fade-in">
            <h3 style="color: #667eea; margin-bottom: 20px;">📊 Status do Sistema</h3>
            <div style="text-align: center;">
                <div style="color: #10b981; font-size: 1.2em; margin: 10px 0;">
                    ✅ Sistema Operacional
                </div>
                <div style="color: #8b92a5; font-size: 0.9em; margin: 10px 0;">
                    Última atualização: 30/07/2024
                </div>
                <div style="color: #8b92a5; font-size: 0.8em; margin: 10px 0;">
                    Versão: 2.2 - PDF + Interface Melhorada
                </div>
                <div style="color: #667eea; font-size: 0.8em; margin: 10px 0;">
                    🔥 Novidades: PDF real + Containers otimizados
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 20px 0; color: #8b92a5;">
        <p>📚 <strong>EBook Generator Pro</strong> - Powered by OpenAI + ReportLab</p>
        <p style="font-size: 0.8em;">Versão 2.2 - PDF Profissional | © 2024 | Feito com ❤️ para criadores</p>
        <p style="font-size: 0.7em;">🔧 Agora com PDF real e interface otimizada!</p>
        <p style="font-size: 0.6em; margin-top: 10px;">
            💡 Dica: Experimente diferentes formatos - PDF para impressão, HTML para web
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()