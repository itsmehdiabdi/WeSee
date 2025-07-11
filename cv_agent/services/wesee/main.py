#!/usr/bin/env python
import logging
import warnings

from wesee.crew import Wesee

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run(linkedin_url: str, job_description: str):
    """
    Run the crew.
    """
    inputs = {
        'linkedin_url': linkedin_url,
        'job_description': job_description
    }
    
    logger.info(f"Running crew with inputs: {inputs}")
    try:
        result = Wesee().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
    logger.info(f"Crew result created!")
    return result
