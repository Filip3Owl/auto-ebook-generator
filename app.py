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

# Importações locais (comentadas para evitar erros se não existirem)
# from core.prompts import EBOOK_PROMPTS
# from agents.outline import create_outline_chain
# from agents.writer import create_writing_chain
# from utils.file_io import save_ebook
# from utils.config import load_config

# Configuração inicial
# load_config()

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
                index=1,  # Padrão para Markdown
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
            "num_chapters": num_chapters,
            "language": language,
            "formats": output_format
        }

def create_main_form():
    """Formulário principal simplificado"""
    with st.form("ebook_form"):
        ebook_topic = st.text_area(
            "",
            placeholder="📝 Exemplo:\n• Introdução ao Marketing Digital\n• Python para Iniciantes\n• Gestão de Tempo e Produtividade\n• História do Brasil Colonial",
            height=120,
            help="Seja específico sobre o tema principal"
        )
        
        with st.expander("Opções Avançadas"):
            target_audience = st.text_input(
                "Público-alvo",
                value="Adultos interessados no tema"
            )
            
            col1, col2 = st.columns(2)
            with col1:
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
        
        submit_button = st.form_submit_button("Gerar Ebook")
    
    return {
        "topic": ebook_topic,
        "audience": target_audience,
        "difficulty": difficulty_level,
        "tone": tone,
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
                            body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; background: #f8f9fa; }}
                            h1, h2, h3 {{ color: #333; }}
                            h1 {{ border-bottom: 3px solid #667eea; padding-bottom: 10px; }}
                            h2 {{ border-bottom: 1px solid #ddd; padding-bottom: 5px; color: #667eea; }}
                            h3 {{ color: #764ba2; }}
                            .highlight {{ background: #f0f8ff; padding: 15px; border-left: 4px solid #667eea; margin: 20px 0; }}
                            code {{ background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }}
                            blockquote {{ background: #f9f9f9; border-left: 4px solid #ddd; margin: 0; padding: 10px 20px; }}
                            .content {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                        </style>
                    </head>
                    <body>
                        <div class="content">
                            {ebook_content.replace('# ', '<h1>').replace('## ', '<h2>').replace('### ', '<h3>').replace('\n', '<br>')}
                        </div>
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
                    file_name=f"{filename}.{file_extension.replace('pdf', 'txt')}",  # PDF não suportado, usar TXT
                    mime=mime_type,
                    use_container_width=True
                )
                
                st.success(f"✅ Pronto para download!")
                
            except Exception as e:
                st.error(f"❌ Erro ao preparar download: {str(e)}")
                
                # Fallback: oferecer download direto do texto
                st.download_button(
                    label="Download Markdown",
                    data=ebook_content.encode('utf-8'),
                    file_name=f"{filename}.md",
                    mime="text/markdown"
                )
        
        with col2:
            st.info("""
            **📋 Formatos Disponíveis:**
            
            • **Markdown**: Editável e flexível
            • **HTML**: Para web e navegadores
            • **Texto**: Simples e universal
            
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
                <h4>🖼️ Sugestões Visuais</h4>
                <p style="color: #8b92a5;">Descrições de imagens e elementos visuais para enriquecer o conteúdo.</p>
            </div>
            <div class="feature-card">
                <h4>📚 Exercícios Práticos</h4>
                <p style="color: #8b92a5;">Atividades e reflexões para aumentar o engajamento dos leitores.</p>
            </div>
            <div class="feature-card">
                <h4>📄 Múltiplos Formatos</h4>
                <p style="color: #8b92a5;">Download em Markdown, HTML e texto para máxima compatibilidade.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Seção de melhorias
        st.markdown("""
        <div class="glass-card fade-in">
            <h3 style="color: #667eea; margin-bottom: 20px;">⚡ Melhorias v2.1</h3>
            <div class="feature-card">
                <h4>🔧 Correção de Tokens</h4>
                <p style="color: #8b92a5;">Sistema completamente reescrito para evitar erros de limite de tokens.</p>
            </div>
            <div class="feature-card">
                <h4>📊 Controle Inteligente</h4>
                <p style="color: #8b92a5;">Geração por partes com controle automático de tamanho e qualidade.</p>
            </div>
            <div class="feature-card">
                <h4>🚀 Performance</h4>
                <p style="color: #8b92a5;">Mais rápido e estável, com recuperação automática de erros.</p>
            </div>
            <div class="feature-card">
                <h4>💡 Feedback Melhorado</h4>
                <p style="color: #8b92a5;">Mensagens de erro mais claras com sugestões práticas de solução.</p>
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
                    Versão: 2.1 - Otimizada para tokens
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 20px 0; color: #8b92a5;">
        <p>📚 <strong>EBook Generator Pro</strong> - Powered by OpenAI</p>
        <p style="font-size: 0.8em;">Versão 2.1 - Otimizada | © 2024 | Feito com ❤️ para criadores</p>
        <p style="font-size: 0.7em;">🔧 Agora com correção completa de erros de token!</p>
        <p style="font-size: 0.6em; margin-top: 10px;">
            💡 Dica: Comece com ebooks de 10-30 páginas para melhores resultados
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()