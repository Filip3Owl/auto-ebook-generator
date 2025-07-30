# Opção 1: Usando pasta agents
from agents.outline.chain import create_outline_chain
from agents.writer.chain import create_writing_chain

# Opção 2: Se quiser manter modules, adicione ao PATH
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from modules.outline.chain import create_outline_chain