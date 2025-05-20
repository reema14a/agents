from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage


from .tools.push_tool import PushNotificationTool

from typing import List
from pydantic import BaseModel, Field

import os
from dotenv import load_dotenv
load_dotenv()  # 👈 Loads .env vars into os.environ

# Get the GEMINI API key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

class TrendingCompany(BaseModel):
    """A company that is in the news and attracting attention"""
    company_name: str = Field(description="The name of the company")
    ticker: str = Field(description="The companies stock ticker")
    industry: str = Field(description="The industry that the company operates in")
    reason_for_trend: str = Field(description="Why the company is currently trending")

class TrendingCompaniesList(BaseModel):
    """List of trending companies"""
    trending_companies: List[TrendingCompany] = Field(description="A list of trending companies")

class TrendingCompanyResearch(BaseModel):
    """Detailed research on a company"""
    company_name: str = Field(description="The name of the company")
    market_position: str = Field(description="The current market position and competitive analysis")
    future_outlook: str = Field(description="The future outlook and growth prospects")
    investment_potential: str = Field(description="The investment potential and suitability for investment")

class TrendingCompaniesResearchList(BaseModel):
    """List of detailed research on all the companies"""
    research_list: List[TrendingCompanyResearch] = Field(description="A list of detailed research on all trending companies")


@CrewBase
class StockPicker():
    """StockPicker crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def trending_company_finder(self) -> Agent:
        return Agent(
            config=self.agents_config['trending_company_finder'],
            tools=[SerperDevTool()],
            verbose=True, 
            memory=True
        )

    @agent
    def financial_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_researcher'],
            tools=[SerperDevTool()], 
            verbose=True
        )

    @agent
    def stock_picker(self) -> Agent:
        return Agent(
            config=self.agents_config['stock_picker'],
            tools=[PushNotificationTool()],
            verbose=True,
            memory=True
        )

    @task
    def find_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['find_trending_companies'],
            output_pydantic=TrendingCompaniesList
        )

    @task
    def research_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['research_trending_companies'],
            output_pydantic=TrendingCompaniesResearchList
        )
    
    @task
    def pick_best_company(self) -> Task:
        return Task(
            config=self.tasks_config['pick_best_company']
        )

    @crew
    def crew(self) -> Crew:
        """Creates the StockPicker crew"""
        
        manager = Agent(
            config=self.agents_config['manager'],
            allow_delegation=True
        )

        long_term_memory = LongTermMemory(
                storage=LTMSQLiteStorage(
                    db_path="./memory/long_term_memory_storage.db"
                )
            )
        
        # Short-term memory for current context using RAG
        short_term_memory = ShortTermMemory(
                storage = RAGStorage(
                        embedder_config={
                            "provider": "google",
                            "config": {
                                "model": "models/text-embedding-004",
                                "api_key": GEMINI_API_KEY,
                            }
                        },
                        type="short_term",
                        path="./memory/"
                    )
                )
        
        # Entity memory for tracking key information about entities
        entity_memory = EntityMemory(
            storage=RAGStorage(
                embedder_config={
                    "provider": "google",
                    "config": {
                        "model": "models/text-embedding-004",
                        "api_key": GEMINI_API_KEY,
                    }
                },
                type="short_term",
                path="./memory/"
            )
        )
        
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.hierarchical,
            verbose=True,
            manager_agent=manager,
            memory=True,
            long_term_memory = long_term_memory,
            short_term_memory = short_term_memory,            
            entity_memory = entity_memory,
        )
