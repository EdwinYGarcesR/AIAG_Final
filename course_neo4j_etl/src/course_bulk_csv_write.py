import logging
import os

from neo4j import GraphDatabase
from retry import retry

COURSES_CSV_PATH = os.getenv("COURSES_CSV_PATH")
PARTNERS_CSV_PATH = os.getenv("PARTNERS_CSV_PATH")
SKILLS_CSV_PATH = os.getenv("SKILLS_CSV_PATH")
QA_CSV_PATH = os.getenv("QA_CSV_PATH")


NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

LOGGER = logging.getLogger(__name__)

NODES = ["Course","Partner","Skill","QA"]


def _set_uniqueness_constraints(tx, node):
    query = f"""CREATE CONSTRAINT IF NOT EXISTS FOR (n:{node})
        REQUIRE n.id IS UNIQUE;"""
    _ = tx.run(query, {})


@retry(tries=100, delay=10)
def load_course_graph_from_csv() -> None:
    """Load structured course CSV data following
    a specific ontology into Neo4j"""

    driver = GraphDatabase.driver(
        NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    )

    LOGGER.info("Setting uniqueness constraints on nodes")
    with driver.session(database="neo4j") as session:
        for node in NODES:
            session.execute_write(_set_uniqueness_constraints, node)

    LOGGER.info("Loading Courses nodes")
    with driver.session(database="neo4j") as session:
        query = f"""
        LOAD CSV WITH HEADERS
        FROM '{COURSES_CSV_PATH}' AS courses
        MERGE (h:Course {{
                            course: courses.course,
                            skills: courses.skills,
                            partner: courses.partner,
                            rating: courses.rating,
                            reviewcount: courses.reviewcount,
                            level: courses.level,
                            certificate: courses.certificatetype,
                            duration: courses.duration,
                            crediteligibility: courses.crediteligibility}});
        """
        _ = session.run(query, {})
        
    LOGGER.info("Loading Partners nodes")
    with driver.session(database="neo4j") as session:
        query = f"""
        LOAD CSV WITH HEADERS
        FROM '{PARTNERS_CSV_PATH}' AS partners
        MERGE (h:Partner {{
                            partner: partners.partner
                            }});
        """
        _ = session.run(query, {})
    
    LOGGER.info("Loading Skills nodes")
    with driver.session(database="neo4j") as session:
        query = f"""
        LOAD CSV WITH HEADERS
        FROM '{SKILLS_CSV_PATH}' AS skills
        MERGE (h:Skill {{
                            skills: skills.skill
                            }});
        """
        _ = session.run(query, {})
    
    LOGGER.info("Loading Q&A nodes")
    with driver.session(database="neo4j") as session:
        query = f"""
        LOAD CSV WITH HEADERS
        FROM '{QA_CSV_PATH}' AS qa
        MERGE (h:QA {{
                            pregunta: qa.pregunta,
                            respuesta: qa.respuesta
                            }});
        """
        _ = session.run(query, {})

    LOGGER.info("Loading 'OFFERS' relationships")
    with driver.session(database="neo4j") as session:
        query = f"""
        LOAD CSV WITH HEADERS FROM '{COURSES_CSV_PATH}' AS courses
            MATCH (v:Course {{partner: (courses.partner)}})
            MATCH (r:Partner {{partner: (courses.partner)}})
            MERGE (v)-[offers:OFFERS]->(r)
        """
        _ = session.run(query, {})

if __name__ == "__main__":
    load_course_graph_from_csv()
