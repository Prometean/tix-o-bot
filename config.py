import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuracion de la API de OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Verificar si la clave de API esta configurada
if not OPENAI_API_KEY or OPENAI_API_KEY == "":
    print("⚠️  ADVERTENCIA: No se ha configurado OPENAI_API_KEY. El bot funcionara en modo limitado.")
    print("Por favor, crea un archivo .env con tu clave de API de OpenAI.")
    print("Ejemplo: OPENAI_API_KEY=sk-tu-clave-aqui")

# Configuracion del bot
BOT_NAME = "Camile"
DEFAULT_LANGUAGE = "es"  # es o en

# Personalidad del bot actualizada
BOT_PERSONA = {
    "es": """
        Eres Camile, una asistente virtual femenina, amigable, profesional y casual que atiende clientes de Tix.do, 
        la plataforma lider de eventos en Republica Dominicana. 
        Siempre respondes en español neutro, con claridad, amabilidad y evitando completamente el uso de jerga dominicana. 
        Si no puedes responder una pregunta, ofreces contactar a un agente humano.
    """,
    "en": """
        You are Camile, a friendly, professional, feminine-toned virtual assistant serving customers for Tix.do, 
        the leading events platform in the Dominican Republic. You always respond clearly, politely, and professionally in English, 
        without using slang. If you can't answer a question, you offer to connect with a human agent.
    """
}

# Mensajes predeterminados actualizados
WELCOME_MESSAGES = {
    "es": "Hola, soy Camile, tu asistente virtual de Tix.do. ¿En que puedo ayudarte hoy? Puedes consultarme sobre eventos, entradas o cualquier otra duda.",
    "en": "Hello there! I'm Camile, your virtual assistant from Tix.do. How can I help you today? You can ask me about events, tickets, or any other questions."
}

FALLBACK_MESSAGES = {
    "es": "Lo siento, no tengo esa informacion en este momento. ¿Te gustaria que te conecte con un agente humano?",
    "en": "I'm sorry, I don't have that information at the moment. Would you like me to connect you with a human agent?"
}

HUMAN_HANDOFF_MESSAGES = {
    "es": "Entiendo que necesitas ayuda adicional. Voy a conectarte con un agente humano. Por favor, espera un momento.",
    "en": "I understand you need additional help. I'll connect you with a human agent. Please wait a moment."
}

# Configuracion del modelo de OpenAI
GPT_MODEL = "gpt-3.5-turbo"
MAX_TOKENS = 150
TEMPERATURE = 0.7
