import streamlit as st
from google.generativeai import configure, GenerativeModel

# Configuración de la página
st.set_page_config(page_title="NutriBot Personal", page_icon="🍎")
st.title("🍎 Tu Asistente de Nutrición")

# 1. Configurar la IA (Aquí pondrías tu API Key)
# Para pruebas locales puedes usar: configure(api_key="TU_API_KEY")
# En Streamlit Cloud se usa st.secrets["GOOGLE_API_KEY"]
configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = GenerativeModel('gemini-pro')

# 2. Definir la PERSONALIDAD (System Instruction)
PERSONALIDAD = (
    "Eres un asistente de nutrición amigable, motivador y con chispa. "
    "Tu objetivo es ayudar a contar calorías y dar consejos saludables. "
    "Usa un lenguaje cercano, pero profesional. Si te preguntan algo que no sea "
    "de nutrición o salud, di que prefieres enfocarte en sus metas de bienestar."
)

# 3. Inicializar el historial del chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes previos
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Lógica de interacción
if prompt := st.chat_input("¿Qué comiste hoy?"):
    # Mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar respuesta con personalidad
    with st.chat_message("assistant"):
        # Combinamos la personalidad con la pregunta del usuario
        full_prompt = f"{PERSONALIDAD}\n\nUsuario: {prompt}\nAsistente:"
        response = model.generate_content(full_prompt)
        
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})