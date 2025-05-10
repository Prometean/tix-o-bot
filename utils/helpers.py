import re
from typing import Dict, List, Any, Optional
import json
import time

def detect_language(text: str) -> str:
    """
    Detecta si el texto está en español o inglés.
    
    Args:
        text: Texto a analizar
        
    Returns:
        Código de idioma ("es" o "en")
    """
    # Palabras comunes en español
    spanish_words = ["el", "la", "los", "las", "un", "una", "unos", "unas", "y", "o", "pero", 
                    "porque", "que", "como", "cuando", "donde", "quien", "cual", "este", "esta",
                    "estos", "estas", "ese", "esa", "esos", "esas", "mi", "tu", "su", "nuestro",
                    "vuestro", "por", "para", "con", "sin", "sobre", "bajo", "ante", "contra",
                    "entre", "según", "durante", "mediante", "excepto", "salvo", "incluso", 
                    "gracias", "hola", "qué", "cómo", "cuándo", "dónde", "porqué", "quién", "cuál"]
    
    # Convertir a minúsculas y separar palabras
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Contar palabras en español
    spanish_count = sum(1 for word in words if word in spanish_words)
    
    # Si más del 15% de las palabras son comunes en español, asumimos que es español
    if len(words) > 0 and spanish_count / len(words) >= 0.15:
        return "es"
    else:
        return "en"

def format_time(timestamp: Optional[float] = None) -> str:
    """
    Formatea una marca de tiempo en formato legible.
    
    Args:
        timestamp: Marca de tiempo UNIX (usa tiempo actual si es None)
        
    Returns:
        Cadena con tiempo formateado
    """
    if timestamp is None:
        timestamp = time.time()
    
    time_struct = time.localtime(timestamp)
    return time.strftime("%d/%m/%Y %H:%M:%S", time_struct)

def save_conversation_log(conversation: List[Dict[str, Any]], filename: str) -> None:
    """
    Guarda una conversación en un archivo JSON.
    
    Args:
        conversation: Lista de mensajes
        filename: Nombre del archivo donde guardar
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(conversation, f, ensure_ascii=False, indent=2)

def load_conversation_log(filename: str) -> List[Dict[str, Any]]:
    """
    Carga una conversación desde un archivo JSON.
    
    Args:
        filename: Nombre del archivo a cargar
        
    Returns:
        Lista de mensajes de la conversación
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []