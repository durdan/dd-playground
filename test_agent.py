import unittest
from agent import Agent, StandardOperatingProcedure
from exceptions import AgentError, PolicyViolationError

class TestAgent(unittest.TestCase):
    
    def setUp(self):
        self.sop = StandardOperatingProcedure(
            name="research",
            steps=["gather data", "analyze", "summarize"]
        )
        self.agent = Agent(
            name="researcher",
            role="data_analyst", 
            policies=["no_external_data"],
            sops=[self.sop]
        )
    
    def test_agent_creation_success(self):
        self.assertEqual(self.agent.name, "researcher")
        self.assertEqual(self.agent.role, "data_analyst")
        self.assertIn("research", self.agent.sops)
    
    def test_agent_creation_invalid_name(self):
        with self.assertRaises(AgentError):
            Agent("", "role", [], [])
    
    def test_execute_task_success(self):
        task_data = {"input": "test data", "sop": "research"}
        result = self.agent.execute_task(task_data)
        
        self.assertEqual(result["agent"], "researcher")
        self.assertEqual(result["status"], "completed")
        self.assertEqual(len(result["steps_executed"]), 3)
    
    def test_execute_task_policy_violation(self):
        task_data = {"external_data": True, "sop": "research"}
        
        with self.assertRaises(PolicyViolationError):
            self.agent.execute_task(task_data)
    
    def test_execute_task_invalid_sop(self):
        task_data = {"sop": "nonexistent"}
        
        with self.assertRaises(AgentError):
            self.agent.execute_task(task_data)

class TestStandardOperatingProcedure(unittest.TestCase):
    
    def test_sop_creation_success(self):
        sop = StandardOperatingProcedure("test", ["step1", "step2"])
        self.assertEqual(sop.name, "test")
        self.assertEqual(len(sop.steps), 2)
    
    def test_sop_creation_empty_name(self):
        with self.assertRaises(AgentError):
            StandardOperatingProcedure("", ["step1"])
    
    def test_sop_creation_no_steps(self):
        with self.assertRaises(AgentError):
            StandardOperatingProcedure("test", [])