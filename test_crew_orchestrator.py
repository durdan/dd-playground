import pytest
from unittest.mock import Mock, patch
from crew_orchestrator import CrewOrchestrator

class TestCrewOrchestrator:
    
    def test_init_with_valid_config(self):
        config = {
            'agents': [
                {
                    'role': 'Test Agent',
                    'goal': 'Test goal',
                    'backstory': 'Test backstory'
                }
            ]
        }
        orchestrator = CrewOrchestrator(config)
        assert len(orchestrator.agents) == 1
        assert orchestrator.crew is not None
    
    def test_init_with_empty_config(self):
        config = {'agents': []}
        orchestrator = CrewOrchestrator(config)
        assert len(orchestrator.agents) == 0
    
    @patch('crew_orchestrator.Crew')
    def test_execute_plan_tasks_success(self, mock_crew_class):
        mock_crew = Mock()
        mock_crew.kickoff.return_value = "Success"
        mock_crew_class.return_value = mock_crew
        
        config = {
            'agents': [
                {'role': 'Test', 'goal': 'Test goal'}
            ]
        }
        orchestrator = CrewOrchestrator(config)
        orchestrator.crew = mock_crew
        
        tasks = [{'description': 'Test task'}]
        result = orchestrator.execute_plan_tasks(tasks)
        
        assert result['status'] == 'success'
        assert result['tasks_completed'] == 1
    
    def test_execute_plan_tasks_empty_tasks(self):
        config = {'agents': []}
        orchestrator = CrewOrchestrator(config)
        
        with pytest.raises(ValueError, match="No tasks provided"):
            orchestrator.execute_plan_tasks([])