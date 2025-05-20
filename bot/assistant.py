import openai
import os
import json
from typing import Dict, List, Tuple, Optional
from bot.knowledge_base import FAQS, find_best_faq_match
from utils.helpers import send_handoff_email, format_time  # Importamos la nueva función
from config import (
    GPT_MODEL, 
    MAX_TOKENS, 
    TEMPERATURE, 
    WELCOME_MESSAGES,
    FALLBACK_MESSAGES,
    HUMAN_HANDOFF_MESSAGES,
    OPENAI_API_KEY
)

# Asegurar que la API key esté configurada
openai.api_key = OPENAI_API_KEY

class TixOBot:
    """Clase principal del asistente Tix-o-bot."""
    
    def __init__(self, name: str, persona: Dict[str, str], default_language: str = "es", user_id: str = "Anónimo"):
        """
        Inicializa el asistente virtual.
        
        Args:
            name: Nombre del asistente
            persona: Descripción de la personalidad en diferentes idiomas
            default_language: Idioma predeterminado ("es" o "en")
            user_id: Identificador único del usuario (si está disponible)
        """
        self.name = name
        self.persona = persona
        self.default_language = default_language
        self.conversation_history: List[Dict[str, str]] = []
        self.last_response = ""  # Almacenar la última respuesta para evitar duplicados
        self.user_id = user_id
        
    def get_welcome_message(self, language: Optional[str] = None) -> str:
        """
        Devuelve el mensaje de bienvenida del bot.
        
        Args:
            language: Código de idioma ("es" o "en")
            
        Returns:
            Mensaje de bienvenida formateado
        """
        lang = language or self.default_language
        welcome_msg = WELCOME_MESSAGES.get(lang, WELCOME_MESSAGES["es"])
        self.last_response = welcome_msg  # Guardamos el mensaje de bienvenida para evitar duplicados
        return welcome_msg
    
    def _check_for_human_handoff_request(self, message: str, language: str) -> bool:
        """
        Verifica si el usuario está solicitando hablar con un humano.
        
        Args:
            message: Mensaje del usuario
            language: Código de idioma
            
        Returns:
            True si el usuario quiere hablar con un humano
        """
        message = message.lower()
        
        human_keywords = {
            "es": ["agente humano", "persona real", "hablar con alguien", "hablar con una persona", 
                  "representante", "servicio al cliente", "hablar con un humano", "hablar con un agente"],
            "en": ["human agent", "real person", "talk to someone", "talk to a person",
                  "representative", "customer service", "talk to a human", "talk to an agent"]
        }
        
        return any(keyword in message for keyword in human_keywords.get(language, []))
    
    def get_response(self, user_message: str, language: Optional[str] = None) -> str:
        """
        Genera una respuesta basada en el mensaje del usuario.
        
        Args:
            user_message: Mensaje del usuario
            language: Código de idioma ("es" o "en")
            
        Returns:
            Respuesta generada
        """
        # Evitar procesar mensajes vacíos
        if not user_message.strip():
            return ""
            
        lang = language or self.default_language
        
        # Evitar duplicar el último mensaje del usuario si es idéntico
        if self.conversation_history and \
           self.conversation_history[-1].get("role") == "user" and \
           self.conversation_history[-1].get("content") == user_message:
            return self.last_response
            
        self.conversation_history.append({"role": "user", "content": user_message})
        
        if self._check_for_human_handoff_request(user_message, lang):
            # Agregar el mensaje de respuesta para el usuario
            response = HUMAN_HANDOFF_MESSAGES.get(lang, HUMAN_HANDOFF_MESSAGES["es"])
            self.conversation_history.append({"role": "assistant", "content": response})
            self.last_response = response
            
            # Enviar correo de notificación al soporte
            try:
                success, message = send_handoff_email(
                    user_message=user_message,
                    language=lang,
                    conversation_history=self.conversation_history,
                    user_id=self.user_id
                )
                
                if success:
                    print(f"✅ {message}")
                else:
                    print(f"⚠️ {message}")
                    
                # Registrar el intento de notificación en el historial interno (no visible para el usuario)
                notification_status = f"[Sistema: Notificación de handoff {'enviada' if success else 'fallida'} - {format_time()}]"
                self.conversation_history.append({"role": "system", "content": notification_status})
                
            except Exception as e:
                print(f"❌ Error inesperado al procesar la solicitud de handoff: {str(e)}")
                
            return response

        # Evitar buscar coincidencias de FAQ si el mensaje es demasiado similar a la última respuesta del bot
        # para evitar la recursión infinita
        should_check_faq = True
        if self.last_response and user_message.lower() in self.last_response.lower():
            should_check_faq = False
            
        faq_match = None
        confidence = 0.0
        
        if should_check_faq:
            faq_match_confidence = find_best_faq_match(user_message, lang)
            print(f"DEBUG - faq_match_confidence: {faq_match_confidence}")

            if isinstance(faq_match_confidence, tuple):
                faq_match, confidence = faq_match_confidence
                if isinstance(confidence, tuple):
                    confidence = confidence[0] if confidence else 0.0

        if faq_match and isinstance(confidence, float) and confidence > 0.7:
            # Evitar devolver la misma respuesta que acabamos de dar
            if faq_match != self.last_response:
                response = faq_match
                self.conversation_history.append({"role": "assistant", "content": response})
                self.last_response = response
                return response

        simple_responses = {
            "es": {
                "hola": "¡Hola, Gracias por contactarnos!, te asiste Camila. ¿En qué puedo ayudarte hoy con Tix.do?",
                "gracias": "¡De nada! Estoy aquí para ayudarte con todo lo relacionado a Tix.do.",
                "adios": "¡Chao! Gracias por contactarnos. ¡Que disfrutes tus eventos!",
                "ayuda": "Puedo ayudarte con información sobre eventos, entradas, reembolsos y más. ¿Qué necesitas saber?",
                "evento": "Tix.do tiene muchos eventos increíbles. ¿Buscas algo específico como conciertos, teatro o deportes?"
            },
            "en": {
                "hello": "Hi there! How can I help you with Tix.do today?",
                "thanks": "You're welcome! I'm here to help with all things Tix.do.",
                "bye": "Goodbye! Thanks for contacting us. Enjoy your events!",
                "help": "I can help you with information about events, tickets, refunds and more. What do you need to know?",
                "event": "Tix.do has many amazing events. Are you looking for something specific like concerts, theater, or sports?"
            }
        }
        
        message_lower = user_message.lower()
        for keyword, response in simple_responses.get(lang, simple_responses["es"]).items():
            if keyword in message_lower:
                # No repetir la misma respuesta que acabamos de dar
                if response != self.last_response:
                    self.conversation_history.append({"role": "assistant", "content": response})
                    self.last_response = response
                    return response

        if OPENAI_API_KEY and len(OPENAI_API_KEY) > 10:
            try:
                messages = [
                    {"role": "system", "content": self.persona.get(lang, self.persona["es"])}
                ]
                messages.extend(self.conversation_history[-5:])

                response = openai.ChatCompletion.create(
                    model=GPT_MODEL,
                    messages=messages,
                    max_tokens=MAX_TOKENS,
                    temperature=TEMPERATURE,
                )
                bot_response = response.choices[0].message["content"].strip()
                
                # Verificar que no estamos devolviendo la misma respuesta que antes
                if bot_response != self.last_response:
                    self.conversation_history.append({"role": "assistant", "content": bot_response})
                    self.last_response = bot_response
                    return bot_response

            except Exception as e:
                print(f"Error al generar respuesta con OpenAI: {str(e)}")

        generic_responses = FALLBACK_MESSAGES.get(lang, FALLBACK_MESSAGES["es"])
        selected_response = generic_responses[len(user_message) % len(generic_responses)]

        # Asegurarse de no repetir la última respuesta
        if selected_response == self.last_response and len(generic_responses) > 1:
            selected_response = generic_responses[(len(user_message) + 1) % len(generic_responses)]

        self.conversation_history.append({"role": "assistant", "content": selected_response})
        self.last_response = selected_response
        return selected_response