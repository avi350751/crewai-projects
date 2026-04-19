from logging import config

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
from typing import List
from .tools.push_tool import PushNotificationTool
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage


class TrendingCompany(BaseModel):
    """A company that is in news and attractiong attention"""
    name: str = Field(..., description="The name of the company")
    ticker: str = Field(..., description="The stock ticker symbol of the company")
    reason: str = Field(..., description="The reason why the stock is trending")

class TrendingCompanyList(BaseModel):
    """A list of trending companies"""
    companies: List[TrendingCompany] = Field(description="A list of trending companies")

class TrendingCompanyResearch(BaseModel):
    """The research output for a trending company"""
    name: str = Field(..., description="The name of the company")
    market_position: str = Field(..., description="The market position of the company")
    future_outlook: str= Field(..., description="The future outlook for the company")
    investment_potential: str = Field(..., description="The investment potential of the company")
    
class TrendingCompanyResearchList(BaseModel):
    """A list of research outputs for trending companies"""
    research_list: List[TrendingCompanyResearch] = Field(description="Comprehensive research on the trending companies, including their market position, future outlook, and investment potential")

@CrewBase
class StockPicker():
    """StockPicker crew"""

    agents_config: 'config/agents.yaml'
    tasks_config: 'config/tasks.yaml'
   

    @agent
    def trending_company_finder(self) -> Agent:
        return Agent(
            config=self.agents_config['trending_company_finder'], # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool()],
            memory=True
        )

    @agent
    def financial_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_researcher'], # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool()]
        )
    
    @agent
    def stock_picker(self) -> Agent:
        return Agent(
            config=self.agents_config['stock_picker'], # type: ignore[index]
            verbose=True,
            tools=[PushNotificationTool()],
            memory=True
        )

    @task
    def find_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['find_trending_companies'], # type: ignore[index]
            output_pydantic=TrendingCompanyList
        )

    @task
    def research_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['research_trending_companies'], # type: ignore[index]
            output_pydantic=TrendingCompanyResearchList
        )
    
    @task
    def pick_best_stock(self) -> Task:
        return Task(
            config=self.tasks_config['pick_best_stock'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the StockPicker crew"""

        manager = Agent(
            config=self.agents_config['manager'], # type: ignore[index]
            verbose=True,
            allow_delegation=True,
        )

        short_term_memory = ShortTermMemory(
            storage=RAGStorage(
                embedder_config={
                    "provider": "openai",
                    "config": {
                        "model": "text-embedding-3-small",
                    }
                },
                type="short_term",
                path="./memory/"
            )
        )

        long_term_memory = LongTermMemory(
            storage=LTMSQLiteStorage(
                db_path="./memory/long_term_memory_storage.db"
            )
        )

        entity_memory = EntityMemory(
            storage=RAGStorage(
                embedder_config={
                    "provider": "openai",
                    "config": {
                        "model": "text-embedding-3-small",
                    }
                },
                type="entity",
                path="./memory/"
            )
        )

        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.hierarchical,
            verbose=True,
            manager_agent=manager,
            memory=True,
            short_term_memory= short_term_memory,
            long_term_memory= long_term_memory,
            entity_memory= entity_memory
        )