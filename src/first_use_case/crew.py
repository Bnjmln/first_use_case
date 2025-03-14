from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, WebsiteSearchTool

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class EmailAnalyzeCrew:
    """Email Analyze Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    @agent
    def web_searcher(self) -> Agent:
        return Agent(
            config=self.agents_config["web_searcher"],
            verbose=True,
            tools=[SerperDevTool(),]
        )
    @agent
    def services_expert(self) -> Agent:
        return Agent(
            config=self.agents_config["services_expert"],
            verbose=True,
            tools=[SerperDevTool(
                search_url='https://www.ricoh-americalatina.com/en'
            ),]
        )
    @agent
    def services_recommender(self) -> Agent:
        return Agent(
        config=self.agents_config["services_recommender"],
        verbose=True
    )
    @agent
    def email_writer(self) -> Agent:
        return Agent(
        config=self.agents_config["email_writer"],
        verbose=True
    )
    
    @task
    def investigate_person(self) -> Task:
        return Task(
            config=self.tasks_config["investigate_person"],
        )
    @task
    def services_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["services_analysis"],
        )
    @task
    def make_match(self) -> Task:
        return Task(
            config=self.tasks_config["make_match"],
            output_file='output/report.md'
        )
    @task
    def write_email(self) -> Task:
        return Task(
            config=self.tasks_config["write_email"],
            output_file='output_email/report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""

        return Crew(
            agents=self.agents, 
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
