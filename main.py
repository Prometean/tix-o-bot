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
    # Flag para controlar la visualización del mensaje de bienvenida
    st.session_state.welcome_shown = False
    
if "bot" not in st.session_state:
    st.session_state.bot = TixOBot(
        name=BOT_NAME,
        persona=BOT_PERSONA,
        default_language=DEFAULT_LANGUAGE
    )

# Estilo personalizado con mejor contraste y visibilidad
st.markdown("""
    <style>
    /* Estilos generales mejorados para mayor contraste */
    body {
        color: #000000;
        background-color: #ffffff;
    }
    
    /* Avatares */
    .user-avatar {
        background-color: #FF4B4B;
        color: white;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        text-align: center;
        line-height: 40px;
        margin-right: 10px;
        font-weight: bold;
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
        font-weight: bold;
    }
    
    /* Contenedores de mensajes */
    .message-container {
        display: flex;
        margin-bottom: 15px;
        align-items: flex-start;
    }
    
    .message-content {
        background-color: #f0f2f6;
        padding: 12px 18px;
        border-radius: 15px;
        max-width: 80%;
        color: #000000 !important;
        font-size: 16px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Asegurar mejor contraste y visibilidad de texto */
    .message-content p, 
    .message-content div, 
    .message-content span {
        color: #000000 !important;
        font-weight: normal;
        font-size: 16px;
        line-height: 1.5;
    }
    
    /* Estilo para títulos y texto general */
    h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
        font-weight: bold;
    }
    
    p, div, span {
        color: #000000 !important;
    }
    
    /* Estilo para la sección de preguntas frecuentes */
    .streamlit-expanderHeader {
        background-color: #e6e6e6 !important;
        color: #000000 !important;
        font-weight: bold !important;
        padding: 10px !important;
    }
    
    /* Botones con mejor contraste */
    button, .stButton>button {
        color: #000000 !important;
        font-weight: 600 !important;
        background-color: #e6e6e6 !important;
        border: 1px solid #0068C9 !important;
        padding: 8px 16px !important;
    }
    
    button:hover, .stButton>button:hover {
        background-color: #d1d1d1 !important;
    }
    
    /* Inputs con mejor contraste */
    input, .stTextInput>div>div>input {
        color: #000000 !important;
        font-weight: normal !important;
        background-color: white !important;
        border: 1px solid #cccccc !important;
        padding: 10px !important;
        font-size: 16px !important;
    }
    
    /* Fondo general mejorado */
    .main .block-container {
        background-color: white !important;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Título del asistente
st.title(f"🎫 {BOT_NAME}")
st.caption("Asistente virtual de Tix.do - Tu acompañante para eventos")

# Mensaje de bienvenida - Solo se muestra una vez y se controla con el flag
if not st.session_state.messages and not st.session_state.welcome_shown:
    welcome_message = st.session_state.bot.get_welcome_message()
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})
    st.session_state.welcome_shown = True

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

# Definir callback para el envío del formulario
def submit_message():
    user_message = st.session_state.user_input
    if user_message.strip():  # Asegurarse de que el mensaje no esté vacío
        # Agregar mensaje del usuario al historial
        st.session_state.messages.append({"role": "user", "content": user_message})
        
        # Obtener respuesta del bot
        selected_lang = "es" if st.session_state.language == "Español" else "en"
        bot_response = st.session_state.bot.get_response(
            user_message,
            language=selected_lang
        )
        
        # Agregar respuesta del bot al historial
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
        # No intentamos limpiar el input aquí, ya que causa un error
        # Streamlit maneja esto automáticamente con clear_on_submit=True

# Guardar el idioma seleccionado en el estado de la sesión
if "language" not in st.session_state:
    st.session_state.language = "Español" if DEFAULT_LANGUAGE == "es" else "English"

# Configuración del formulario para capturar la entrada del usuario
with st.form(key="message_form", clear_on_submit=True):
    # Usar st.session_state para mantener el valor del input
    st.text_input(
        "Escribe tu pregunta aquí:",
        key="user_input"
    )
    
    # Botones del formulario
    col1, col2 = st.columns([4, 1])
    with col1:
        submit_button = st.form_submit_button(label="Enviar", on_click=submit_message)
    with col2:
        clear_button = st.form_submit_button(label="Limpiar")
    
    # Ya no necesitamos esta lógica, la manejamos con on_click y clear_on_submit
    # if submit_button:
    #     submit_message()
    
    if clear_button:
        # No intentamos modificar directamente el valor
        st.session_state.messages = st.session_state.messages  # Truco para forzar un rerender

# Botón para cambiar idioma en la barra lateral
with st.sidebar:
    selected_language = st.selectbox(
        "Idioma / Language",
        ["Español", "English"],
        index=0 if st.session_state.language == "Español" else 1,
        key="language_selector"
    )
    
    # Actualizar el idioma en el estado de la sesión
    st.session_state.language = selected_language

# Opciones comunes (FAQs) para facilitar la interacción
with st.expander("Preguntas frecuentes"):
    faq_cols = st.columns(2)
    
    for i, (question, _) in enumerate(FAQS):
        col_idx = i % 2
        with faq_cols[col_idx]:
            if st.button(question, key=f"faq_{i}"):
                # Agregar la pregunta al historial
                st.session_state.messages.append({"role": "user", "content": question})
                
                # Obtener la respuesta del bot
                selected_lang = "es" if st.session_state.language == "Español" else "en"
                bot_response = st.session_state.bot.get_response(
                    question,
                    language=selected_lang
                )
                
                # Agregar la respuesta al historial
                st.session_state.messages.append({"role": "assistant", "content": bot_response})

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
        st.session_state.welcome_shown = False  # Resetear también el flag de bienvenida