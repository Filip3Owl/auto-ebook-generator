"""
Módulo com templates de prompts otimizados para geração de ebooks
Versão simplificada para evitar limite de tokens
"""

# Prompt principal otimizado para outline
OPTIMIZED_OUTLINE_PROMPT = """
Crie um esboço detalhado para um ebook sobre: {topic}

ESPECIFICAÇÕES:
- Estilo: {style}
- Páginas: {length}
- Público: {target_audience}
- Nível: {depth_level}
- Objetivo: {main_objective}

ESTRUTURA REQUERIDA:

1. TÍTULO PRINCIPAL (atrativo para o tema)

2. INTRODUÇÃO:
   - Por que este tema é importante
   - O que o leitor aprenderá
   - Como usar o livro

3. CAPÍTULOS (5-8 capítulos):
   Para cada capítulo:
   - Título do capítulo
   - 3-4 subtópicos principais
   - Objetivo específico

4. CONCLUSÃO:
   - Resumo dos pontos principais
   - Próximos passos para o leitor

Seja específico e prático. Use markdown para formatação.
"""

# Prompt para escrita de conteúdo
OPTIMIZED_WRITING_PROMPT = """
Escreva o conteúdo completo de um ebook baseado neste esboço:

ESBOÇO:
{outline}

ESPECIFICAÇÕES:
- Tópico: {topic}
- Estilo: {style}
- Público: {target_audience}
- Nível: {depth_level}
- Objetivo: {main_objective}

INSTRUÇÕES:
1. Siga a estrutura do esboço
2. Desenvolva cada seção adequadamente
3. Use linguagem clara
4. Inclua exemplos práticos
5. Use formatação markdown

Escreva um ebook completo e profissional.
"""

# Prompts por tipo de livro (simplificados)
BUSINESS_STYLE = """
Para ebooks de negócios, inclua:
- Cases reais
- Métricas e ROI
- Estratégias práticas
- Exemplos de mercado
"""

TECHNICAL_STYLE = """
Para ebooks técnicos, inclua:
- Exemplos de código
- Diagramas (descrições)
- Tutoriais passo-a-passo
- Troubleshooting
"""

SELF_HELP_STYLE = """
Para desenvolvimento pessoal, inclua:
- Exercícios práticos
- Reflexões pessoais
- Histórias inspiradoras
- Passos de ação
"""

EDUCATIONAL_STYLE = """
Para conteúdo educacional, inclua:
- Conceitos fundamentais
- Exemplos didáticos
- Exercícios de fixação
- Resumos por capítulo
"""

# Dicionário principal simplificado
EBOOK_PROMPTS = {
    "outline": OPTIMIZED_OUTLINE_PROMPT,
    "writing": OPTIMIZED_WRITING_PROMPT,
    "business": BUSINESS_STYLE,
    "technical": TECHNICAL_STYLE,
    "self_help": SELF_HELP_STYLE,
    "educational": EDUCATIONAL_STYLE,
}

# Parâmetros padrão simplificados
DEFAULT_PARAMETERS = {
    "📈 Negócios": {
        "style": "Executivo e prático",
        "target_audience": "Empresários e gestores",
        "depth_level": "Estratégico com foco em resultados",
        "main_objective": "Ensinar estratégias de negócios eficazes",
    },
    "🛠️ Técnico": {
        "style": "Técnico e didático", 
        "target_audience": "Profissionais e estudantes da área",
        "depth_level": "Intermediário a avançado",
        "main_objective": "Explicar conceitos técnicos de forma clara",
    },
    "💡 Autoajuda": {
        "style": "Inspiracional e prático",
        "target_audience": "Pessoas em busca de crescimento pessoal", 
        "depth_level": "Acessível com profundidade emocional",
        "main_objective": "Guiar o desenvolvimento pessoal através de técnicas comprovadas",
    },
    "🎓 Educacional": {
        "style": "Didático e claro",
        "target_audience": "Estudantes e educadores",
        "depth_level": "Progressivo e estruturado", 
        "main_objective": "Educar sobre o tema de forma didática e estruturada",
    },
    "📝 Narrativo": {
        "style": "Envolvente e descritivo",
        "target_audience": "Leitores interessados em narrativas",
        "depth_level": "Envolvente com profundidade narrativa",
        "main_objective": "Contar uma história envolvente e significativa",
    }
}