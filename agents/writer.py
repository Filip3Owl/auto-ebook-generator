from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

def create_writing_chain(llm):
    """Cria a cadeia para escrita de conteúdo com prompt otimizado"""
    
    # Prompt otimizado para geração de conteúdo
    writing_template = """
Escreva o conteúdo completo de um ebook baseado neste esboço:

ESBOÇO:
{outline}

ESPECIFICAÇÕES:
- Tópico: {topic}
- Estilo: {style}
- Público: {target_audience}
- Nível: {depth_level}
- Objetivo: {main_objective}

INSTRUÇÕES DE ESCRITA:
1. Siga exatamente a estrutura do esboço
2. Desenvolva cada seção com 200-400 palavras
3. Use linguagem clara e adequada ao público
4. Inclua exemplos práticos quando relevante
5. Mantenha tom consistente com o estilo
6. Use formatação markdown (##, ###, -, etc.)

ELEMENTOS OBRIGATÓRIOS:
- Introdução envolvente (300-500 palavras)
- Cada capítulo bem desenvolvido
- Exemplos ou casos práticos
- Conclusão motivadora (200-300 palavras)
- Transições suaves entre seções

FORMATO DE SAÍDA:
Use markdown com:
- # para título principal
- ## para capítulos
- ### para subseções
- - para listas
- **negrito** para ênfase

Seja informativo, prático e engajante. Escreva um ebook completo e profissional.
"""

    prompt = PromptTemplate(
        input_variables=[
            "outline", "topic", "style", "target_audience", 
            "depth_level", "main_objective"
        ],
        template=writing_template
    )
    
    return LLMChain(llm=llm, prompt=prompt, verbose=True)