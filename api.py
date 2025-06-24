import streamlit as st
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from bot.assistant import TixOBot
from config import OPENAI_API_KEY, BOT_NAME, BOT_PERSONA, DEFAULT_LANGUAGE

# Initialize FastAPI
app = FastAPI(
    title="Tix-o-bot API",
    description="API REST sencilla para chatbot para Tix.do",
    version="1.0.0"
)

# FastAPI models
class ChatRequest(BaseModel):
    message: str
    user_id: str = None
    language: str = "es"

class ChatResponse(BaseModel):
    response: str
    bot_name: str
    language_used: str
    timestamp: str

# Token for simple authentication
API_TOKEN = "tixdo_secure_token"

async def verify_token(authorization: str = Header(...)):
    token_type, _, token = authorization.partition(" ")
    if token_type.lower() != "bearer" or token != API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid or missing token")

@app.post("/api/chat", response_model=ChatResponse, dependencies=[Depends(verify_token)])
async def chat_endpoint(chat_request: ChatRequest):
    selected_lang = chat_request.language
    bot = TixOBot(name=BOT_NAME, persona=BOT_PERSONA, default_language=DEFAULT_LANGUAGE)
    response = bot.get_response(chat_request.message, language=selected_lang)

    return ChatResponse(
        response=response,
        bot_name=BOT_NAME,
        language_used=selected_lang,
        timestamp=datetime.utcnow().isoformat() + "Z"
    )

# Streamlit UI starts here
if not OPENAI_API_KEY:
    st.error("⚠️ No se ha configurado la API key de OpenAI. Por favor, configura la variable OPENAI_API_KEY en el archivo .env")
    st.stop()

st.set_page_config(
    page_title=f"{BOT_NAME} | Asistente Virtual de Tix.do",
    page_icon="🎫",
    layout="centered"
)

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.welcome_shown = False

if "bot" not in st.session_state:
    st.session_state.bot = TixOBot(
        name=BOT_NAME,
        persona=BOT_PERSONA,
        default_language=DEFAULT_LANGUAGE
    )

st.title(f"🎫 {BOT_NAME}")
st.caption("Asistente virtual de Tix.do - Tu acompañante para eventos")

if not st.session_state.messages and not st.session_state.welcome_shown:
    welcome_message = st.session_state.bot.get_welcome_message()
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})
    st.session_state.welcome_shown = True

for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🤖"
    alignment = "flex-end" if message["role"] == "user" else "flex-start"
    bg_color = "#c0c9cd" if message["role"] == "user" else "#000000"
    with st.container():
        st.markdown(f"""
        <div class="message-container" style="justify-content: {alignment};">
            <div class="message-content" style="background-color: {bg_color};">{message["content"]}</div>
            <div class="{'user-avatar' if avatar == '👤' else 'bot-avatar'}">{avatar}</div>
        </div>
        """, unsafe_allow_html=True)

def submit_message():
    user_message = st.session_state.user_input
    if user_message.strip():
        st.session_state.messages.append({"role": "user", "content": user_message})
        selected_lang = "es" if st.session_state.language == "Español" else "en"
        bot_response = st.session_state.bot.get_response(user_message, language=selected_lang)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

with st.form(key="message_form", clear_on_submit=True):
    st.text_input("Escribe tu pregunta aquí:", key="user_input")
    col1, col2 = st.columns([4, 1])
    with col1:
        st.form_submit_button(label="Enviar", on_click=submit_message)
    with col2:
        if st.form_submit_button(label="Limpiar"):
            st.session_state.messages = []
            st.session_state.welcome_shown = False

with st.sidebar:
    selected_language = st.selectbox("Idioma / Language", ["Español", "English"], index=0 if DEFAULT_LANGUAGE == "es" else 1)
    st.session_state.language = selected_language
    st.subheader("Sobre Tix-o-bot")
    st.write("Asistente virtual para Tix.do, la plataforma líder de eventos en República Dominicana.")
    st.divider()
    st.caption(f"© {datetime.now().year} Tix.do")
    st.caption("Desarrollado por Ean Jimenez")
    st.divider()
    if st.button("Reiniciar conversación"):
        st.session_state.messages = []
        st.session_state.welcome_shown = False
