import os
from datetime import datetime

def save_ebook(content, title, format="pdf"):
    """Salva o ebook no formato especificado"""
    os.makedirs("output", exist_ok=True)
    
    if format == "pdf":
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=content)
        filename = f"output/ebook_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf.output(filename)
    else:  # markdown
        filename = f"output/ebook_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
    
    return filename