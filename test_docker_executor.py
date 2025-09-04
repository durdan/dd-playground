import unittest
from unittest.mock import patch, MagicMock
from docker_executor import DockerExecutor, DockerResult

class TestDockerExecutor(unittest.TestCase):
    def setUp(self):
        self.executor = DockerExecutor("python:3.9")
    
    def test_init_requires_image(self):
        with self.assertRaises(TypeError):
            DockerExecutor()
    
    def test_run_command_empty_command_fails(self):
        with self.assertRaises(ValueError):
            self.executor.run_command([])
    
    @patch('subprocess.run')
    def test_run_command_success(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="success output",
            stderr=""
        )
        
        result = self.executor.run_command(["echo", "hello"])
        
        self.assertTrue(result.success)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.stdout, "success output")
    
    @patch('subprocess.run')
    def test_run_command_failure(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="",
            stderr="error output"
        )
        
        result = self.executor.run_command(["false"])
        
        self.assertFalse(result.success)
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(result.stderr, "error output")

if __name__ == '__main__':
    unittest.main()