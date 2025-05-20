# Tix-o-bot

Asistente virtual inteligente para la plataforma de eventos [Tix.do](https://tix.do), desarrollado por Ean Jimenez.

## Objetivo

Automatizar la atención al cliente de Tix.do a través de un agente conversacional multicanal, con lenguaje natural adaptado al público joven dominicano. El bot responde consultas frecuentes sobre eventos, pagos, reembolsos y más, con un tono casual y profesional.

---

## Propiedad del Código

Todo el código de este repositorio es propiedad de Tix.do. Este desarrollo se realiza de forma independiente, bajo contrato personal con Ean Jimenez.

---

## Fases del Proyecto

1. **Branding del bot y configuración base** ✅
2. **Entrenamiento con FAQs y ajustes conversacionales** ✅
3. **Desarrollo de interfaz e integración web** *(en curso)*
4. **Pruebas funcionales y ajustes**
5. **Entrega final y soporte post-implementación**

---

## Funcionalidades Principales

* Procesamiento de preguntas frecuentes (FAQs)
* Respuestas naturales en español o inglés, tono casual y profesional
* Soporte automatizado 24/7
* Escalamiento simulado a agente humano
* Interfaz embebible en sitio web

---

## Funcionalidades Adicionales (planificadas)

* Conexión con API de eventos
* Validación de códigos de ticket
* Reenvío automatizado de entradas
* Automatización de correos personalizados
* Soporte multicanal (WhatsApp, Instagram, correo)
* Análisis de sentimiento
* Reportes automáticos
* Entrenamiento personalizado por canal o audiencia

---

## Estado Actual

* Fase actual: **Desarrollo de interfaz e integración web**
* Entorno de desarrollo: **GitHub / Streamlit Cloud**
* Fecha de inicio: Mayo-09-2025

---

## Tecnologías

* Python
* Streamlit (versión gratuita temporal)
* OpenAI GPT-3.5 (API comercial)
* GitHub (código fuente y control de versiones)
* Replit (opcional para prototipado rápido)

---

## Estructura del Proyecto

```
📁 tix-o-bot/
├── .streamlit/              # Configuración de Streamlit
│   └── config.toml
├── bot/                     # Lógica del asistente
│   ├── __init__.py
│   ├── assistant.py         # Clase principal del bot Camile
│   └── knowledge_base.py    # Base de preguntas frecuentes
├── utils/                   # Funciones auxiliares
│   ├── __init__.py
│   └── helpers.py
├── venv/                    # Entorno virtual (excluido del repo)
├── .env                     # Variables de entorno locales
├── .env copy.example        # Plantilla de configuración de entorno
├── .gitignore
├── config.py                # Configuraciones globales del bot
├── main.py                  # Entrada principal (Streamlit UI)
├── main_simple.py           # Versión simple del bot (modo demo)
├── test_bot.py              # Script de prueba en consola
├── requirements.txt         # Dependencias del proyecto
├── requirements-alt.txt     # Alternativa para entornos distintos
└── README.md                # Este documento
```

---

## Licencia

Este proyecto es de uso exclusivo de Tix.do. No se permite su redistribución ni uso comercial fuera de este alcance.

---

## Contacto

Desarrollado por Ean Jimenez
Contacto: [ean.jimenez97@gmail.com](mailto:ean.jimenez97@gmail.com)

---

## Archivos Clave

### main.py

Interfaz en Streamlit que conecta con el bot y permite chatear en tiempo real.

### test\_bot.py

Script para validar respuestas del bot desde consola.

### config.py

Define idioma, nombre del bot, API Key de OpenAI, mensajes predefinidos y personalidad.

### requirements.txt

```
streamlit
openai
tenacity
python-dotenv
```

### .env copy.example

```bash
OPENAI_API_KEY=sk-...
DEFAULT_LANGUAGE=es
```
