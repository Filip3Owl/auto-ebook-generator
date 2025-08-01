# 📚 Auto‑Ebook Generator

Automatic eBook generator using **Streamlit** + **AI** (OpenAI), ready to create digital books from a natural language prompt.

Create complete eBooks with chapters, sections, cohesive content, and an illustrative cover. Export to formats like **EPUB** and **PDF** for reading on Kindle and other devices.

---

## 🚀 Features

* ✅ Interactive web interface with [Streamlit](https://streamlit.io/)
* ✅ Automated book writing with OpenAI GPT (e.g., GPT-3.5, GPT-4)
* ✅ Logical structure generation: chapters, sections, and paragraphs
* ✅ EPUB export with customizable templates
* ✅ Optional AI-generated cover
* ✅ Customizable writing style (professional, basic, etc.)

---

## 🧪 Demo

Run locally with:

```bash
streamlit run app.py
```

Access in your browser: [http://localhost:8501](http://localhost:8501)

---

## 🛠️ Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Filip3Owl/auto-ebook-generator.git
   cd auto-ebook-generator
   ```

2. Create and activate the virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate    # Linux/Mac
   .venv\Scripts\activate       # Windows
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## ⚙️ Configuration

Create a `.env` file in the root folder with your OpenAI key:

```env
OPENAI_API_KEY=your-key-here
```

You can configure the model (e.g., `gpt-4`, `gpt-3.5-turbo`) in the `utils/config.py` file.

---

## 🧠 Usage

1. Launch the app with `streamlit run app.py`
2. Enter a title and a prompt (book theme)
3. The system will:

   * Generate the outline (chapters/sections)
   * Automatically write the content
   * Optionally create an AI-generated cover
   * Export the eBook in the selected format

---

## 📁 Project Structure

```
auto-ebook-generator/
│
├── app.py                 # Streamlit interface
├── .env                  # Configurations (API Key)
├── requirements.txt      # Project dependencies
│
├── agents/               # Automated writing logic
│   ├── writer.py         # Content writing
│   └── outline.py        # Structure generation (chapters/sections)
│
├── core/                 # Prompt templates and business rules
│   └── prompts.py
│
├── utils/                # Helper functions and config
│   ├── config.py         # General system configurations
│   └── file_io.py        # File input/output handling
│
├── templates/            # EPUB layout templates
│   ├── basic/            # Simple style
│   └── professional/     # More refined style
│
├── output/               # Generated eBooks and covers
│   └── ebook_*.epub/pdf
│
├── assets/               # Styles, images, and CSS
│   ├── css/
│   └── images/
```

---

## 📦 Technologies Used

* [Python 3.10+](https://www.python.org/)
* [Streamlit](https://streamlit.io/)
* [OpenAI API](https://platform.openai.com/)
* [Ebooklib](https://github.com/aerkalov/ebooklib)
* [dotenv](https://pypi.org/project/python-dotenv/)
* [Pillow](https://python-pillow.org/) (for cover images)

---

## 📤 Export

* Generated books are saved in the `output/` folder
* The system exports in `.epub` format
* PDF support can be added using libraries like `reportlab` or `PyMuPDF`

---

## 🤝 Contributions

Contributions are welcome!

1. Fork the repository
2. Create a branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'My new feature'`)
4. Push to the remote repository
5. Open a Pull Request 🚀

---

## 📜 License

Distributed under the **MIT** license. See `LICENSE` for more information.

---

## 👨‍💻 Author

**Filipe Rangel**
🔗 [LinkedIn](https://www.linkedin.com/in/filiperangelambrosio/)
📂 [GitHub Repository](https://github.com/Filip3Owl/auto-ebook-generator)

---
