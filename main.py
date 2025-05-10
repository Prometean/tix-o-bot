import streamlit as st
import openai
import os
from datetime import datetime
from bot.assistant import TixOBot
from bot.knowledge_base import FAQS
from config import OPENAI_API_KEY, BOT_NAME, BOT_PERSONA, DEFAULT_LANGUAGE

# Configuración de la API de OpenAI
openai.api_key = OPENAI_API_KEY

# Verificar que la API key esté configurada
if not OPENAI_API_KEY:
    st.error("⚠️ No se ha configurado la API key de OpenAI. Por favor, configura la variable OPENAI_API_KEY en el archivo .env")
    st.stop()

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

# Estilo personalizado
st.markdown("""
    <style>
    .user-avatar {
        background-color: #FF4B4B;
        color: white;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        text-align: center;
        line-height: 40px;
        margin-right: 10px;
    }
    .bot-avatar {
        background-color: #0068C9;
        color: white;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        text-align: center;
        line-height: 40px;
        margin-right: 10px;
    }
    .message-container {
        display: flex;
        margin-bottom: 15px;
    }
    .message-content {
        background-color: #f0f2f6;
        padding: 10px 15px;
        border-radius: 15px;
        max-width: 80%;
        color: #262730;
    }
    /* Mejorar el contraste en general */
    p, div, span, h1, h2, h3, h4, h5, h6 {
        color: #262730;
    }
    /* Estilo para la sección de preguntas frecuentes */
    .streamlit-expanderHeader {
        background-color: #f0f2f6 !important;
        color: #262730 !important;
    }
    </style>
""", unsafe_allow_html=True)

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
        with st.container():
            st.markdown(f"""
            <div class="message-container" style="justify-content: flex-end;">
                <div class="message-content" style="background-color: #e6f7ff;">
                    {message["content"]}
                </div>
                <div class="user-avatar">👤</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        with st.container():
            st.markdown(f"""
            <div class="message-container">
                <div class="bot-avatar">🤖</div>
                <div class="message-content">
                    {message["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)

# Área de entrada de texto
user_input = st.text_input("Escribe tu pregunta aquí:", key="user_input")

# Botón para cambiar idioma
language = st.sidebar.selectbox(
    "Idioma / Language",
    ["Español", "English"],
    index=0 if DEFAULT_LANGUAGE == "es" else 1
)

# Opciones comunes (FAQs) para facilitar la interacción
with st.expander("Preguntas frecuentes"):
    faq_cols = st.columns(2)
    faq_buttons = {}
    
    for i, (question, _) in enumerate(FAQS):
        col_idx = i % 2
        with faq_cols[col_idx]:
            faq_buttons[question] = st.button(question)
            
    for question, is_clicked in faq_buttons.items():
        if is_clicked:
            user_input = question

# Procesar la entrada del usuario
if user_input:
    # Agregar mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Obtener respuesta del bot
    selected_lang = "es" if language == "Español" else "en"
    bot_response = st.session_state.bot.get_response(
        user_input, 
        language=selected_lang
    )
    
    # Agregar respuesta del bot al historial
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    
    # Recargar la página para mostrar los nuevos mensajes
    st.rerun()

# Información adicional en la barra lateral
with st.sidebar:
    st.subheader("Sobre Tix-o-bot")
    st.write("Asistente virtual para Tix.do, la plataforma líder de eventos en República Dominicana.")
    
    st.divider()
    
    st.caption(f"© {datetime.now().year} Tix.do")
    st.caption("Desarrollado por Ean Jimenez")
    
    st.divider()
    
    if st.button("Reiniciar conversación"):
        st.session_state.messages = []
        st.experimental_rerun()