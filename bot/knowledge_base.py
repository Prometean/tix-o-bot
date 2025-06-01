from typing import Tuple, Optional
import re
from difflib import SequenceMatcher

# Base de conocimiento: Preguntas frecuentes (FAQs)
# Formato: (pregunta, respuesta)
FAQS = [
    # Saludos y conversación básica
    (
        "Hola",
        "¡Hola!\n\n¡Gracias por contactarnos!\n\n¿En qué puedo asistirte hoy?"
    ),
    (
        "Buenas",
        "¡Hola!\n\n¡Gracias por contactarnos!\n\n¿En qué puedo asistirte hoy?"
    ),
    (
        "Hello",
        "Hi!\n\nThank you for contacting us!\n\nHow can I help you today?"
    ),
    (
        "Gracias",
        "¡De nada! Siempre es un placer ayudarte. Si tienes más preguntas, estoy aquí para ti. Feliz día"
    ),
    (
        "Thank you",
        "You're welcome! It's always a pleasure to help. If you have more questions, I'm here for you. Have a nice day"
    ),
    
    # Compra de boletos/entradas
    (
        "¿Cómo compro entradas?",
        "Para comprar entradas en Tix.do debes acceder al link del evento que te interesa, seleccionar la cantidad y tipo de boletos, y completar el pago. Recibirás tus boletos por correo electrónico con un código QR."
    ),
    (
        "Quiero comprar boletas",
        "¡Hola!\n\nGracias por comunicarte con nosotros. Puedo compartirte el link del evento para que puedas visualizar los precios y realizar la compra de tus tickets.\n\nPor favor, indícame el nombre del evento que te interesa.\n\nFeliz día"
    ),
    (
        "Me interesan unas entradas",
        "¡Hola!\n\nGracias por comunicarte con nosotros. Por favor, indícame el nombre del evento para el que deseas adquirir entradas y te compartiré el link de compra.\n\nFeliz día"
    ),
    (
        "¿Cómo puedo adquirir boletas?",
        "¡Hola!\n\nGracias por comunicarte con nosotros. Te puedo proporcionar el link del evento para que puedas visualizar los precios y realizar la compra de tus tickets. Solo necesito que me indiques el evento que te interesa.\n\nFeliz día"
    ),
    (
        "How do I buy tickets?",
        "Hi!\n\nThank you for contacting us. I can share the link to the event so you can see the prices and purchase your tickets. Please let me know which event you're interested in.\n\nHave a nice day"
    ),
    
    # Información sobre eventos específicos
    (
        "Quedan entradas disponibles",
        "Para verificar la disponibilidad de entradas de este evento, por favor comunícate directamente con la producción. Puedes hacerlo a través del link del evento que te puedo proporcionar si me indicas cuál es el evento de tu interés."
    ),
    (
        "Quedan mesas disponibles",
        "Para información sobre disponibilidad de mesas, debes comunicarte directamente con la producción del evento. Puedes hacerlo a través del link del evento que te puedo proporcionar."
    ),
    
    # Publicación de eventos (para organizadores)
    (
        "¿Cómo publicar un evento?",
        "Para subir tu evento con nosotros solo debes crear tu perfil y llenar tus datos en nuestra página https://vendors.tix.do/register\n\nLuego de haber creado tu perfil podrás visualizar en tu cuenta la opción de crear evento, donde debes colocar todos los campos requeridos con la información.\n\nLa imagen debe ser 1,080 x 1,080 px exactos y no pesar más de 1.5 Mb. Tu evento tendrá un periodo de revisión de 15 a 30 min en la plataforma."
    ),
    (
        "¿Cuáles son los costos para publicar un evento?",
        "La publicación del evento es totalmente gratuita. El organizador solo paga el fee del procesamiento de transacción de un 4.9% + RD$25 por boleta vendida.\n\nEl participante del evento (Comprador) paga un cargo por servicio de un 8.5% + RD$15 de cada boleta adquirida."
    ),
    (
        "¿Qué información solicitan al comprador?",
        "En nuestra base de datos recopilamos el correo electrónico del comprador. Esta es la información de contacto principal que se utiliza para enviar los códigos QR de las entradas adquiridas."
    ),
    (
        "¿Qué información recibe el cliente tras comprar?",
        "El participante recibe un correo electrónico con su código QR, que servirá como entrada digital para el evento."
    ),
    (
        "¿Ofrecen servicios adicionales para eventos?",
        "Sí, ofrecemos servicio de staff para el escaneo de códigos QR generados en la compra, creando una logística de entrada eficiente. También contamos con servicio de alquiler de verifones para venta de puerta y bares. Puedo ponerte en contacto con nuestro equipo especializado para más detalles."
    ),
    
    # Reembolsos y cancelaciones
    (
        "¿Cómo solicito un reembolso?",
        "Para solicitar un reembolso, por favor envía todos los datos relacionados a tu orden (nombre, correo, número de orden) al correo electrónico info@tix.do."
    ),
    (
        "Compré un seguro, ¿cómo pido reembolso?",
        "Para el reembolso de una orden asegurada debes enviarnos una constancia de la razón vía correo electrónico a info@tix.do.\n\nLa misma debe estar contemplada dentro de nuestros términos y condiciones: https://tix.do/asegura-tu-compra\n\nEl proceso de reembolso tarda de 10-15 días hábiles (sujeto a tiempos bancarios) y solo se realizará al método de pago original de la compra.\n\nLos cargos por servicios no son reembolsables en ningún caso."
    ),
    (
        "Quiero una devolución",
        "Para solicitar una devolución, por favor envía al correo electrónico info@tix.do todos los datos relacionados a tu orden, como el nombre, el correo y el número de orden. Nuestro equipo revisará tu solicitud según nuestras políticas de devolución."
    ),
    (
        "No puedo asistir al evento",
        "Lamentamos que no puedas asistir. Si adquiriste el seguro de compra, puedes solicitar un reembolso enviando una constancia de la razón a info@tix.do. Si no adquiriste seguro, lamentablemente los boletos no son reembolsables según nuestros términos y condiciones."
    ),
    
    # Datos de contacto 
    (
        "¿Cómo contactarlos?",
        "Puedes contactarnos a través de nuestro correo electrónico info@tix.do o por este mismo canal de WhatsApp. Estamos disponibles para asistirte en lo que necesites."
    ),
    (
        "¿Cuál es su correo electrónico?",
        "Nuestro correo electrónico de contacto es info@tix.do"
    ),
    
    # Preguntas sobre Tix.do
    (
        "¿Qué es Tix.do?",
        "Tix.do es la plataforma líder de venta de entradas y gestión de eventos en República Dominicana. Facilitamos la compra de boletos para conciertos, obras de teatro, eventos deportivos y más."
    ),
    (
        "What is Tix.do?",
        "Tix.do is the leading ticket sales and event management platform in the Dominican Republic. We facilitate the purchase of tickets for concerts, plays, sporting events, and more."
    ),
    
    # Métodos de pago
    (
        "¿Qué métodos de pago aceptan?",
        "En Tix.do aceptamos múltiples formas de pago: tarjetas de crédito/débito (Visa y Mastercard) y transferencias bancarias."
    ),
    (
        "What payment methods do you accept?",
        "At Tix.do we accept multiple payment methods: credit/debit cards (Visa and Mastercard) and bank transfers."
    ),
    
    # Boletos perdidos
    (
        "Perdí mis entradas",
        "¡No te preocupes! Por favor confirma tu correo electrónico y el nombre del evento para poder reenviar tus entradas lo antes posible."
    ),
    (
        "No me llegó el correo con las entradas",
        "Lamento que no hayas recibido tus entradas. Por favor, comparte conmigo tu nombre completo, correo electrónico y el número de orden para poder verificar el estado de tu compra y reenviar las entradas si es necesario."
    ),
    
    # Preguntas sobre el bot
    (
        "¿Quién eres tú?",
        "¡Hola! Soy Camile, la asistente virtual de Tix.do. Estoy aquí para ayudarte con preguntas sobre eventos, entradas y más. Si necesitas hablar con un agente humano, solo dímelo y te conectaré con nuestro equipo de servicio al cliente."
    ),
    (
        "Who are you?",
        "Hello! I'm Camile, the virtual assistant for Tix.do. I'm here to help you with questions about events, tickets, and more. If you need to talk to a human agent, just let me know and I'll connect you with our customer service team."
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
        is_spanish_question = "¿" in question or any(word in question.lower() for word in ["hola", "gracias", "como", "qué", "cómo", "buenas"])
        
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
    confidence_threshold = 0.5  # Umbral para considerar una respuesta válida
    
    return best_match, best_score if best_score >= confidence_threshold else (None, 0.0)