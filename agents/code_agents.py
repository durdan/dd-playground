from crewai import Agent
from crewai_tools import CodeDocsSearchTool, FileReadTool
from langchain_openai import ChatOpenAI

class CodeGenerationAgents:
    def __init__(self, llm_model="gpt-4"):
        self.llm = ChatOpenAI(model=llm_model, temperature=0.1)
        self.code_search_tool = CodeDocsSearchTool()
        self.file_read_tool = FileReadTool()
    
    def create_architect_agent(self):
        return Agent(
            role="Software Architect",
            goal="Design robust, scalable software architecture and create detailed implementation plans",
            backstory="""You are a senior software architect with 15+ years of experience.
            You excel at breaking down complex problems into manageable components,
            designing clean interfaces, and ensuring code maintainability.""",
            tools=[self.code_search_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
    
    def create_developer_agent(self):
        return Agent(
            role="Senior Developer",
            goal="Implement high-quality, well-structured code following best practices",
            backstory="""You are an expert developer who writes clean, efficient code.
            You follow SOLID principles, implement proper error handling,
            and ensure code is testable and maintainable.""",
            tools=[self.code_search_tool, self.file_read_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
    
    def create_reviewer_agent(self):
        return Agent(
            role="Code Reviewer",
            goal="Review code for quality, security, performance, and adherence to best practices",
            backstory="""You are a meticulous code reviewer with expertise in security,
            performance optimization, and code quality. You catch bugs before they
            reach production and ensure code follows team standards.""",
            tools=[self.file_read_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
    
    def create_tester_agent(self):
        return Agent(
            role="Test Engineer",
            goal="Create comprehensive test suites with good coverage and meaningful test cases",
            backstory="""You are a testing expert who believes in test-driven development.
            You create unit tests, integration tests, and edge case scenarios
            to ensure code reliability and maintainability.""",
            tools=[self.file_read_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )