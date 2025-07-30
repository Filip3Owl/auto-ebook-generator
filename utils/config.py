import os
from dotenv import load_dotenv

def load_config():
    """Carrega configurações do ambiente"""
    load_dotenv()
    
    if "OPENAI_API_KEY" not in os.environ:
        raise ValueError("OPENAI_API_KEY não encontrada no .env")
    
    return {
        "openai_key": os.getenv("OPENAI_API_KEY"),
        "max_tokens": int(os.getenv("MAX_TOKENS", "4000")),
        "temperature": float(os.getenv("TEMPERATURE", "0.7"))
    }