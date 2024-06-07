from  chains.hospital_review_chain import reviews_vector_chain
import openai
import json
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

class RAGChatbotEval:
    def __init__(self, retrieval_function, generation_function):
        self.retrieval_function = retrieval_function
        self.generation_function = generation_function

    def evaluate(self, item):
        prompt = item['input']
        expected_response = item['ideal']

        # Llamar a la función de recuperación de información
        retrieved_info = self.retrieval_function(prompt)
        
        # Crear un nuevo prompt combinando la información recuperada con la pregunta original
        new_prompt = f"Context retrieved: {retrieved_info}\nQuestion: {prompt}"

        # Llamar a la API de OpenAI para obtener la respuesta del modelo
        response = self.generation_function(new_prompt)

        generated_response = response.strip()

        # Evaluar si la respuesta generada es correcta
        is_correct = generated_response.lower() == expected_response.lower()

        return {
            "input": prompt,
            "retrieved_info": retrieved_info,
            "expected": expected_response,
            "generated": generated_response,
            "correct": is_correct
        }

# Implementación real de tu lógica de recuperación de información
def actual_retrieval_function(query):
    response = reviews_vector_chain({"query": query})
    return response["result"]

# Implementación real de tu generación de texto usando OpenAI
def actual_generation_function(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )
    return response.choices[0].text.strip()

# Crear una instancia de la evaluación
rag_chatbot_eval = RAGChatbotEval(
    retrieval_function=actual_retrieval_function,
    generation_function=actual_generation_function
)

# Cargar datos de evaluación desde el archivo JSON
with open("chatbot_api\src\eval\eval_data.json", 'r') as file:
    eval_data = json.load(file)

# Ejecutar la evaluación
results = [rag_chatbot_eval.evaluate(item) for item in eval_data]

# Calcular precisión
accuracy = sum(result['correct'] for result in results) / len(results)
print(f"Accuracy: {accuracy * 100:.2f}%")

# Imprimir resultados detallados
for result in results:
    print(result)