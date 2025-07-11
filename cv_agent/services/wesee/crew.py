from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Wesee():
    """WeSee crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def linkedin_data_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['linkedin_data_analyst'], # type: ignore[index]
            verbose=True
        )

    @agent
    def job_requirements_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['job_requirements_analyst'], # type: ignore[index]
            verbose=True
        )

    @agent
    def content_filter_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['content_filter_specialist'], # type: ignore[index]
            verbose=True
        )

    @agent
    def cv_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['cv_writer'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def extract_linkedin_data(self) -> Task:
        return Task(
            config=self.tasks_config['extract_linkedin_data'], # type: ignore[index]
        )

    @task
    def analyze_job_requirements(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_job_requirements'], # type: ignore[index]
        )

    @task
    def filter_relevant_content(self) -> Task:
        return Task(
            config=self.tasks_config['filter_relevant_content'], # type: ignore[index]
        )

    @task
    def create_customized_cv(self) -> Task:
        return Task(
            config=self.tasks_config['create_customized_cv'], # type: ignore[index]
            output_file='customized_cv.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the WeSee crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
