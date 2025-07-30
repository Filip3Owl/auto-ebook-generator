from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

def create_writing_chain(llm):
    """Cria uma cadeia LLM para geração estruturada de livros digitais em múltiplos formatos."""

    writing_template = """
Você é um autor experiente responsável por escrever um livro completo e profissional com base nas seguintes informações:

TEMA PRINCIPAL: {topic}
ESTILO DE ESCRITA: {style}
PÚBLICO-ALVO: {target_audience}
NÍVEL DE PROFUNDIDADE: {depth_level}
OBJETIVO DO LIVRO: {main_objective}
FORMATO DE SAÍDA: {output_format} (Ex: markdown, pdf, html, epub)

ESTRUTURA OBRIGATÓRIA DO LIVRO:

1. Capa  
   - Título: {topic}  
   - Autor: {author_name}  
   - Editora: (se aplicável)  
   - Inclua uma descrição breve e chamativa (em formato de texto, sem imagem real).

2. Contracapa  
   - Sinopse da obra  
   - Comentários de críticos (fictícios, se necessário)  
   - Biografia curta do autor  
   - Frase de impacto.

3. Folha de rosto  
   - Título do livro  
   - Nome do autor

4. Verso da folha de rosto  
   - Edição, número ISBN (simulado), local e ano de publicação  
   - Direitos autorais fictícios

5. Dedicatória (opcional)  
   - Dê um toque pessoal

6. Agradecimentos (opcional)  
   - Agradeça pessoas ou instituições relevantes

7. Epígrafe (opcional)  
   - Inclua uma citação ou frase inspiradora relacionada ao tema

8. Prefácio / Introdução  
   - Explique o contexto do livro, o motivo da escrita e o que o leitor encontrará

9. Sumário  
   - Gere uma lista numerada de capítulos com títulos significativos, baseando-se no esboço fornecido

10. Conteúdo Principal  
   - Desenvolva cada capítulo baseado no esboço abaixo, com 200–400 palavras por seção  
   - Use linguagem clara e consistente  
   - Inclua exemplos práticos sempre que possível  
   - Use transições suaves entre seções

ESBOÇO:
{outline}

11. Conclusão  
   - Reforce os principais aprendizados  
   - Ofereça uma mensagem final inspiradora

FORMATAÇÃO:
- Use Markdown se o formato for "markdown"
- Use HTML se o formato for "html"
- Mantenha estrutura limpa e com hierarquia de títulos:
  - # Título principal
  - ## Capítulos
  - ### Subtópicos
  - - Listas
  - **Negrito** para ênfase
  - (Evite elementos gráficos ou imagens reais — apenas texto descritivo)

OBJETIVO FINAL:
Gerar um livro completo, coeso, informativo, interessante e pronto para publicação no formato especificado.
"""

    prompt = PromptTemplate(
        input_variables=[
            "outline",
            "topic",
            "style",
            "target_audience",
            "depth_level",
            "main_objective",
            "output_format",
            "author_name"
        ],
        template=writing_template
    )

    return LLMChain(llm=llm, prompt=prompt, verbose=True)
