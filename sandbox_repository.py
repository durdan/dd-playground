import json
import os
from pathlib import Path

class SandboxRepository:
    def __init__(self, config_file: str = "sandbox_config.json"):
        self._config_file = Path(config_file)
    
    def load_sandbox_state(self) -> bool:
        """Load sandbox state from file, default to False if file doesn't exist."""
        try:
            if self._config_file.exists():
                with open(self._config_file, 'r') as f:
                    data = json.load(f)
                    return data.get('sandbox_enabled', False)
        except (json.JSONDecodeError, IOError):
            pass
        return False
    
    def save_sandbox_state(self, enabled: bool) -> None:
        """Save sandbox state to file."""
        if not isinstance(enabled, bool):
            raise ValueError("Sandbox state must be boolean")
            
        try:
            data = {'sandbox_enabled': enabled}
            with open(self._config_file, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            raise RuntimeError(f"Failed to save sandbox state: {e}")
    
    def clear_config(self) -> None:
        """Remove config file for testing."""
        if self._config_file.exists():
            self._config_file.unlink()