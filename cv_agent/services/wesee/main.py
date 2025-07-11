#!/usr/bin/env python
import logging
import warnings

from .crew import Wesee

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run(linkedin_data: dict, job_description: str):
    """
    Run the crew with LinkedIn data fetched from database.

    Args:
        linkedin_data (dict): LinkedIn profile data from database
        job_description (str): Job description to match against
    """
    inputs = {"linkedin_input": linkedin_data, "job_posting": job_description}

    logger.info(f"Running crew with LinkedIn data and job description")
    logger.info(
        f"LinkedIn data keys: {list(linkedin_data.keys()) if linkedin_data else 'No data'}"
    )
    try:
        result = Wesee().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
    logger.info(f"Crew result created!")
    return result
