import unittest
from crew import Crew
from agent import Agent, StandardOperatingProcedure
from task import Task
from exceptions import CrewError

class TestCrew(unittest.TestCase):
    
    def setUp(self):
        sop = StandardOperatingProcedure("default", ["execute"])
        self.agent = Agent("test_agent", "worker", [], [sop])
        self.crew = Crew("test_crew", [self.agent])
    
    def test_crew_creation_success(self):
        self.assertEqual(self.crew.name, "test_crew")
        self.assertIn("test_agent", self.crew.agents)
    
    def test_crew_creation_no_agents(self):
        with self.assertRaises(CrewError):
            Crew("test", [])
    
    def test_assign_task_success(self):
        task = Task("1", "test task", {"data": "test"})
        result = self.crew.assign_task(task, "test_agent")
        
        self.assertEqual(result["agent"], "test_agent")
        self.assertEqual(len(self.crew.completed_tasks), 1)
    
    def test_assign_task_agent_not_found(self):
        task = Task("1", "test task", {"data": "test"})
        
        with self.assertRaises(CrewError):
            self.crew.assign_task(task, "nonexistent_agent")
    
    def test_get_crew_status(self):
        status = self.crew.get_crew_status()
        
        self.assertEqual(status["name"], "test_crew")
        self.assertEqual(len(status["agents"]), 1)
        self.assertEqual(status["tasks_completed"], 0)