import streamlit as st
from openai import OpenAI

# CONFIGURACIÓN DE BIENVENIDA PERSONALIZADA
st.set_page_config(page_title="Chatbot Matemáticas UNAL", page_icon="📚")

# TÍTULO Y BIENVENIDA PERSONALIZADA
st.title("📚 Chatbot Oficial - Departamento de Matemáticas UNAL")

# ESTE ES EL MENSAJE DE BIENVENIDA QUE PIDES
st.markdown("""
### 🎓 ¡Bienvenido al chatbot oficial del Departamento de Matemáticas de la UNAL!

Soy tu asistente virtual especializado en ayudarte con:
- 📋 Trámites académicos y administrativos
- 📝 Inscripciones a cursos de matemáticas
- 📄 Solicitud de certificados y constancias
- ❓ Preguntas frecuentes sobre el departamento
- 📅 Información sobre horarios y profesores
- 🏢 Ubicación y contactos del departamento

**¿En qué puedo ayudarte hoy?** 
""")

# Información adicional en la barra lateral
with st.sidebar:
    st.header("ℹ️ Información del Departamento")
    st.info(
        """
        **Departamento de Matemáticas UNAL**
        - 📍 Edificio 404, Oficina 201
        - 📞 Teléfono: (601) 3165000 ext. 16000
        - 📧 Email: decanatura_matematicas@unal.edu.co
        - 🕒 Horario: Lunes a Viernes 8am - 5pm
        """
    )
    
    st.header("🔧 Configuración")
    # Aquí puedes agregar opciones de configuración si lo deseas

# Configuración de la API Key (puedes guardarla en secrets.toml para no pedirla siempre)
# Por ahora, mantendremos la opción de ingresarla manualmente
openai_api_key = st.text_input("🔑 OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Por favor, ingresa tu API key de OpenAI para continuar.", icon="🗝️")
    st.stop()

# Crear el cliente de OpenAI
client = OpenAI(api_key=openai_api_key)

# Inicializar el historial de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = [
        # Mensaje de sistema para enfocar el comportamiento del chatbot
        {"role": "system", "content": """
        Eres un asistente virtual especializado del Departamento de Matemáticas de la UNAL.
        Tu función es ayudar a estudiantes con trámites administrativos y consultas académicas.
        
        Información importante que debes conocer:
        - El departamento ofrece cursos de: Cálculo, Álgebra Lineal, Ecuaciones Diferenciales, etc.
        - Trámites comunes: inscripción de asignaturas, solicitud de certificados, justificaciones, etc.
        - Horario de atención: Lunes a Viernes 8am - 5pm
        - Ubicación: Edificio 404, Oficina 201
        
        IMPORTANTE: Responde SIEMPRE en español, de manera amable y profesional.
        Si no sabes algo, sugiere al estudiante contactar directamente al departamento.
        """}
    ]

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    if message["role"] != "system":  # No mostrar el mensaje de sistema
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Área de entrada del usuario
if prompt := st.chat_input("Escribe tu consulta aquí..."):

    # Agregar mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar respuesta de OpenAI (sin incluir el mensaje de sistema en el historial visible)
    messages_for_api = [st.session_state.messages[0]] + st.session_state.messages[1:]
    
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages_for_api,
        stream=True,
        temperature=0.7,  # Controla la creatividad de las respuestas
    )

    # Mostrar y guardar la respuesta
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Agregar algunos botones de ayuda rápida (opcional)
st.divider()
st.caption("**Consultas rápidas:**")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📋 ¿Cómo inscribir un curso?"):
        st.session_state.messages.append({"role": "user", "content": "¿Cómo inscribir un curso de matemáticas?"})
        st.rerun()
with col2:
    if st.button("📄 Solicitar certificado"):
        st.session_state.messages.append({"role": "user", "content": "¿Cómo solicito un certificado?"})
        st.rerun()
with col3:
    if st.button("📍 ¿Dónde está el departamento?"):
        st.session_state.messages.append({"role": "user", "content": "¿Dónde está ubicado el departamento?"})
        st.rerun()
