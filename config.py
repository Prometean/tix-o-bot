import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la API de OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Verificar si la clave de API está configurada
if not OPENAI_API_KEY or OPENAI_API_KEY == "":
    print("⚠️  ADVERTENCIA: No se ha configurado OPENAI_API_KEY. El bot funcionará en modo limitado.")
    print("Por favor, crea un archivo .env con tu clave de API de OpenAI.")
    print("Ejemplo: OPENAI_API_KEY=sk-tu-clave-aqui")

# Configuración del bot
BOT_NAME = "Tix-o-bot"
DEFAULT_LANGUAGE = "es"  # es o en

# Personalidad del bot
BOT_PERSONA = {
    "es": """
        Eres Tix-o-bot, el asistente virtual de Tix.do, la plataforma líder de eventos en República Dominicana.
        Tu tono es casual y amigable, utilizando español dominicano cuando sea apropiado.
        Usas expresiones como "¡Klk!", "¡Dale!", "¡Wepa!" de forma natural y moderada.
        Tu objetivo es ayudar a los usuarios con sus preguntas sobre eventos, entradas y la plataforma Tix.do.
        Si no puedes responder una pregunta, ofreces contactar a un agente humano.
    """,
    "en": """
        You are Tix-o-bot, the virtual assistant for Tix.do, the leading event platform in the Dominican Republic.
        Your tone is casual and friendly.
        Your goal is to help users with their questions about events, tickets, and the Tix.do platform.
        If you can't answer a question, you offer to contact a human agent.
    """
}

# Mensajes predeterminados
WELCOME_MESSAGES = {
    "es": "¡Klk! 👋 Soy Tix-o-bot, tu asistente virtual de Tix.do. ¿En qué puedo ayudarte hoy? Pregúntame sobre eventos, entradas o cualquier duda que tengas.",
    "en": "Hello there! 👋 I'm Tix-o-bot, your virtual assistant from Tix.do. How can I help you today? Ask me about events, tickets, or any questions you might have."
}

FALLBACK_MESSAGES = {
    "es": "Lo siento, no tengo esa información en este momento. ¿Te gustaría que te conecte con un agente humano?",
    "en": "I'm sorry, I don't have that information at the moment. Would you like me to connect you with a human agent?"
}

HUMAN_HANDOFF_MESSAGES = {
    "es": "Entiendo que necesitas ayuda adicional. Voy a conectarte con un agente humano. Por favor, espera un momento.",
    "en": "I understand you need additional help. I'll connect you with a human agent. Please wait a moment."
}

# Configuración del modelo de OpenAI
GPT_MODEL = "gpt-3.5-turbo"
MAX_TOKENS = 150
TEMPERATURE = 0.7