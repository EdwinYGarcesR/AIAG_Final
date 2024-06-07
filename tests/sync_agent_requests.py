import time

import requests

CHATBOT_URL = "http://localhost:8000/course-rag-agent"

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
outputs = [requests.post(CHATBOT_URL, json=data) for data in request_bodies]
end_time = time.perf_counter()

print(f"Run time: {end_time - start_time} seconds")
