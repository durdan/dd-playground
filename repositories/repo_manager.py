from typing import List, Set
from pathlib import Path
import json

class RepositoryManager:
    """Manages target repositories for the ML project."""
    
    def __init__(self, config_file: str = "config/repositories.json"):
        self.config_file = config_file
        self.repositories: Set[str] = set()
        self._load_repositories()
    
    def add_repository(self, repo_path: str) -> bool:
        """Add a repository to the target list."""
        if not repo_path:
            raise ValueError("Repository path cannot be empty")
        
        # Normalize path
        normalized_path = str(Path(repo_path).resolve())
        
        if normalized_path in self.repositories:
            return False  # Already exists
        
        self.repositories.add(normalized_path)
        self._save_repositories()
        return True
    
    def remove_repository(self, repo_path: str) -> bool:
        """Remove a repository from the target list."""
        normalized_path = str(Path(repo_path).resolve())
        
        if normalized_path not in self.repositories:
            return False  # Doesn't exist
        
        self.repositories.remove(normalized_path)
        self._save_repositories()
        return True
    
    def list_repositories(self) -> List[str]:
        """Get list of all target repositories."""
        return sorted(list(self.repositories))
    
    def validate_repositories(self) -> List[str]:
        """Check which repositories exist and return invalid ones."""
        invalid_repos = []
        for repo in self.repositories:
            if not Path(repo).exists():
                invalid_repos.append(repo)
        return invalid_repos
    
    def _load_repositories(self):
        """Load repositories from config file."""
        try:
            if Path(self.config_file).exists():
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.repositories = set(data.get('repositories', []))
        except (json.JSONDecodeError, IOError):
            self.repositories = set()
    
    def _save_repositories(self):
        """Save repositories to config file."""
        Path(self.config_file).parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump({'repositories': list(self.repositories)}, f, indent=2)