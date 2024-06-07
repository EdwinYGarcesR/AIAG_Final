import os
from typing import Any

import numpy as np
from langchain_community.graphs import Neo4jGraph


def _get_current_courses() -> list[str]:
    """Fetch a list of current courses names from a Neo4j database."""
    graph = Neo4jGraph(
        url=os.getenv("NEO4J_URI"),
        username=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD"),
    )

    current_courses = graph.query(
        """
        MATCH (h:Curso)
        RETURN h.name AS course
        """
    )

    current_courses = [d["course"].lower() for d in current_courses]

    return current_courses


def _get_current_wait_time_minutes(course: str) -> int:
    """Get the current wait time at a course in minutes."""

    current_courses = _get_current_courses()

    if course.lower() not in current_courses:
        return -1

    return np.random.randint(low=0, high=600)


def get_current_wait_times(course: str) -> str:
    """Get the current wait time at a course formatted as a string."""

    wait_time_in_minutes = _get_current_wait_time_minutes(course)

    if wait_time_in_minutes == -1:
        return f"Course '{course}' does not exist."

    hours, minutes = divmod(wait_time_in_minutes, 60)

    if hours > 0:
        formatted_wait_time = f"{hours} hours {minutes} minutes"
    else:
        formatted_wait_time = f"{minutes} minutes"

    return formatted_wait_time


def get_most_available_course(_: Any) -> dict[str, float]:
    """Find the course with the shortest wait time."""

    current_courses = _get_current_courses()

    current_wait_times = [
        _get_current_wait_time_minutes(h) for h in current_courses
    ]

    best_time_idx = np.argmin(current_wait_times)
    best_course = current_courses[best_time_idx]
    best_wait_time = current_wait_times[best_time_idx]

    return {best_course: best_wait_time}
