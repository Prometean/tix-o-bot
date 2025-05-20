from bot.assistant import TixOBot
from config import BOT_NAME, BOT_PERSONA, DEFAULT_LANGUAGE

# Instancia del bot
bot = TixOBot(name=BOT_NAME, persona=BOT_PERSONA, default_language=DEFAULT_LANGUAGE)

# Conversaciones de prueba
test_inputs = [
    "Hola, quien eres?",
    "Como puedo comprar entradas?",
    "Perdi mis boletos",
    "Quiero hablar con una persona real",
    "What is Tix.do?",
    "How can I buy tickets?",
    "Thanks",
    "Help",
    "Chao"
]

for question in test_inputs:
    response = bot.get_response(question)
    print(f"Usuario: {question}")
    print(f"Camile: {response}")
    print("-" * 60)