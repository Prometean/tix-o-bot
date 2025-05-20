import re
import os
import json
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Any, Optional, Tuple


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


def send_handoff_email(user_message: str, language: str, conversation_history: List[Dict[str, str]], user_id: str = "Anónimo") -> Tuple[bool, str]:
    """
    Envía un correo electrónico al soporte cuando un usuario solicita hablar con un humano.
    
    Args:
        user_message: El mensaje del usuario que solicitó hablar con un humano
        language: El idioma detectado del usuario ("es" o "en")
        conversation_history: El historial de conversación reciente
        user_id: Identificador del usuario (si está disponible)
        
    Returns:
        Tuple[bool, str]: (Éxito del envío, Mensaje de estado)
    """
    try:
        # Obtener configuración del correo desde variables de entorno
        email_host = os.getenv("EMAIL_HOST", "smtp.gmail.com")
        email_port = int(os.getenv("EMAIL_PORT", "587"))
        email_user = os.getenv("EMAIL_USER", "notificaciones@tixbot.com")
        email_password = os.getenv("EMAIL_PASS", "")
        email_to = os.getenv("EMAIL_TO", "info@tix.do")
        
        # Si no hay contraseña configurada, no podemos enviar el correo
        if not email_password:
            return False, "No se ha configurado EMAIL_PASS en las variables de entorno"
            
        # Crear el mensaje
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_to
        msg['Subject'] = "Usuario solicitó asistencia humana"
        
        # Incluir la fecha y hora actual
        current_time = format_time()
        
        # Construir el cuerpo del mensaje
        body = f"""
        ¡Alerta de solicitud de atención humana!
        
        Fecha y hora: {current_time}
        Usuario: {user_id}
        Idioma detectado: {language}
        Mensaje que activó la solicitud: "{user_message}"
        
        --- Historial de conversación reciente ---
        """
        
        # Añadir las últimas 5 interacciones (o menos si no hay tantas)
        recent_history = conversation_history[-min(5, len(conversation_history)):]
        for i, entry in enumerate(recent_history):
            role = "Usuario" if entry["role"] == "user" else "Bot"
            body += f"\n{i+1}. {role}: {entry['content']}"
            
        body += """
        
        Por favor, contacte al usuario lo antes posible.
        
        --
        Enviado automáticamente por Tix-o-bot
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Conectar al servidor SMTP y enviar
        server = smtplib.SMTP(email_host, email_port)
        server.starttls()
        server.login(email_user, email_password)
        text = msg.as_string()
        server.sendmail(email_user, email_to, text)
        server.quit()
        
        success_msg = f"Correo enviado exitosamente a {email_to}"
        return True, success_msg
        
    except Exception as e:
        error_msg = f"Error al enviar correo de handoff: {str(e)}"
        return False, error_msg