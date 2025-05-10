import openai
import os
import json
from typing import Dict, List, Tuple, Optional
from bot.knowledge_base import FAQS, find_best_faq_match
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
    
    def __init__(self, name: str, persona: Dict[str, str], default_language: str = "es"):
        """
        Inicializa el asistente virtual.
        
        Args:
            name: Nombre del asistente
            persona: Descripción de la personalidad en diferentes idiomas
            default_language: Idioma predeterminado ("es" o "en")
        """
        self.name = name
        self.persona = persona
        self.default_language = default_language
        self.conversation_history: List[Dict[str, str]] = []
        
    def get_welcome_message(self, language: Optional[str] = None) -> str:
        """
        Devuelve el mensaje de bienvenida del bot.
        
        Args:
            language: Código de idioma ("es" o "en")
            
        Returns:
            Mensaje de bienvenida formateado
        """
        lang = language or self.default_language
        return WELCOME_MESSAGES.get(lang, WELCOME_MESSAGES["es"])
    
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
        lang = language or self.default_language
        
        self.conversation_history.append({"role": "user", "content": user_message})
        
        if self._check_for_human_handoff_request(user_message, lang):
            response = HUMAN_HANDOFF_MESSAGES.get(lang, HUMAN_HANDOFF_MESSAGES["es"])
            self.conversation_history.append({"role": "assistant", "content": response})
            return response

        faq_match_confidence = find_best_faq_match(user_message, lang)
        print(f"DEBUG - faq_match_confidence: {faq_match_confidence}")

        if isinstance(faq_match_confidence, tuple):
            faq_match, confidence = faq_match_confidence
            if isinstance(confidence, tuple):
                confidence = confidence[0] if confidence else 0.0
        else:
            faq_match, confidence = None, 0.0

        if faq_match and isinstance(confidence, float) and confidence > 0.7:
            response = faq_match
            self.conversation_history.append({"role": "assistant", "content": response})
            return response

        simple_responses = {
            "es": {
                "hola": "¡Klk! ¿En qué puedo ayudarte hoy con Tix.do?",
                "gracias": "¡De nada! Estoy aquí para ayudarte con todo lo relacionado a Tix.do.",
                "adios": "¡Chao! Gracias por usar Tix-o-bot. ¡Que disfrutes tus eventos!",
                "ayuda": "Puedo ayudarte con información sobre eventos, entradas, reembolsos y más. ¿Qué necesitas saber?",
                "evento": "Tix.do tiene muchos eventos increíbles. ¿Buscas algo específico como conciertos, teatro o deportes?"
            },
            "en": {
                "hello": "Hi there! How can I help you with Tix.do today?",
                "thanks": "You're welcome! I'm here to help with all things Tix.do.",
                "bye": "Goodbye! Thanks for using Tix-o-bot. Enjoy your events!",
                "help": "I can help you with information about events, tickets, refunds and more. What do you need to know?",
                "event": "Tix.do has many amazing events. Are you looking for something specific like concerts, theater, or sports?"
            }
        }
        
        message_lower = user_message.lower()
        for keyword, response in simple_responses.get(lang, simple_responses["es"]).items():
            if keyword in message_lower:
                self.conversation_history.append({"role": "assistant", "content": response})
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
                self.conversation_history.append({"role": "assistant", "content": bot_response})
                return bot_response

            except Exception as e:
                print(f"Error al generar respuesta con OpenAI: {str(e)}")

        generic_responses = FALLBACK_MESSAGES.get(lang, FALLBACK_MESSAGES["es"])
        selected_response = generic_responses[len(user_message) % len(generic_responses)]

        self.conversation_history.append({"role": "assistant", "content": selected_response})
        return selected_response
