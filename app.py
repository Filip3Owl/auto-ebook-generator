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
import zipfile
import io

# Configura paths para imports
sys.path.append(str(Path(__file__).parent))

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
            
            # Tamanho do ebook
            ebook_pages = st.slider(
                "📄 Número de Páginas",
                min_value=10,
                max_value=100,
                value=30,
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
            estimated_words = ebook_pages * 300
            st.info(f"📊 Estimativa: ~{estimated_words:,} palavras em {num_chapters} capítulos")
            
            # Idioma
            language = st.selectbox(
                "🌍 Idioma",
                ["🇧🇷 Português", "🇺🇸 Inglês", "🇪🇸 Espanhol", "🇫🇷 Francês"],
                index=0
            )
        
        # Opções de formato - APENAS EPUB E MARKDOWN
        with st.expander("💾 Formato de Saída"):
            output_format = st.radio(
                "Escolha o formato:",
                ["📚 EPUB", "📝 Markdown"],
                index=1,  # Padrão para Markdown
                horizontal=False,
                help="EPUB para leitores de ebooks, Markdown para edição"
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

def generate_epub_structure(ebook_content, title, author="EBook Generator Pro"):
    """
    Gera a estrutura EPUB básica
    """
    # Dividir o conteúdo em capítulos
    chapters = []
    current_chapter = ""
    chapter_title = ""
    
    lines = ebook_content.split('\n')
    for line in lines:
        if line.startswith('# ') and 'Capítulo' in line:
            if current_chapter:
                chapters.append({
                    'title': chapter_title,
                    'content': current_chapter
                })
            chapter_title = line.replace('# ', '').strip()
            current_chapter = line + '\n'
        else:
            current_chapter += line + '\n'
    
    # Adicionar último capítulo
    if current_chapter:
        chapters.append({
            'title': chapter_title,
            'content': current_chapter
        })
    
    # Se não houver capítulos identificados, criar um único capítulo
    if not chapters:
        chapters.append({
            'title': title,
            'content': ebook_content
        })
    
    # Criar estrutura EPUB simplificada
    epub_files = {}
    
    # META-INF/container.xml
    epub_files['META-INF/container.xml'] = '''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
    </rootfiles>
</container>'''
    
    # mimetype
    epub_files['mimetype'] = 'application/epub+zip'
    
    # OEBPS/content.opf
    manifest_items = []
    spine_items = []
    
    for i, chapter in enumerate(chapters):
        chapter_id = f"chapter{i+1}"
        manifest_items.append(f'<item id="{chapter_id}" href="{chapter_id}.xhtml" media-type="application/xhtml+xml"/>')
        spine_items.append(f'<itemref idref="{chapter_id}"/>')
    
    content_opf = f'''<?xml version="1.0" encoding="UTF-8"?>
<package version="3.0" xmlns="http://www.idpf.org/2007/opf" unique-identifier="uid">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
        <dc:identifier id="uid">{title.replace(' ', '_').lower()}</dc:identifier>
        <dc:title>{title}</dc:title>
        <dc:creator>{author}</dc:creator>
        <dc:language>pt-BR</dc:language>
        <dc:date>{datetime.now().strftime('%Y-%m-%d')}</dc:date>
        <meta property="dcterms:modified">{datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}</meta>
    </metadata>
    <manifest>
        <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
        <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
        {''.join(manifest_items)}
    </manifest>
    <spine toc="ncx">
        {''.join(spine_items)}
    </spine>
</package>'''
    
    epub_files['OEBPS/content.opf'] = content_opf
    
    # OEBPS/toc.ncx
    nav_points = []
    for i, chapter in enumerate(chapters):
        nav_points.append(f'''
        <navPoint id="navpoint-{i+1}" playOrder="{i+1}">
            <navLabel><text>{chapter['title']}</text></navLabel>
            <content src="chapter{i+1}.xhtml"/>
        </navPoint>''')
    
    toc_ncx = f'''<?xml version="1.0" encoding="UTF-8"?>
<ncx version="2005-1" xmlns="http://www.daisy.org/z3986/2005/ncx/">
    <head>
        <meta name="dtb:uid" content="{title.replace(' ', '_').lower()}"/>
        <meta name="dtb:depth" content="1"/>
        <meta name="dtb:totalPageCount" content="0"/>
        <meta name="dtb:maxPageNumber" content="0"/>
    </head>
    <docTitle><text>{title}</text></docTitle>
    <navMap>{''.join(nav_points)}
    </navMap>
</ncx>'''
    
    epub_files['OEBPS/toc.ncx'] = toc_ncx
    
    # OEBPS/nav.xhtml
    nav_list = []
    for i, chapter in enumerate(chapters):
        nav_list.append(f'<li><a href="chapter{i+1}.xhtml">{chapter["title"]}</a></li>')
    
    nav_xhtml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
    <title>Índice</title>
</head>
<body>
    <nav epub:type="toc">
        <h1>Índice</h1>
        <ol>{''.join(nav_list)}</ol>
    </nav>
</body>
</html>'''
    
    epub_files['OEBPS/nav.xhtml'] = nav_xhtml
    
    # Capítulos XHTML
    for i, chapter in enumerate(chapters):
        # Converter Markdown para HTML básico
        content_html = chapter['content']
        content_html = content_html.replace('# ', '<h1>').replace('\n# ', '</h1>\n<h1>')
        content_html = content_html.replace('## ', '<h2>').replace('\n## ', '</h2>\n<h2>')
        content_html = content_html.replace('### ', '<h3>').replace('\n### ', '</h3>\n<h3>')
        content_html = content_html.replace('\n\n', '</p>\n<p>')
        content_html = f'<p>{content_html}</p>'
        content_html = content_html.replace('<p><h', '<h').replace('</h1></p>', '</h1>')
        content_html = content_html.replace('</h2></p>', '</h2>').replace('</h3></p>', '</h3>')
        content_html = content_html.replace('<p></p>', '')
        
        chapter_xhtml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>{chapter['title']}</title>
    <style>
        body {{ font-family: serif; line-height: 1.6; margin: 2em; }}
        h1, h2, h3 {{ color: #333; margin-top: 2em; }}
        h1 {{ border-bottom: 2px solid #667eea; padding-bottom: 0.5em; }}
        p {{ text-align: justify; margin: 1em 0; }}
    </style>
</head>
<body>
    {content_html}
</body>
</html>'''
        
        epub_files[f'OEBPS/chapter{i+1}.xhtml'] = chapter_xhtml
    
    return epub_files

def create_epub_file(epub_files):
    """
    Cria o arquivo EPUB como um zip em memória
    """
    epub_buffer = io.BytesIO()
    
    with zipfile.ZipFile(epub_buffer, 'w', zipfile.ZIP_DEFLATED) as epub_zip:
        # Adicionar mimetype primeiro (sem compressão)
        epub_zip.writestr('mimetype', epub_files['mimetype'], compress_type=zipfile.ZIP_STORED)
        
        # Adicionar outros arquivos
        for filepath, content in epub_files.items():
            if filepath != 'mimetype':
                epub_zip.writestr(filepath, content)
    
    epub_buffer.seek(0)
    return epub_buffer.getvalue()

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
                <li>Planejamento Financeiro</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h4>🛠️ Tecnologia</h4>
            <ul>
                <li>Python para Iniciantes</li>
                <li>Desenvolvimento Web Básico</li>
                <li>Inteligência Artificial Prática</li>
                <li>Segurança Digital</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>💡 Desenvolvimento Pessoal</h4>
            <ul>
                <li>Gestão do Tempo</li>
                <li>Comunicação Eficaz</li>
                <li>Liderança Pessoal</li>
                <li>Hábitos Saudáveis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h4>🎓 Educação</h4>
            <ul>
                <li>História do Brasil</li>
                <li>Matemática Básica</li>
                <li>Ciências Naturais</li>
                <li>Literatura Brasileira</li>
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
        ("🎯", "Seja Específico", "Temas focados geram conteúdo mais útil"),
        ("👥", "Defina o Público", "Conhecer o leitor melhora a abordagem"),
        ("📊", "Escolha o Nível", "Iniciante, intermediário ou avançado"),
        ("💼", "Use Exemplos", "Solicite casos práticos e reais"),
        ("🔄", "Teste Configurações", "Experimente diferentes estilos"),
        ("📱", "Pense na Aplicação", "Como o leitor usará o conteúdo")
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
                filename = f"ebook_{form_data['topic'][:30].replace(' ', '_').replace('/', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}"
                
                # Download baseado no formato selecionado
                if config["format"] == "📚 EPUB":
                    # Gerar EPUB
                    st.info("📚 Gerando arquivo EPUB...")
                    epub_files = generate_epub_structure(ebook_content, form_data['topic'])
                    epub_data = create_epub_file(epub_files)
                    
                    st.download_button(
                        label="📚 Baixar Ebook (EPUB)",
                        data=epub_data,
                        file_name=f"{filename}.epub",
                        mime="application/epub+zip",
                        use_container_width=True
                    )
                    st.success("✅ Arquivo EPUB pronto para download!")
                    
                else:  # Markdown
                    # Gerar Markdown
                    st.download_button(
                        label="📝 Baixar Ebook (Markdown)",
                        data=ebook_content.encode('utf-8'),
                        file_name=f"{filename}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                    st.success("✅ Arquivo Markdown pronto para download!")
                
            except Exception as e:
                st.error(f"❌ Erro ao preparar download: {str(e)}")
                
                # Fallback: oferecer download direto do texto
                st.download_button(
                    label="📝 Baixar como Texto (Fallback)",
                    data=ebook_content.encode('utf-8'),
                    file_name=f"{filename}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        with col2:
            st.info(f"""
            **📋 Formato Selecionado:**
            
            • **{config['format']}**
            
            {"**📚 EPUB:**" if "EPUB" in config['format'] else "**📝 Markdown:**"}
            {"✅ Compatível com leitores de ebook" if "EPUB" in config['format'] else "✅ Editável e flexível"}
            {"✅ Estrutura de capítulos" if "EPUB" in config['format'] else "✅ Formatação universal"}
            {"✅ Metadados inclusos" if "EPUB" in config['format'] else "✅ Suporte completo"}
            {"✅ Índice navegável" if "EPUB" in config['format'] else "✅ Fácil conversão"}
            
            📊 **Qualidade:**
            ✅ Estrutura profissional
            ✅ Conteúdo otimizado
            ✅ Formatação adequada
            ✅ Pronto para uso
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
                <h4>✨ Geração Otimizada</h4>
                <p style="color: #8b92a5;">Sistema aprimorado que evita erros de token e gera conteúdo de qualidade.</p>
            </div>
            <div class="feature-card">
                <h4>📋 Estrutura Profissional</h4>
                <p style="color: #8b92a5;">Introdução, capítulos bem organizados, conclusão e recursos extras.</p>
            </div>
            <div class="feature-card">
                <h4>📚 Formato EPUB</h4>
                <p style="color: #8b92a5;">Ebooks compatíveis com Kindle, Apple Books e outros leitores.</p>
            </div>
            <div class="feature-card">
                <h4>📝 Formato Markdown</h4>
                <p style="color: #8b92a5;">Fácil edição e conversão para outros formatos.</p>
            </div>
            <div class="feature-card">
                <h4>🖼️ Sugestões Visuais</h4>
                <p style="color: #8b92a5;">Descrições de imagens e elementos visuais para enriquecer o conteúdo.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Seção de melhorias
        st.markdown("""
        <div class="glass-card fade-in">
            <h3 style="color: #667eea; margin-bottom: 20px;">⚡ Melhorias v3.0</h3>
            <div class="feature-card">
                <h4>📚 Suporte EPUB Nativo</h4>
                <p style="color: #8b92a5;">Geração de arquivos EPUB profissionais com estrutura completa.</p>
            </div>
            <div class="feature-card">
                <h4>📝 Markdown Otimizado</h4>
                <p style="color: #8b92a5;">Formatação perfeita para conversão e edição posterior.</p>
            </div>
            <div class="feature-card">
                <h4>🔧 Dois Formatos Premium</h4>
                <p style="color: #8b92a5;">Foco nos formatos mais utilizados e versáteis do mercado.</p>
            </div>
            <div class="feature-card">
                <h4>💡 Interface Simplificada</h4>
                <p style="color: #8b92a5;">Menos opções, mais qualidade e facilidade de uso.</p>
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
                    Última atualização: 31/07/2024
                </div>
                <div style="color: #8b92a5; font-size: 0.8em; margin: 10px 0;">
                    Versão: 3.0 - EPUB + Markdown
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 20px 0; color: #8b92a5;">
        <p>📚 <strong>EBook Generator Pro</strong> - Powered by OpenAI</p>
        <p style="font-size: 0.8em;">Versão 3.0 - EPUB & Markdown | © 2024 | Feito com ❤️ para criadores</p>
        <p style="font-size: 0.7em;">📚 Agora com suporte nativo para EPUB profissional!</p>
        <p style="font-size: 0.6em; margin-top: 10px;">
            💡 Dica: Use EPUB para leitores digitais e Markdown para edição
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()