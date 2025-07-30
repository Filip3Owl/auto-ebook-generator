"""
Módulo com templates de prompts para geração de ebooks
"""

OUTLINE_PROMPT = """
Você é um escritor profissional de ebooks. Crie um esboço detalhado para um ebook sobre: {topic}

Requisitos:
- Estilo: {style}
- Tamanho aproximado: {length} páginas
- Público-alvo: Adultos interessados no tema

Retorne em formato Markdown com:
1. Título criativo
2. Capítulos principais
3. Subseções para cada capítulo
4. Introdução e conclusão
"""

CHAPTER_PROMPT = """
Escreva o conteúdo para a seção '{chapter_title}' de um ebook sobre {topic}.

Estilo: {style}
Seja detalhado e informativo.
Inclua exemplos práticos quando relevante.
"""

EBOOK_PROMPTS = {
    "outline": OUTLINE_PROMPT,
    "chapter": CHAPTER_PROMPT,
    "introduction": "Escreva uma introdução envolvente sobre {topic} no estilo {style}",
    "conclusion": "Escreva uma conclusão impactante sobre {topic} no estilo {style}"
}