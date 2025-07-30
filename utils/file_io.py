import os
from datetime import datetime
import re
from io import BytesIO
from base64 import b64encode

def save_ebook(content, title, format="markdown"):
    """Salvaa o ebook no formato especificado com tratamento de erros"""
    
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
    """Salva como arquivo PDF com melhor formatação"""
    try:
        from fpdf import FPDF
        
        filename = f"output/ebook_{title}_{timestamp}.pdf"
        
        # Criar PDF com encoding UTF-8
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Adicionar fonte com suporte a UTF-8
        pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        pdf.set_font('DejaVu', '', 12)
        
        # Processar conteúdo
        lines = content.split('\n')
        for line in lines:
            if line.strip():
                # Processar diferentes níveis de cabeçalho
                if line.startswith('###'):
                    pdf.set_font('DejaVu', 'B', 12)
                    pdf.cell(0, 10, txt=line[4:].strip(), ln=1)
                    pdf.set_font('DejaVu', '', 12)
                elif line.startswith('##'):
                    pdf.set_font('DejaVu', 'B', 14)
                    pdf.cell(0, 10, txt=line[3:].strip(), ln=1)
                    pdf.set_font('DejaVu', '', 12)
                elif line.startswith('#'):
                    pdf.set_font('DejaVu', 'B', 16)
                    pdf.cell(0, 10, txt=line[1:].strip(), ln=1)
                    pdf.set_font('DejaVu', '', 12)
                else:
                    # Processar texto normal
                    pdf.multi_cell(0, 8, txt=line.encode('utf-8').decode('latin-1', 'replace'))
                pdf.ln(5)
        
        pdf.output(filename)
        return filename
        
    except ImportError:
        print("fpdf2 não instalado. Instale com: pip install fpdf2")
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

def get_file_preview(filepath):
    """Obtém uma pré-visualização do arquivo"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            return content[:500] + "..." if len(content) > 500 else content
    except:
        return "Não foi possível ler o conteúdo do arquivo."

def get_file_download_link(filepath):
    """Gera um link de download para o arquivo"""
    with open(filepath, "rb") as f:
        bytes = f.read()
        b64 = b64encode(bytes).decode()
        return f"data:application/octet-stream;base64,{b64}"