import os

import requests
import streamlit as st

CHATBOT_URL = os.getenv(
    "CHATBOT_URL", "http://localhost:8000/cursos-rag-agent"
)

with st.sidebar:
    st.header("About")
    st.markdown(
        """
        Este chatbot interactúa con un
        [agente de LangChain](https://python.langchain.com/docs/get_started/introduction)
        diseñado para responder preguntas sobre los cursos, estudiantes,
        inscripciones, instructores y plataformas en un sistema de cursos en línea ficticio.
        El agente utiliza generación aumentada por recuperación (RAG) sobre datos
        estructurados y no estructurados que han sido generados sintéticamente.
        """
    )

    st.header("Preguntas comunes")
    st.markdown("- Cuales son los horarios de operacion de la plataforma?")
    st.markdown(
        """- Donde puedo acceder a la plataforma de cursos?"""
    )
    st.markdown(
        """- Necesito algun software especial para acceder a los cursos?
"""
    )
    st.markdown(
        "- Cuales son los requisitos tecnicos para usar la plataforma?"
    )
    st.markdown(
        """- Cuales son las formas de pago aceptadas para inscribirse en un curso?"""
    )
    st.markdown(
        "- Puedo cancelar mi inscripcion y obtener un reembolso?"
    )
    st.markdown("- Puedo ver una vista previa de los cursos antes de inscribirme?")
    st.markdown(
        "- Como me inscribo en un curso?"
    )
    st.markdown("- Como se estructuran los cursos?")
    st.markdown(
        """- Como se evalua mi progreso en el curso?"""
    )
    st.markdown(
        "- Que sucede si no paso una evaluacion?"
    )


st.title("Plataforma de cursos online - Chatbot")
st.info(
    """¡Hazme preguntas sobre estudiantes, inscripciones, plataformas de cursos, 
    instructores, cursos, evaluaciones y tiempos de espera!"""
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "output" in message.keys():
            st.markdown(message["output"])

        if "explanation" in message.keys():
            with st.status("How was this generated", state="complete"):
                st.info(message["explanation"])

if prompt := st.chat_input("What do you want to know?"):
    st.chat_message("user").markdown(prompt)

    st.session_state.messages.append({"role": "user", "output": prompt})

    data = {"text": prompt}

    with st.spinner("Searching for an answer..."):
        response = requests.post(CHATBOT_URL, json=data)

        if response.status_code == 200:
            output_text = response.json()["output"]
            explanation = response.json()["intermediate_steps"]

        else:
            output_text = """An error occurred while processing your message.
            Please try again or rephrase your message."""
            explanation = output_text

    st.chat_message("assistant").markdown(output_text)
    st.status("How was this generated?", state="complete").info(explanation)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "output": output_text,
            "explanation": explanation,
        }
    )
