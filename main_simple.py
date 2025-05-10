import streamlit as st
import openai
import os
from datetime import datetime
from bot.assistant import TixOBot
from bot.knowledge_base import FAQS
from config import OPENAI_API_KEY, BOT_NAME, BOT_PERSONA, DEFAULT_LANGUAGE

# Configuración de la API de OpenAI
openai.api_key = OPENAI_API_KEY

# Configuración de la página
st.set_page_config(
    page_title=f"{BOT_NAME} | Asistente Virtual de Tix.do",
    page_icon="🎫",
    layout="centered"
)

# Inicialización del estado de la sesión
if "messages" not in st.session_state:
    st.session_state.messages = []

if "bot" not in st.session_state:
    st.session_state.bot = TixOBot(
        name=BOT_NAME,
        persona=BOT_PERSONA,
        default_language=DEFAULT_LANGUAGE
    )

# Título del asistente
st.title(f"🎫 {BOT_NAME}")
st.caption("Asistente virtual de Tix.do - Tu acompañante para eventos")

# Mensaje de bienvenida
if not st.session_state.messages:
    welcome_message = st.session_state.bot.get_welcome_message()
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})

# Mostrar historial de mensajes
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"**Usuario:** {message['content']}")
    else:
        st.markdown(f"**{BOT_NAME}:** {message['content']}")
    st.markdown("---")

# Sidebar para cambio de idioma
language = st.sidebar.selectbox(
    "Idioma / Language",
    ["Español", "English"],
    index=0 if DEFAULT_LANGUAGE == "es" else 1
)

# Opciones comunes (FAQs)
with st.expander("Preguntas frecuentes"):
    faq_cols = st.columns(2)
    faq_buttons = {}

    for i, (question, _) in enumerate(FAQS):
        col_idx = i % 2
        with faq_cols[col_idx]:
            faq_buttons[question] = st.button(question)

    for question, is_clicked in faq_buttons.items():
        if is_clicked:
            st.session_state.user_input = question

# Área de entrada de texto
user_input = st.text_input("Escribe tu pregunta aquí:", key="user_input")
submit_button = st.button("Enviar")

# Procesar entrada del usuario (solo al presionar botón)
if submit_button and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    selected_lang = "es" if language == "Español" else "en"
    bot_response = st.session_state.bot.get_response(
        user_input, 
        language=selected_lang
    )

    st.session_state.messages.append({"role": "assistant", "content": bot_response})

    st.rerun()

# Información adicional en sidebar
with st.sidebar:
    st.subheader("Sobre Tix-o-bot")
    st.write("Asistente virtual para Tix.do, la plataforma líder de eventos en República Dominicana.")

    st.divider()

    st.caption(f"© {datetime.now().year} Tix.do")
    st.caption("Desarrollado por Ean Jimenez")

    st.divider()

    if st.button("Reiniciar conversación"):
        st.session_state.messages = []
        st.rerun()
