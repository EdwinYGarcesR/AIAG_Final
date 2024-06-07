import os

from chains.course_cypher_chain import course_cypher_chain
from chains.course_review_chain import reviews_vector_chain
from langchain import hub
from langchain.agents import AgentExecutor, Tool, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from tools.wait_times import (
    get_current_wait_times,
    get_most_available_course,
)

COURSE_AGENT_MODEL = os.getenv("COURSE_AGENT_MODEL")

course_agent_prompt = hub.pull("hwchase17/openai-functions-agent")

tools = [
    Tool(
        name="Experiences",
        func=reviews_vector_chain.invoke,
        description="""Útil cuando necesitas responder preguntas
        sobre las experiencias de los estudiantes, opiniones, u otras
        preguntas cualitativas que puedan responderse sobre un curso
        usando búsqueda semántica. No es útil para responder preguntas
        objetivas que involucren contar, porcentajes, agregaciones o
        listar hechos. Usa todo el mensaje como entrada para la herramienta.
        Por ejemplo, si el mensaje es "¿Están satisfechos los estudiantes con
        este curso?", la entrada debe ser "¿Están satisfechos los estudiantes
        con este curso?".
        """,
    ),
    Tool(
        name="Graph",
        func=course_cypher_chain.invoke,
        description="""Útil para responder preguntas sobre cursos,
        instructores, plataformas de cursos, estadísticas de revisiones
        de cursos y detalles de inscripción. Usa todo el mensaje
        como entrada para la herramienta. Por ejemplo, si el mensaje es
        "¿Cuántos estudiantes están inscritos en este curso?", la entrada
        debe ser "¿Cuántos estudiantes están inscritos en este curso?".
        """,
    )
]

chat_model = ChatOpenAI(
    model=COURSE_AGENT_MODEL,
    temperature=0,
)

course_rag_agent = create_openai_functions_agent(
    llm=chat_model,
    prompt=course_agent_prompt,
    tools=tools,
)

course_rag_agent_executor = AgentExecutor(
    agent=course_rag_agent,
    tools=tools,
    return_intermediate_steps=True,
    verbose=True,
)
