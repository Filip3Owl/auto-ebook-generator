"""
Módulo avançado com templates de prompts para geração completa de ebooks
Inclui todas as seções estruturais de um livro profissional
"""

# Prompts para elementos pré-textuais
COVER_PROMPT = """
Você é um designer editorial experiente. Crie uma descrição detalhada para a capa de um ebook sobre: {topic}

Especificações:
- Título: Crie um título cativante e profissional
- Subtítulo: Se necessário, adicione um subtítulo explicativo
- Autor: {author_name}
- Estilo visual: Descreva cores, tipografia e elementos gráficos apropriados para {style}
- Público-alvo: {target_audience}

Retorne:
1. Título principal
2. Subtítulo (se aplicável)
3. Descrição visual da capa
4. Justificativa das escolhas de design
"""

TITLE_PAGE_PROMPT = """
Crie a folha de rosto completa para um ebook com as seguintes informações:

Título: {title}
Autor: {author_name}
Editora: {publisher}
Ano: {year}
Cidade: {city}

Formate de maneira profissional e elegante.
"""

COPYRIGHT_PAGE_PROMPT = """
Crie uma página de direitos autorais completa e profissional para:

Título: {title}
Autor: {author_name}
Editora: {publisher}
Ano: {year}
ISBN: {isbn}
Edição: {edition}

Inclua:
- Informações de copyright
- Dados de catalogação
- Créditos técnicos
- Avisos legais apropriados
- Contato da editora
"""

DEDICATION_PROMPT = """
Escreva uma dedicatória tocante e apropriada para um ebook sobre {topic}.
Estilo: {style}
Tom: Pessoal mas profissional
Extensão: 1-3 frases elegantes

A dedicatória deve refletir o espírito da obra e conectar emocionalmente com o leitor.
"""

ACKNOWLEDGMENTS_PROMPT = """
Redija uma seção de agradecimentos profissional para um ebook sobre {topic}.

Inclua agradecimentos a:
- Pessoas que contribuíram com conhecimento
- Fontes de inspiração
- Apoio técnico e editorial
- Família e amigos (de forma equilibrada)

Tom: Profissional, sincero e conciso
Extensão: 2-4 parágrafos
"""

EPIGRAPH_PROMPT = """
Selecione e apresente uma epígrafe impactante para um ebook sobre {topic}.

Requisitos:
- Citação relevante ao tema central
- Autor da citação claramente identificado
- Conexão clara com o conteúdo da obra
- Tom adequado ao estilo {style}

Se não encontrar citação adequada, crie uma frase original marcante.
"""

# Prompts para estrutura principal
ENHANCED_OUTLINE_PROMPT = """
Você é um escritor bestseller e consultor editorial. Crie um esboço COMPLETO e detalhado para um ebook sobre: {topic}

ESPECIFICAÇÕES TÉCNICAS:
- Estilo: {style}
- Tamanho: {length} páginas
- público-alvo: {target_audience}
- Nível de profundidade: {depth_level}
- Objetivo principal: {main_objective}

ENTREGUE UM ESBOÇO ESTRUTURADO COM:

1. TÍTULO PRINCIPAL (cativante e SEO-friendly)
2. SUBTÍTULO (se necessário)

3. ESTRUTURA PRÉ-TEXTUAL:
   - Dedicatória (sugestão de tema)
   - Agradecimentos (principais categorias)
   - Epígrafe (tema sugerido)

4. INTRODUÇÃO/PREFÁCIO:
   - Hook inicial
   - Contextualização do tema
   - Objetivos da obra
   - Como usar o livro
   - Promessa de valor

5. SUMÁRIO DETALHADO:
   Para cada capítulo, inclua:
   - Título do capítulo
   - Objetivo específico
   - 4-6 subseções principais
   - Pontos-chave a abordar
   - Exemplos/casos práticos sugeridos
   - Exercícios ou reflexões (se aplicável)

6. CONCLUSÃO/EPÍLOGO:
   - Síntese dos pontos principais
   - Chamada para ação
   - Próximos passos para o leitor

7. ELEMENTOS PÓS-TEXTUAIS:
   - Apêndices necessários
   - Recursos adicionais
   - Bibliografia sugerida
   - Sobre o autor

CRITÉRIOS DE QUALIDADE:
- Fluxo lógico entre capítulos
- Progressão didática do conteúdo
- Balance entre teoria e prática
- Adequação ao público-alvo
- Potencial de engajamento

Retorne em formato Markdown bem estruturado.
"""

ENHANCED_INTRODUCTION_PROMPT = """
Escreva uma introdução magistral para um ebook sobre {topic}.

CONTEXTO:
- Estilo: {style}
- Público: {target_audience}
- Objetivo: {main_objective}
- Tom: {tone}

ESTRUTURA DA INTRODUÇÃO (800-1200 palavras):

1. ABERTURA IMPACTANTE:
   - Hook que capture atenção imediata
   - Estatística surpreendente, história pessoal ou pergunta provocativa

2. CONTEXTUALIZAÇÃO:
   - Por que este tema é importante AGORA
   - Problemas/desafios que o leitor enfrenta
   - Oportunidades disponíveis

3. CREDIBILIDADE:
   - Sua autoridade no assunto (sem ser pretensioso)
   - Experiências relevantes
   - Resultados que você/outros obtiveram

4. PROMESSA DE VALOR:
   - O que exatamente o leitor aprenderá
   - Benefícios concretos e mensuráveis
   - Transformação prometida

5. ESTRUTURA DO LIVRO:
   - Visão geral dos capítulos
   - Como os conteúdos se conectam
   - Melhor forma de usar o material

6. CHAMADA PARA JORNADA:
   - Convide o leitor para a transformação
   - Crie expectativa para o conteúdo
   - Tom motivacional e confiante

REQUISITOS DE QUALIDADE:
- Linguagem clara e acessível
- Evite jargões desnecessários
- Inclua elementos emocionais
- Seja específico, não genérico
- Termine com gancho para o primeiro capítulo
"""

ENHANCED_CHAPTER_PROMPT = """
Escreva um capítulo completo e profissional intitulado '{chapter_title}' para um ebook sobre {topic}.

ESPECIFICAÇÕES:
- Estilo: {style}
- Extensão: {chapter_length} palavras
- Público: {target_audience}
- Posição: Capítulo {chapter_number} de {total_chapters}

ESTRUTURA OBRIGATÓRIA:

1. ABERTURA DO CAPÍTULO:
   - Introdução que conecta com capítulo anterior
   - Visão geral do que será abordado
   - Por que este capítulo é importante

2. DESENVOLVIMENTO (3-5 seções principais):
   - Conceitos fundamentais explicados claramente
   - Exemplos práticos e relevantes
   - Casos de estudo quando apropriado
   - Citações de autoridades no assunto
   - Dados e estatísticas atuais

3. ELEMENTOS PRÁTICOS:
   - Exercícios ou atividades
   - Checklists quando aplicável
   - Templates ou frameworks
   - Dicas e insights exclusivos

4. CONEXÕES:
   - Referências a outros capítulos
   - Como se integra ao tema geral
   - Preparação para próximo capítulo

5. FECHAMENTO:
   - Resumo dos pontos principais
   - Principais takeaways
   - Próximos passos sugeridos

REQUISITOS DE QUALIDADE:
- Informação atualizada e precisa
- Linguagem adequada ao público
- Fluxo narrativo envolvente
- Balance teoria/prática
- Formatting em Markdown
- Subseções bem definidas

ELEMENTOS OBRIGATÓRIOS:
- Pelo menos 2 exemplos práticos
- 1 caso de estudo ou história
- Box com dica especial
- Lista de ação ou reflexão
"""

ENHANCED_CONCLUSION_PROMPT = """
Escreva uma conclusão poderosa e memorável para um ebook sobre {topic}.

CONTEXTO:
- Estilo: {style}
- Jornada do leitor: {reader_journey}
- Objetivo principal alcançado: {main_objective}
- Próximos passos desejados: {next_steps}

ESTRUTURA DA CONCLUSÃO (600-900 palavras):

1. RECAPITULAÇÃO ESTRATÉGICA:
   - Relembrar a jornada percorrida
   - Principais aprendizados consolidados
   - Transformação prometida vs. entregue

2. SÍNTESE PODEROSA:
   - 3-5 pontos mais importantes
   - Como tudo se conecta
   - O grande insight central

3. INSPIRAÇÃO E MOTIVAÇÃO:
   - Reconhecer o progresso do leitor
   - Encorajar aplicação prática
   - Visão do futuro possível

4. CHAMADA PARA AÇÃO CLARA:
   - Próximos passos específicos
   - Como começar imediatamente
   - recursos para continuar aprendendo

5. FECHAMENTO MEMORÁVEL:
   - Mensagem final inspiradora
   - Conexão emocional
   - Convite para jornada contínua

REQUISITOS:
- Tom otimista mas realista
- Evitar repetições desnecessárias
- Incluir elementos de urgência saudável
- Conectar com abertura do livro
- Deixar leitor energizado e confiante
"""

APPENDIX_PROMPT = """
Crie um apêndice útil e bem estruturado para complementar o ebook sobre {topic}.

Tipo de apêndice: {appendix_type}
Conteúdo específico: {specific_content}

ESTRUTURA:
1. Título claro do apêndice
2. Breve explicação do propósito
3. Organização lógica do conteúdo
4. Formatação profissional

TIPOS POSSÍVEIS:
- Recursos e ferramentas
- Templates e checklists
- Estudos de caso adicionais
- Glossário de termos
- Bibliografia comentada
- Exercícios práticos
- Dados e estatísticas
"""

ABOUT_AUTHOR_PROMPT = """
Redija uma biografia profissional "Sobre o Autor" para {author_name}, escritor de um ebook sobre {topic}.

INFORMAÇÕES DO AUTOR:
- Experiência: {author_experience}
- Credenciais: {author_credentials}
- Conquistas: {author_achievements}
- Estilo pessoal: {author_style}

ESTRUTURA (150-250 palavras):
1. Apresentação profissional
2. Experiência relevante ao tema
3. Credenciais e conquistas
4. Outras obras (se houver)
5. Informação pessoal leve
6. Contato/redes sociais

Tom: Profissional mas acessível, confiável sem ser pretensioso.
"""

BIBLIOGRAPHY_PROMPT = """
Crie uma seção de referências bibliográficas para um ebook sobre {topic}.

ESPECIFICAÇÕES:
- Estilo de citação: {citation_style}
- Tipos de fonte: {source_types}
- Quantidade: {number_of_sources}

CATEGORIAS:
1. Livros fundamentais
2. Artigos acadêmicos
3. Estudos e pesquisas
4. Recursos online confiáveis
5. Especialistas e autoridades

FORMATO: 
- Ordenação alfabética
- Formatação consistente
- Links quando aplicável
- Comentários breves sobre relevância
"""

# Prompts especializados por tipo de conteúdo
TECHNICAL_BOOK_PROMPT = """
Para ebooks técnicos sobre {topic}, inclua elementos específicos:

ELEMENTOS TÉCNICOS:
- Diagramas e fluxogramas (descrições)
- Códigos e exemplos práticos
- Troubleshooting guides
- Best practices destacadas
- Warnings e alertas importantes
- Step-by-step tutorials
- Performance benchmarks
- Compatibility notes

ESTRUTURA TÉCNICA:
- Prerequisites claramente definidos
- Dificuldade progressiva
- Hands-on exercises
- Real-world applications
- Common pitfalls
- Advanced techniques
"""

BUSINESS_BOOK_PROMPT = """
Para ebooks de negócios sobre {topic}, enfatize:

ELEMENTOS DE NEGÓCIO:
- Case studies reais
- ROI e métricas
- Implementation roadmaps
- Risk assessment
- Market insights
- Competitive analysis
- Financial projections
- Success stories
- Failure lessons
- Industry trends

ABORDAGEM EXECUTIVA:
- Executive summaries
- Quick wins identificados
- Long-term strategies
- Team implementation
- Change management
- Measuring success
"""

SELF_HELP_PROMPT = """
Para ebooks de desenvolvimento pessoal sobre {topic}, inclua:

ELEMENTOS TRANSFORMACIONAIS:
- Self-assessment tools
- Reflection exercises
- Goal-setting frameworks
- Progress tracking methods
- Mindset shifts
- Habit formation
- Obstacle overcoming
- Success stories inspiradoras
- Daily practices
- Long-term vision

ABORDAGEM PESSOAL:
- Linguagem empática
- Exemplos relacionáveis
- Action steps claros
- Motivational elements
- Practical wisdom
- Emotional intelligence
"""

# Dicionário principal organizado
EBOOK_PROMPTS = {
    # Elementos pré-textuais
    "cover": COVER_PROMPT,
    "title_page": TITLE_PAGE_PROMPT,
    "copyright": COPYRIGHT_PAGE_PROMPT,
    "dedication": DEDICATION_PROMPT,
    "acknowledgments": ACKNOWLEDGMENTS_PROMPT,
    "epigraph": EPIGRAPH_PROMPT,
    
    # Estrutura principal
    "outline": ENHANCED_OUTLINE_PROMPT,
    "introduction": ENHANCED_INTRODUCTION_PROMPT,
    "chapter": ENHANCED_CHAPTER_PROMPT,
    "conclusion": ENHANCED_CONCLUSION_PROMPT,
    
    # Elementos pós-textuais
    "appendix": APPENDIX_PROMPT,
    "about_author": ABOUT_AUTHOR_PROMPT,
    "bibliography": BIBLIOGRAPHY_PROMPT,
    
    # Especializações por tipo
    "technical": TECHNICAL_BOOK_PROMPT,
    "business": BUSINESS_BOOK_PROMPT,
    "self_help": SELF_HELP_PROMPT,
}

# Parâmetros padrão para diferentes tipos de ebook
DEFAULT_PARAMETERS = {
    "technical": {
        "style": "Técnico e didático",
        "target_audience": "Profissionais e estudantes da área",
        "depth_level": "Intermediário a avançado",
        "tone": "Profissional e preciso",
        "chapter_length": "2000-3000",
    },
    
    "business": {
        "style": "Executivo e prático",
        "target_audience": "Empresários e gestores",
        "depth_level": "Estratégico com foco em resultados",
        "tone": "Assertivo e orientado para ação",
        "chapter_length": "1800-2500",
    },
    
    "self_help": {
        "style": "Inspiracional e prático",
        "target_audience": "Pessoas em busca de crescimento pessoal",
        "depth_level": "Acessível com profundidade emocional",
        "tone": "Empático e motivacional",
        "chapter_length": "1500-2200",
    },
    
    "educational": {
        "style": "Didático e claro",
        "target_audience": "Estudantes e educadores",
        "depth_level": "Progressivo e estruturado",
        "tone": "Educativo e encorajador",
        "chapter_length": "2200-2800",
    }
}

# Função helper para selecionar prompts baseados no tipo
def get_book_type_prompts(book_type: str) -> dict:
    """
    Retorna prompts específicos baseados no tipo de livro
    """
    base_prompts = EBOOK_PROMPTS.copy()
    
    if book_type in ["technical", "business", "self_help"]:
        base_prompts["specialized"] = EBOOK_PROMPTS[book_type]
    
    return base_prompts

# Função para gerar parâmetros contextuais
def generate_context_parameters(topic: str, book_type: str, **kwargs) -> dict:
    """
    Gera parâmetros contextuais baseados no tópico e tipo do livro
    """
    base_params = DEFAULT_PARAMETERS.get(book_type, DEFAULT_PARAMETERS["educational"])
    
    context_params = {
        "topic": topic,
        "book_type": book_type,
        **base_params,
        **kwargs
    }
    
    return context_params

# Exemplo de uso:
"""
# Para usar os prompts aprimorados:

context = generate_context_parameters(
    topic="Inteligência Artificial na Educação",
    book_type="technical",
    author_name="Dr. João Silva",
    length="200"
)

outline_prompt = EBOOK_PROMPTS["outline"].format(**context)
introduction_prompt = EBOOK_PROMPTS["introduction"].format(**context)
"""