import os
from dotenv import load_dotenv

def load_config():
    """Carrega configurações do ambiente com tratamento de erros"""
    try:
        load_dotenv()
        
        # Não é obrigatório ter OPENAI_API_KEY no .env
        # pois será fornecida via interface do Streamlit
        return True
        
    except Exception as e:
        print(f"Aviso: Erro ao carregar .env: {e}")
        return False

def get_api_key():
    """Obtém a API key do ambiente"""
    return os.getenv("OPENAI_API_KEY")

def validate_api_key(api_key):
    """Valida se a API key tem formato correto"""
    if not api_key:
        return False, "API Key não fornecida"
    
    if not api_key.startswith("sk-"):
        return False, "API Key deve começar com 'sk-'"
    
    if len(api_key) < 20:
        return False, "API Key muito curta"
    
    return True, "API Key válida"