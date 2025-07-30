from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

def create_outline_chain(llm):
    """Cria a cadeia para geração de outlines com prompt otimizado"""
    
    # Prompt simplificado para caber no limite de tokens
    simplified_outline_template = """
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

EXEMPLO DE FORMATO:
# Título: [Título Atrativo]

## Introdução
- Hook inicial sobre o tema
- Promessa de valor
- Guia de uso

## Capítulo 1: [Nome]
- Subtópico A
- Subtópico B
- Subtópico C
- Objetivo: [O que o leitor aprenderá]

[Continue para outros capítulos...]

## Conclusão
- Síntese dos aprendizados
- Chamada para ação

Seja específico e prático. Use markdown para formatação.
"""

    prompt = PromptTemplate(
        input_variables=[
            "topic", "style", "length", "target_audience", 
            "depth_level", "main_objective"
        ],
        template=simplified_outline_template
    )
    
    return LLMChain(llm=llm, prompt=prompt, verbose=True)