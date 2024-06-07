# Chatbot de revisión de cursos en línea

Este repositorio contiene un chatbot RAG (generación aumentada de recuperación) creado con LangChain y Neo4j para responder preguntas sobre cursos en línea, y temas relacionados con el funcionamiento de la plataforma.
Trabajo realizado por:
 - Edwin Yahir Garcés Romero
 - Edwin Espinoza Jiménez

Universidad del Cauca - Electiva: Aplicación de Inteligencia Artificial Generativa

## Tabla de contenido
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del proyecto](#estructura-proyecto)

## Instalación

### Requisitos previos
- Python 3.10+
- Docker and Docker Compose
- Base de datos en grfo - Neo4J (Base de datos ya prevista para la ejecución)
- Clave API de OpenAI

### Configuración del proyecto
1. **Clonar el repositorio:**
2. **Crea un entorno virtual:**
 ```sh
 Python -m venv venv
 ```
3. **Instalar las dependencias:**
```sh
    pip install -r requirements.txt
```

4. **Configurar variables de entorno:**
En caso dde que no aparezcan, Cree un archivo `.env` en el directorio raíz y agregue las siguientes variables:
 ```entorno
 OPENAI_API_KEY=tu_llave_api_openai
 NEO4J_URI=tu_neo4j_uri
 NEO4J_USERNAME=tu_nombre_de_usuario_neo4j
 NEO4J_PASSWORD=tu_contraseña_neo4j
 ```

## Uso

1. **Ejecute el chatbot:**
Con Docker ejecutado, hay que abrir una terminal y ejecutar:
```sh
    docker-compose up --buil
```

2. **Interactuar con el chatbot:**
Empiece a hacer preguntas sobre los cursos, reseñas o cualquier información relacionada.
Puede consultar la base de datos para analizar las respuestas según los datos.

## Estructura del proyecto - 3 módulos
- Chatbot_api --- Contiene la lógica del chatbot, incluído el funcionamiento de cadenas
- Chatbot frontend --- Interfaz del chatbot
- Course Neo4j --- Carga de la base de datos a Neo4j
