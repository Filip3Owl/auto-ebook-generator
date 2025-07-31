# 📚 Auto‑Ebook Generator

Gerador automático de eBooks com **Streamlit** + **IA** (OpenAI), pronto para criar livros digitais a partir de um prompt em linguagem natural.

Crie eBooks completos com capítulos, seções, conteúdo coeso e capa ilustrativa. Exporte em formatos como **EPUB** e **PDF** para leitura em Kindle e outros dispositivos.

---

## 🚀 Funcionalidades

- ✅ Interface web interativa com [Streamlit](https://streamlit.io/)
- ✅ Escrita automatizada de livros com OpenAI GPT (ex: GPT-3.5, GPT-4)
- ✅ Geração de estrutura lógica (outline): capítulos, seções e parágrafos
- ✅ Exportação para EPUB com templates personalizáveis
- ✅ Criação opcional de capa por IA
- ✅ Estilo de escrita personalizável (profissional, básico, etc.)

---

## 🧪 Demonstração

Inicie localmente com:

```bash
streamlit run app.py
````

Acesse via navegador: [http://localhost:8501](http://localhost:8501)

---

## 🛠️ Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/Filip3Owl/auto-ebook-generator.git
   cd auto-ebook-generator
   ```

2. Crie e ative o ambiente virtual:

   ```bash
   python -m venv .venv
   source .venv/bin/activate    # Linux/Mac
   .venv\Scripts\activate       # Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

---

## ⚙️ Configuração

Crie um arquivo `.env` na raiz com sua chave da OpenAI:

```env
OPENAI_API_KEY=sua-chave-aqui
```

Você pode configurar o modelo (ex: `gpt-4`, `gpt-3.5-turbo`) no arquivo `utils/config.py`.

---

## 🧠 Uso

1. Abra o app com `streamlit run app.py`
2. Digite um título e um prompt (tema do livro)
3. O sistema:

   * Gera o outline (capítulos/seções)
   * Escreve automaticamente o conteúdo
   * Cria capa com IA (opcional)
   * Exporta o eBook no formato desejado

---

## 📁 Estrutura do Projeto

```
auto-ebook-generator/
│
├── app.py                 # Interface Streamlit
├── .env                  # Configurações (API Key)
├── requirements.txt      # Dependências do projeto
│
├── agents/               # Lógica de escrita automática
│   ├── writer.py         # Escrita do conteúdo
│   └── outline.py        # Geração da estrutura (capítulos/seções)
│
├── core/                 # Prompt templates e regras de negócio
│   └── prompts.py
│
├── utils/                # Funções auxiliares e configuração
│   ├── config.py         # Configurações gerais do sistema
│   └── file_io.py        # Manipulação de arquivos de entrada/saída
│
├── templates/            # Templates de layout para EPUB
│   ├── basic/            # Estilo simples
│   └── professional/     # Estilo mais refinado
│
├── output/               # eBooks e capas geradas
│   └── ebook_*.epub/pdf
│
├── assets/               # Estilos, imagens e CSS
│   ├── css/
│   └── images/
```

---

## 📦 Tecnologias Utilizadas

* [Python 3.10+](https://www.python.org/)
* [Streamlit](https://streamlit.io/)
* [OpenAI API](https://platform.openai.com/)
* [Ebooklib](https://github.com/aerkalov/ebooklib)
* [dotenv](https://pypi.org/project/python-dotenv/)
* [Pillow](https://python-pillow.org/) (para imagens de capa)

---

## 📤 Exportação

* Os livros gerados ficam na pasta `output/`
* O sistema exporta em formato `.epub`
* O suporte a `.pdf` pode ser adicionado com bibliotecas como `reportlab` ou `PyMuPDF`

---

## 🤝 Contribuições

Contribuições são bem-vindas!

1. Faça um fork do repositório
2. Crie uma branch (`git checkout -b feature/sua-feature`)
3. Commit suas mudanças (`git commit -m 'Minha nova feature'`)
4. Push para o repositório remoto
5. Abra um Pull Request 🚀

---

## 📜 Licença

Distribuído sob a licença **MIT**. Veja `LICENSE` para mais informações.

---

## 👨‍💻 Autor

**Filipe Rangel**
🔗 [LinkedIn](https://www.linkedin.com/in/filiperangelambrosio/)
📂 [Repositório GitHub](https://github.com/Filip3Owl/auto-ebook-generator)

---

```

Se quiser, posso te gerar um print do app em funcionamento para usar no README (via `st.screenshot()` ou `printscreen` manual) e/ou ajudar com deploy no **Streamlit Cloud**, **HuggingFace Spaces**, ou **Render**. Deseja isso?
```
