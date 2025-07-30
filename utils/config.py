import os
from dotenv import load_dotenv

def load_config():
    """Carrega configurações do ambiente"""
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY não encontrada no arquivo .env")