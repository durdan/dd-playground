#!/usr/bin/env python3
"""
Project setup automation script.
Sets up development environment with all necessary dependencies and configurations.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


class SetupError(Exception):
    """Custom exception for setup failures."""
    pass


class ProjectSetup:
    """Handles automated project setup."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.venv_path = self.project_root / "venv"
        
    def run_command(self, command, check=True):
        """Run shell command with error handling."""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                check=check,
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            return result
        except subprocess.CalledProcessError as e:
            raise SetupError(f"Command failed: {command}\nError: {e.stderr}")
    
    def check_prerequisites(self):
        """Verify required tools are installed."""
        print("🔍 Checking prerequisites...")
        
        # Check Python version
        if sys.version_info < (3, 8):
            raise SetupError("Python 3.8+ is required")
        print(f"✅ Python {sys.version.split()[0]}")
        
        # Check Git
        try:
            self.run_command("git --version")
            print("✅ Git")
        except SetupError:
            raise SetupError("Git is required but not installed")
    
    def setup_virtual_environment(self):
        """Create and activate virtual environment."""
        print("🐍 Setting up virtual environment...")
        
        if self.venv_path.exists():
            print("Virtual environment already exists, skipping creation")
            return
            
        self.run_command(f"python -m venv {self.venv_path}")
        print("✅ Virtual environment created")
    
    def install_dependencies(self):
        """Install Python dependencies."""
        print("📦 Installing dependencies...")
        
        pip_cmd = str(self.venv_path / "bin" / "pip")
        if os.name == "nt":  # Windows
            pip_cmd = str(self.venv_path / "Scripts" / "pip.exe")
        
        requirements_file = self.project_root / "requirements.txt"
        if requirements_file.exists():
            self.run_command(f"{pip_cmd} install -r requirements.txt")
            print("✅ Dependencies installed")
        else:
            print("⚠️  No requirements.txt found, skipping dependency installation")
    
    def setup_configuration(self):
        """Setup local configuration files."""
        print("⚙️  Setting up configuration...")
        
        config_dir = self.project_root / "config"
        if not config_dir.exists():
            config_dir.mkdir()
        
        # Copy example config if it exists
        example_config = config_dir / "local.example.yml"
        local_config = config_dir / "local.yml"
        
        if example_config.exists() and not local_config.exists():
            shutil.copy(example_config, local_config)
            print("✅ Local configuration created")
        else:
            print("ℹ️  Configuration files already exist or no example found")
    
    def setup_git_hooks(self):
        """Setup pre-commit hooks if available."""
        print("🪝 Setting up Git hooks...")
        
        try:
            pip_cmd = str(self.venv_path / "bin" / "pip")
            if os.name == "nt":
                pip_cmd = str(self.venv_path / "Scripts" / "pip.exe")
            
            # Install pre-commit if not already installed
            self.run_command(f"{pip_cmd} install pre-commit")
            
            # Install hooks
            precommit_cmd = str(self.venv_path / "bin" / "pre-commit")
            if os.name == "nt":
                precommit_cmd = str(self.venv_path / "Scripts" / "pre-commit.exe")
            
            self.run_command(f"{precommit_cmd} install")
            print("✅ Git hooks installed")
        except SetupError:
            print("⚠️  Could not setup Git hooks (optional)")
    
    def run_initial_tests(self):
        """Run tests to verify setup."""
        print("🧪 Running initial tests...")
        
        python_cmd = str(self.venv_path / "bin" / "python")
        if os.name == "nt":
            python_cmd = str(self.venv_path / "Scripts" / "python.exe")
        
        try:
            self.run_command(f"{python_cmd} -m pytest --tb=short")
            print("✅ All tests passed")
        except SetupError:
            print("⚠️  Some tests failed - check your setup")
    
    def setup(self):
        """Run complete setup process."""
        print("🚀 Starting project setup...\n")
        
        try:
            self.check_prerequisites()
            self.setup_virtual_environment()
            self.install_dependencies()
            self.setup_configuration()
            self.setup_git_hooks()
            self.run_initial_tests()
            
            print("\n🎉 Setup completed successfully!")
            print("\nNext steps:")
            print("1. Activate virtual environment: source venv/bin/activate")
            print("2. Start development server: ./scripts/dev-server.py")
            print("3. Read docs/ONBOARDING.md for detailed information")
            
        except SetupError as e:
            print(f"\n❌ Setup failed: {e}")
            print("Check docs/ONBOARDING.md for manual setup instructions")
            sys.exit(1)


if __name__ == "__main__":
    setup = ProjectSetup()
    setup.setup()