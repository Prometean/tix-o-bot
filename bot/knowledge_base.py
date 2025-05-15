from typing import List, Tuple, Dict, Optional
import re
from difflib import SequenceMatcher

# Base de conocimiento: Preguntas frecuentes (FAQs)
# Formato: (pregunta, respuesta)
FAQS = [
    # Saludos y conversación básica
    (
        "Hola",
        "¡Hola, Gracias por contactarnos!, te asiste Camila. ¿En qué puedo ayudarte hoy?"
    ),
    (
        "Hello",
        "Hi, thank you for contacting us! This is Camila assisting you. How can I help you today?"
    ),
    (
        "Gracias",
        "¡De nada! Siempre es un placer ayudarte. Si tienes más preguntas, estoy aquí para ti."
    ),
    (
        "Thank you",
        "You're welcome! It's always a pleasure to help. If you have more questions, I'm here for you."
    ),
    # Preguntas generales sobre Tix.do
    (
        "¿Qué es Tix.do?",
        "Tix.do es la plataforma líder de venta de entradas y gestión de eventos en República Dominicana. Facilitamos la compra de boletos para conciertos, obras de teatro, eventos deportivos y más."
    ),
    (
        "What is Tix.do?",
        "Tix.do is the leading ticket sales and event management platform in the Dominican Republic. We facilitate the purchase of tickets for concerts, plays, sporting events, and more."
    ),
    # Preguntas sobre compra de boletos
    (
        "¿Cómo compro entradas?",
        "Para comprar entradas en Tix.do: 1) Selecciona el evento que te interesa, 2) Escoge la cantidad y tipo de boletos, 3) Completa el pago con tarjeta de crédito. ¡Listo! Recibirás tus boletos por correo electrónico."
    ),
    (
        "How do I buy tickets?",
        "To buy tickets on Tix.do: 1) Select the event you're interested in, 2) Choose the quantity and type of tickets, 3) Complete payment by credit card. Done! You'll receive your tickets by email."
    ),
    # Preguntas sobre medios de pago
    (
        "¿Qué métodos de pago aceptan?",
        "En Tix.do aceptamos múltiples formas de pago: tarjetas de crédito/débito (Visa y Mastercard) y transferencias bancarias."
    ),
    (
        "What payment methods do you accept?",
        "At Tix.do we accept multiple payment methods: credit/debit cards (Visa and Mastercard) and bank transfers."
    ),
    # Preguntas sobre reembolsos
    (
        "¿Puedo solicitar un reembolso?",
        "La política de reembolso depende de cada organizador. En general, los boletos no son reembolsables, pero en caso de cancelación del evento por parte del organizador, se garantiza el reembolso. Recuerda que el cargo por servicio no es reembolsable. Contacta a info@tix.do para casos específicos."
    ),
    (
        "Can I request a refund?",
        "The refund policy depends on each organizer. In general, tickets are non-refundable, but in case of cancellation of the event by the organizer, a refund is guaranteed. Contact info@tix.do for specific cases."
    ),
    # Preguntas sobre entradas perdidas
    (
        "Perdí mis entradas, ¿qué hago?",
        "¡No te preocupes! Por favor confírmanos tu correo electrónico y el nombre del evento para poder reenviar tus entradas lo antes posible."
    ),
    (
        "I lost my tickets, what should I do?",
        "No worries! Please confirm your email address and the name of the event so we can resend your tickets as soon as possible."
    ),
    # Preguntas sobre reventa
    (
        "¿Puedo revender mis entradas?",
        "La reventa no oficial de boletos está prohibida en Tix.do."
    ),
    (
        "Can I resell my tickets?",
        "Unofficial ticket resale is prohibited on Tix.do."
    ),
    # Preguntas sobre contacto
    (
        "¿Cómo puedo contactar a servicio al cliente?",
        "Puedes contactar a nuestro equipo de servicio al cliente a través de: Email: info@tix.do, WhatsApp: +1 (809)330-3797, o en instagram @Tix.do."
    ),
    (
        "How can I contact customer service?",
        "You can contact our customer service team through: Email: info@tix.do, WhatsApp: +1 (809) 330-3797, or on instagram @Tix.do."
    ),
    # Preguntas sobre el bot
    (
        "¿Quién eres tú?",
        "¡Hola! Soy Camila, la asistente virtual de Tix.do. Estoy aquí para ayudarte con preguntas sobre eventos, entradas y más. Si necesitas hablar con un humano, solo dímelo y te conectaré con un agente de servicio al cliente."
    ),
    (
        "Who are you?",
        "Hello! I'm Camila, the virtual assistant for Tix.do. I'm here to help you with questions about events, tickets, and more. If you need to talk to a human, just tell me and I'll connect you with a customer service agent."
    )
]

def clean_text(text: str) -> str:
    """
    Limpia el texto para comparación (elimina puntuación, espacios extras, etc.)
    
    Args:
        text: Texto a limpiar
        
    Returns:
        Texto limpio en minúsculas
    """
    # Convertir a minúsculas
    text = text.lower()
    
    # Eliminar puntuación y caracteres especiales
    text = re.sub(r'[^\w\s]', '', text)
    
    # Eliminar espacios múltiples
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calcula la similitud entre dos textos.
    
    Args:
        text1: Primer texto
        text2: Segundo texto
        
    Returns:
        Valor de similitud entre 0 y 1
    """
    return SequenceMatcher(None, clean_text(text1), clean_text(text2)).ratio()

def find_best_faq_match(user_query: str, language: str = "es") -> Tuple[Optional[str], float]:
    """
    Busca la mejor coincidencia para la consulta del usuario en las FAQs.
    
    Args:
        user_query: Consulta del usuario
        language: Idioma preferido ("es" o "en")
        
    Returns:
        Tuple con la respuesta y el nivel de confianza
    """
    best_match = None
    best_score = 0.0
    
    # Preprocesar la consulta del usuario
    clean_query = clean_text(user_query)
    
    # Detectar idioma basado en características
    detected_lang = language
    
    # Palabras en español que ayudan a identificar el idioma
    spanish_indicators = ["que", "como", "donde", "cuando", "por", "para", "quien", "cual", 
                         "porque", "qué", "cómo", "dónde", "cuándo", "quién", "cuál", 
                         "gracias", "hola", "adios", "ayuda", "necesito"]
                         
    # Detectar idioma basado en palabras clave
    for word in spanish_indicators:
        if f" {word} " in f" {clean_query} " or clean_query.startswith(f"{word} ") or clean_query.endswith(f" {word}"):
            detected_lang = "es"
            break
    else:
        # Si no encontró palabras en español, probablemente es inglés
        if len(clean_query.split()) > 1:  # Si tiene más de una palabra
            detected_lang = "en"
    
    # Si el idioma explícitamente seleccionado difiere del detectado, priorizar el seleccionado
    actual_lang = language if language != detected_lang else detected_lang
    
    for question, answer in FAQS:
        # Determinar si la pregunta está en español
        is_spanish_question = "¿" in question or question in ["Hola", "Gracias"]
        
        # Filtrar preguntas por idioma
        if (actual_lang == "es" and not is_spanish_question) or (actual_lang == "en" and is_spanish_question):
            continue
        
        # Calcular similitud
        similarity = calculate_similarity(user_query, question)
        
        # Si es una coincidencia exacta (por ejemplo, botón FAQ presionado)
        if user_query == question:
            return answer, 1.0
        
        # Actualizar mejor coincidencia si corresponde
        if similarity > best_score:
            best_score = similarity
            best_match = answer
    
    # Ajustar el umbral de confianza para ser más permisivo
    confidence_threshold = 0.5  # Bajamos el umbral para ser más flexibles
    
    return best_match, best_score if best_score >= confidence_threshold else (None, 0.0)