from typing import List, Tuple, Dict, Optional
import re
from difflib import SequenceMatcher

# Base de conocimiento: Preguntas frecuentes (FAQs)
# Formato: (pregunta, respuesta)
FAQS = [
    # Saludos y conversación básica
    (
        "Hola",
        "¡Klk! ¿Qué tal? Soy Tix-o-bot, tu asistente virtual de Tix.do. ¿En qué puedo ayudarte hoy?"
    ),
    (
        "Hello",
        "Hello there! I'm Tix-o-bot, your virtual assistant from Tix.do. How can I help you today?"
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
        "Para comprar entradas en Tix.do: 1) Crea una cuenta o inicia sesión, 2) Selecciona el evento que te interesa, 3) Escoge la cantidad y tipo de boletos, 4) Completa el pago con tarjeta de crédito, transferencia o pago móvil. ¡Listo! Recibirás tus boletos por correo electrónico."
    ),
    (
        "How do I buy tickets?",
        "To buy tickets on Tix.do: 1) Create an account or log in, 2) Select the event you're interested in, 3) Choose the quantity and type of tickets, 4) Complete payment by credit card, bank transfer, or mobile payment. Done! You'll receive your tickets by email."
    ),
    
    # Preguntas sobre medios de pago
    (
        "¿Qué métodos de pago aceptan?",
        "En Tix.do aceptamos múltiples formas de pago: tarjetas de crédito/débito (Visa, Mastercard, American Express), transferencias bancarias, pago móvil (tPago), y en algunos casos efectivo en puntos autorizados."
    ),
    (
        "What payment methods do you accept?",
        "At Tix.do we accept multiple payment methods: credit/debit cards (Visa, Mastercard, American Express), bank transfers, mobile payment (tPago), and in some cases cash at authorized points."
    ),
    
    # Preguntas sobre reembolsos
    (
        "¿Puedo solicitar un reembolso?",
        "La política de reembolso depende de cada organizador. En general, los boletos no son reembolsables, pero en caso de cancelación del evento por parte del organizador, se garantiza el reembolso completo. Contacta a soporte@tix.do para casos específicos."
    ),
    (
        "Can I request a refund?",
        "The refund policy depends on each organizer. In general, tickets are non-refundable, but in case of cancellation of the event by the organizer, a full refund is guaranteed. Contact support@tix.do for specific cases."
    ),
    
    # Preguntas sobre entradas perdidas
    (
        "Perdí mis entradas, ¿qué hago?",
        "¡No te preocupes! Puedes recuperar tus entradas iniciando sesión en tu cuenta de Tix.do y accediendo a la sección 'Mis Boletos'. Desde allí podrás descargar o reenviar tus entradas a tu correo. Si necesitas asistencia adicional, escribe a soporte@tix.do."
    ),
    (
        "I lost my tickets, what should I do?",
        "Don't worry! You can recover your tickets by logging into your Tix.do account and accessing the 'My Tickets' section. From there you can download or resend your tickets to your email. If you need additional assistance, write to support@tix.do."
    ),
    
    # Preguntas sobre reventa
    (
        "¿Puedo revender mis entradas?",
        "La reventa no oficial de boletos está prohibida en Tix.do. Sin embargo, para algunos eventos ofrecemos la función de transferencia segura de boletos, que te permite transferir legalmente tus entradas a otra persona a través de nuestra plataforma."
    ),
    (
        "Can I resell my tickets?",
        "Unofficial ticket resale is prohibited on Tix.do. However, for some events we offer the secure ticket transfer function, which allows you to legally transfer your tickets to another person through our platform."
    ),
    
    # Preguntas sobre contacto
    (
        "¿Cómo puedo contactar a servicio al cliente?",
        "Puedes contactar a nuestro equipo de servicio al cliente a través de: Email: soporte@tix.do, Teléfono: +1 (809) 555-TIXS (8497), WhatsApp: +1 (829) 555-TIXS (8497), o en nuestras redes sociales @TixDO."
    ),
    (
        "How can I contact customer service?",
        "You can contact our customer service team through: Email: support@tix.do, Phone: +1 (809) 555-TIXS (8497), WhatsApp: +1 (829) 555-TIXS (8497), or on our social networks @TixDO."
    ),
    
    # Preguntas sobre el bot
    (
        "¿Quién eres tú?",
        "¡Klk! Soy Tix-o-bot, el asistente virtual de Tix.do. Estoy aquí para ayudarte con preguntas sobre eventos, entradas y más. Si necesitas hablar con un humano, solo dímelo y te conectaré con un agente de servicio al cliente."
    ),
    (
        "Who are you?",
        "Hello! I'm Tix-o-bot, the virtual assistant for Tix.do. I'm here to help you with questions about events, tickets, and more. If you need to talk to a human, just tell me and I'll connect you with a customer service agent."
    ),
    
    # Preguntas adicionales sobre la plataforma
    (
        "¿Cómo me registro en Tix.do?",
        "Registrarse en Tix.do es muy fácil: 1) Ve a www.tix.do y haz clic en 'Crear cuenta', 2) Completa el formulario con tu información personal, 3) Verifica tu correo electrónico, y 4) ¡Listo! Ya puedes empezar a comprar boletos para tus eventos favoritos."
    ),
    (
        "How do I register on Tix.do?",
        "Registering on Tix.do is very easy: 1) Go to www.tix.do and click on 'Create account', 2) Fill out the form with your personal information, 3) Verify your email, and 4) Done! You can now start buying tickets for your favorite events."
    ),
    
    # Preguntas sobre seguridad
    (
        "¿Es seguro comprar en Tix.do?",
        "¡Absolutamente! Tix.do utiliza tecnología de encriptación SSL para proteger tus datos personales y financieros. Además, somos la plataforma oficial de venta de boletos para cientos de eventos en República Dominicana, garantizando la autenticidad de cada entrada vendida."
    ),
    (
        "Is it safe to buy on Tix.do?",
        "Absolutely! Tix.do uses SSL encryption technology to protect your personal and financial data. Additionally, we are the official ticket selling platform for hundreds of events in the Dominican Republic, guaranteeing the authenticity of each ticket sold."
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