OUTLINE_PROMPT = """
Você é um escritor profissional de ebooks. Crie um esboço detalhado para um ebook sobre {topic}.
Estilo: {style}
Número aproximado de páginas: {length}

O esboço deve incluir:
1. Título criativo
2. Capítulos principais (pelo menos {length})
3. Subseções para cada capítulo
4. Conclusão
5. Seção de recursos/adicionais

Retorne em formato Markdown com hierarquia clara.
"""

EBOOK_PROMPTS = {
    "introduction": "Escreva uma introdução envolvente sobre {topic} no estilo {style}",
    "chapter": "Escreva o capítulo '{chapter_title}' sobre {topic} no estilo {style}",
    "conclusion": "Escreva uma conclusão impactante sobre {topic} no estilo {style}"
}