# Chatbot de revisión de cursos en línea

Este repositorio contiene un chatbot RAG (generación aumentada de recuperación) creado con LangChain y Neo4j para responder preguntas sobre cursos en línea, y temas relacionados con el funcionamiento de la plataforma.
Trabajo realizado por:
 - Edwin Yahir Garcés Romero
 - Edwin Espinoza Jiménez

Universidad del Cauca - Electiva: Aplicación de Inteligencia Artificial Generativa

## Tabla de contenido
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Documentación](#documentación)

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

## Estructura del proyecto
Construcción mediante 3 módulos:
- Chatbot_api --- Contiene la lógica del chatbot, incluído el funcionamiento de cadenas
- Chatbot frontend --- Interfaz del chatbot
- Course Neo4j --- Carga de la base de datos a Neo4j

## Documentación

Métodología CRISP-DM
### Entendimiento del negocio
1. **Objetivo del negocio:**
Básicamente, hay que vender cursos para que la plataforma siga en pie

2. **Planteamiento del Problema:**
Problema: La accesibilidad de los cursos es poco intuitiva y la tasa de finalización de los cursos es baja
Impacto: Los usuarios no completan los cursos, lo que afecta la satisfacción del cliente y las renovaciones de suscripción.

3. **Objetivo General del desarrollo**
Mejorar la personalización de recomendaciones de cursos, y faciliatr el acceso de los usuarios a toda la información necesaria para cursar

4. **Planificación**
- Tareas: Recolección de datos, análisis exploratorio, limpieza y preparación de datos, modelado, evaluación, despliegue, monitoreo.

### Recolección dde datos
- Recolectar datos iniciales: Se utilizó el conjunto de datos "Online Courses" disponible en Kaggle (https://www.kaggle.com/datasets/khaledatef1/online-courses) como fuente principal de información. Posteriormente se utilizó el conjunto de datos "Multi-Platform Online Courses Dataset" disponible tambien en Kaggle (https://www.kaggle.com/datasets/everydaycodings/multi-platform-online-courses-dataset)
- Descripción de datos: El segundo dataset se utilizó como formato para ambos datasets
- Calidad de los datos: El segundo dataset nos presentó varios problemas al presentar grna cantidad de datos nulos

### Preparación de los datos
Los dos datasets se acomodaron para acoplarse a una base de datos en grafos compuesta de 4 tablas principales:
- Courses: Tabla principal con la información de todos los cursos.
- Partners: Tabla con todos los proovedores disponibles de cursos online extraídos de los dos datasets
- Skills: Tabla con la lista de actividades necesarias para todos los cursos
- Q&A: Tabla con preguntas y respuestas generales relacionadas al funcionamiento de la plataforma y estructuras básicas de un curso online

### Modelado
- Construcción: LLM RAG CHATBOT With LangChain and Neo4j
La construcción y distribución general del proyecto se realizó siguiendo la estructura dispuesta en el tutorial del título

- Modelos utilizados: 2 tipos de consultas LangChain (Consulta de Grafo del dataset, Consulta de experiencia de la aplicación)

### Evaluación
Evaluación de resultados
- Completitud, correctitud y velocidad de la respuesta
  Durante el proceso tuvimos algunos problemas en la construcción de la consulta.
  Por la construcción de la aplicación, tiene un tiempo límite de ejecución para lanzar el error en caso de falla.
  El chat cumple con la completitud y correctitud de las respuestas relacionadas a las preguntas comunes y a información básica de los cursos, pero presenta problemas para las búsquedas más complejas, como evaluación de rankings y review de cada curso. En promedio, 2 de cada 4 consultas funcionan perfectamente.
- Por inconvenientes con los datasets en las últimas semanas del desarrollo, no concretamos una evaluación mediante .evals o otras herramientas para evaluación de llm 
