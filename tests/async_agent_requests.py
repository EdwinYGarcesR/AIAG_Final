import asyncio
import time

import httpx

CHATBOT_URL = "http://localhost:8000/course-rag-agent"


async def make_async_post(url, data):
    timeout = httpx.Timeout(timeout=120)
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, timeout=timeout)
        return response


async def make_bulk_requests(url, data):
    tasks = [make_async_post(url, payload) for payload in data]
    responses = await asyncio.gather(*tasks)
    outputs = [r.json()["output"] for r in responses]
    return outputs


questions = [
    "Cuales son los horarios de operacion de la plataforma?",
    "Donde puedo acceder a la plataforma de cursos?",
    "Necesito algun software especial para acceder a los cursos?",
    "Cuales son los requisitos tecnicos para usar la plataforma?",
    "Cuales son las formas de pago aceptadas para inscribirse en un curso?",
    "Puedo cancelar mi inscripcion y obtener un reembolso?",
    "Puedo ver una vista previa de los cursos antes de inscribirme?",
    "Como me inscribo en un curso?",
    "Como se estructuran los cursos?",
    "Como se evalua mi progreso en el curso?",
    "Que sucede si no paso una evaluacion?",
]

request_bodies = [{"text": q} for q in questions]

start_time = time.perf_counter()
outputs = asyncio.run(make_bulk_requests(CHATBOT_URL, request_bodies))
end_time = time.perf_counter()

print(f"Run time: {end_time - start_time} seconds")
