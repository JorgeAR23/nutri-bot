import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="NutriBot - Tu coach inteligente",
    page_icon="🍎",
    layout="centered"
)


# --- CONFIGURACIÓN DE LA IA ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Configuramos el modelo
    model = genai.GenerativeModel('gemini-3-flash-preview')
except Exception as e:
    st.error("⚠️ Error: No se encontró la configuración de la API Key. Verifica tu archivo secrets.toml.")
    st.stop()

# --- DEFINICIÓN DE LA PERSONALIDAD ---
# Este es el "System Prompt" que guía el comportamiento de la IA
PERSONALIDAD = """
Eres un asistente de nutrición experto, pero con una personalidad muy humana, empática y motivadora. 
No eres una máquina rígida; hablas como un coach que se preocupa por el usuario.

Reglas de comportamiento:
1. Siempre saluda de forma amable y usa emojis relacionados con comida saludable.
2. Si el usuario te cuenta lo que comió, intenta estimar calorías o beneficios nutricionales de forma conversacional.
3. Si el usuario se siente desanimado, dale palabras de aliento.
4. MUY IMPORTANTE: Si el usuario pregunta cosas que no tienen NADA que ver con nutrición, salud, ejercicio o bienestar (como política, programación o chismes), responde con humor que tu cerebro solo está programado para hablar de comida y salud, y redirige la charla.
5. Mantén un tono balanceado: no prohíbas alimentos, fomenta el equilibrio.
"""

# --- INICIALIZACIÓN DEL HISTORIAL ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! Soy tu asistente de nutrición. 🍎 ¿Qué tal estuvo tu comida de hoy? Cuéntame y te ayudo a balancear el día."}
    ]

# --- RENDERIZADO DEL CHAT ---
st.title("🍎 NutriBot")
st.caption("Tu compañero inteligente para una vida más sana")

# Mostramos los mensajes almacenados
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- LÓGICA DE ENTRADA DE USUARIO ---
if prompt := st.chat_input("Escribe aquí (ej: ¿Cuánta proteína tiene un huevo?)"):
    
    # 1. Agregar y mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generar respuesta de la IA
    with st.chat_message("assistant"):
        message_placeholder = st.empty() # Para efecto de carga
        
        try:
            # Construimos el contexto completo para la IA
            # Enviamos la personalidad + el historial + la pregunta actual
            historial_contexto = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
            full_query = f"{PERSONALIDAD}\n\nHistorial de la charla:\n{historial_contexto}\n\nAsistente:"
            
            response = model.generate_content(full_query)
            full_response = response.text
            
            # Mostramos la respuesta
            message_placeholder.markdown(full_response)
            
            # Guardamos en el historial
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Hubo un error al procesar tu mensaje: {e}")