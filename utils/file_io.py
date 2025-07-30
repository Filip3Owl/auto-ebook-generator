import os
from datetime import datetime
import re

def save_ebook(content, title, format="markdown"):
    """Salva o ebook no formato especificado com tratamento de erros"""
    
    # Criar diretório de saída
    os.makedirs("output", exist_ok=True)
    
    # Limpar título para nome de arquivo
    clean_title = re.sub(r'[^\w\s-]', '', title)
    clean_title = re.sub(r'[-\s]+', '_', clean_title)
    clean_title = clean_title[:30]  # Limitar tamanho
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    try:
        if format.lower() == "pdf":
            return save_as_pdf(content, clean_title, timestamp)
        elif format.lower() == "html":
            return save_as_html(content, clean_title, timestamp)
        elif format.lower() == "epub":
            return save_as_epub(content, clean_title, timestamp)
        else:  # markdown (padrão)
            return save_as_markdown(content, clean_title, timestamp)
            
    except Exception as e:
        # Fallback para markdown simples
        print(f"Erro ao salvar em {format}: {e}")
        return save_as_markdown(content, clean_title, timestamp)

def save_as_markdown(content, title, timestamp):
    """Salva como arquivo Markdown"""
    filename = f"output/ebook_{title}_{timestamp}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    
    return filename

def save_as_html(content, title, timestamp):
    """Salva como arquivo HTML"""
    filename = f"output/ebook_{title}_{timestamp}.html"
    
    # Converter markdown básico para HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #333; border-bottom: 2px solid #333; }}
        h2 {{ color: #666; margin-top: 30px; }}
        h3 {{ color: #888; }}
        p {{ line-height: 1.6; }}
        ul, ol {{ line-height: 1.6; }}
    </style>
</head>
<body>
{markdown_to_html(content)}
</body>
</html>
"""
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    return filename

def save_as_pdf(content, title, timestamp):
    """Salva como arquivo PDF (requer fpdf2)"""
    try:
        from fpdf import FPDF
        
        filename = f"output/ebook_{title}_{timestamp}.pdf"
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Quebrar conteúdo em linhas para evitar overflow
        lines = content.split('\n')
        for line in lines:
            if line.strip():
                # Remover markdown básico
                clean_line = line.replace('#', '').replace('*', '').replace('_', '')
                pdf.multi_cell(0, 10, txt=clean_line.encode('latin-1', 'replace').decode('latin-1'))
                pdf.ln()
        
        pdf.output(filename)
        return filename
        
    except ImportError:
        print("fpdf2 não instalado. Salvando como markdown.")
        return save_as_markdown(content, title, timestamp)
    except Exception as e:
        print(f"Erro ao criar PDF: {e}. Salvando como markdown.")
        return save_as_markdown(content, title, timestamp)

def save_as_epub(content, title, timestamp):
    """Salva como arquivo EPUB (fallback para markdown)"""
    print("EPUB não implementado ainda. Salvando como markdown.")
    return save_as_markdown(content, title, timestamp)

def markdown_to_html(markdown_text):
    """Converte markdown básico para HTML"""
    html = markdown_text
    
    # Converter headers
    html = re.sub(r'^# (.*$)', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*$)', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*$)', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    
    # Converter listas
    html = re.sub(r'^- (.*$)', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*</li>)', r'<ul>\1</ul>', html, flags=re.DOTALL)
    
    # Converter negrito
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    
    # Converter parágrafos
    html = re.sub(r'^(?!<[hul])(.*$)', r'<p>\1</p>', html, flags=re.MULTILINE)
    
    return html

def get_output_files():
    """Lista arquivos na pasta de saída"""
    output_dir = "output"
    if not os.path.exists(output_dir):
        return []
    
    files = []
    for filename in os.listdir(output_dir):
        if filename.startswith("ebook_"):
            filepath = os.path.join(output_dir, filename)
            stat = os.stat(filepath)
            files.append({
                "name": filename,
                "path": filepath,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime)
            })
    
    return sorted(files, key=lambda x: x["modified"], reverse=True)