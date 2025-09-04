import pytest
import json
from pathlib import Path
from tempfile import NamedTemporaryFile
from plan_executor import PlanExecutor

class TestPlanExecutor:
    
    def test_execute_plan_without_crew(self):
        executor = PlanExecutor(use_crew=False)
        plan_data = {
            'tasks': [
                {'description': 'Task 1'},
                {'description': 'Task 2'}
            ]
        }
        
        result = executor.execute_plan(plan_data)
        
        assert result['status'] == 'success'
        assert result['tasks_completed'] == 2
        assert result['total_tasks'] == 2
    
    def test_execute_plan_empty_data(self):
        executor = PlanExecutor()
        
        with pytest.raises(ValueError, match="Plan data cannot be empty"):
            executor.execute_plan({})
    
    def test_execute_plan_no_tasks(self):
        executor = PlanExecutor()
        
        with pytest.raises(ValueError, match="Plan must contain tasks"):
            executor.execute_plan({'tasks': []})
    
    def test_execute_plan_file_json(self):
        executor = PlanExecutor(use_crew=False)
        plan_data = {
            'tasks': [{'description': 'Test task'}]
        }
        
        with NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(plan_data, f)
            plan_file = Path(f.name)
        
        try:
            result = executor.execute_plan_file(plan_file)
            assert result['status'] == 'success'
            assert result['tasks_completed'] == 1
        finally:
            plan_file.unlink()
    
    def test_execute_plan_file_not_found(self):
        executor = PlanExecutor()
        
        with pytest.raises(FileNotFoundError):
            executor.execute_plan_file(Path('nonexistent.json'))