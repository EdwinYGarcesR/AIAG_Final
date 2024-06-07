import os

from langchain.chains import GraphCypherQAChain
from langchain.prompts import PromptTemplate
from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI

COURSE_QA_MODEL = os.getenv("COURSE_QA_MODEL")
COURSE_CYPHER_MODEL = os.getenv("COURSE_CYPHER_MODEL")

graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
)

graph.refresh_schema()

cypher_generation_template = """
Task:
Generate Cypher query for a Neo4j graph database.

Instructions:
Use the provided relationship types and properties in the schema.

Schema:
{schema}

Note:
Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything other than
for you to construct a Cypher statement. Do not include any text except
the generated Cypher statement. Make sure the direction of the relationship is
correct in your queries. Make sure you alias both entities and relationships
properly. Do not run any queries that would add to or delete from
the database. Make sure to alias all statements that follow as with
statement (e.g. WITH v as visit, c.billing_amount as billing_amount)
If you need to divide numbers, make sure to
filter the denominator to be non zero.If you receive any name of a required 
skill or partner that is in Spanish, translate it into English before searching.

Examples:
# What is the course with the highest number of reviews?
MATCH (c:Course)
WHERE c.reviewcount IS NOT NULL
RETURN c
ORDER BY toInteger(c.reviewcount) DESCENDING
LIMIT 1

# What is the course with the lowlest number of reviews?
MATCH (c:Course)
WHERE c.reviewcount IS NOT NULL
RETURN c
ORDER BY toInteger(c.reviewcount) ASCENDING
LIMIT 1

# Can you provide me information about this course "Tools of the Trade: Linux and SQL"?
MATCH (c:Course {course: 'Tools of the Trade: Linux and SQL'})
RETURN c

# Which courses need skills like "Python Programming"?
MATCH (c:Course)
WHERE "Python Programming" IN split(substring(c.skills, 1, size(c.skills) - 1), ", ")
RETURN c

# Can i find IBM courses?
MATCH (c:Course {partner: 'IBM'})
RETURN c

# How many courses exist belonging to Google?
match (r:Course)-[:OFFERS]->(v:Partner)
where r.partner = 'Google'
return count(*)

# What courses do you have available on the Google Cloud platform?
match (r:Course)-[c:OFFERS]->(v:Partner)
where r.partner = 'Google Cloud'
return r

# What is the course with the best Microsoft ranking?
match (r:Course)-[c:OFFERS]->(v:Partner)
where r.partner = 'Microsoft'
RETURN r
ORDER BY toInteger(r.rating) DESCENDING
LIMIT 1

# On the platform I can find the course 'Agile with Atlassian Jira' offered by 'Attlassian'?
match (r:Course)-[c:OFFERS]->(v:Partner)
where r.partner = 'Atlassian' and r.course = 'Agile with Atlassian Jira'
RETURN r

# Are there any discounts available for students or groups?
MATCH (c:QA)
WHERE c.pregunta = 'Are there any discounts available for students or groups?'
RETURN c.respuesta

Make sure to use IS NULL or IS NOT NULL when analyzing missing properties.
Never return embedding properties in your queries. You must never include the
statement "GROUP BY" in your query.
If you need to divide numbers, make sure to filter the denominator to be non
zero.

The question is:
{question}
"""

cypher_generation_prompt = PromptTemplate(
    input_variables=["schema", "question"], template=cypher_generation_template
)

qa_generation_template = """You are an assistant that takes the results
from a Neo4j Cypher query and forms a human-readable response. The
query results section contains the results of a Cypher query that was
generated based on a users natural language question. The provided
information is authoritative, you must never doubt it or try to use
your internal knowledge to correct it. Make the answer sound like a
response to the question.

Query Results:
{context}

Question:
{question}

If the provided information is empty, say you don't know the answer.
Empty information looks like this: []

If the information is not empty, you must provide an answer using the
results. If the question involves a time duration, assume the query
results are in units of days unless otherwise specified.

Never say you don't have the right information if there is data in
the query results. Make sure to show all the relevant query results
if you're asked.

Helpful Answer:
"""

qa_generation_prompt = PromptTemplate(
    input_variables=["context", "question"], template=qa_generation_template
)

course_cypher_chain = GraphCypherQAChain.from_llm(
    cypher_llm=ChatOpenAI(model=COURSE_CYPHER_MODEL, temperature=0),
    qa_llm=ChatOpenAI(model=COURSE_QA_MODEL, temperature=0),
    graph=graph,
    verbose=True,
    qa_prompt=qa_generation_prompt,
    cypher_prompt=cypher_generation_prompt,
    validate_cypher=True,
    top_k=100,
)
