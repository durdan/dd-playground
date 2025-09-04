from dataclasses import dataclass
from typing import Dict, List, Optional
import yaml
import json

@dataclass
class DiffLimits:
    max_files_changed: int = 10
    max_lines_added: int = 500
    max_lines_deleted: int = 300
    max_lines_modified: int = 800
    max_complexity_increase: int = 10

@dataclass
class QualityConfig:
    diff_limits: DiffLimits
    required_approvals: int = 1
    block_on_failure: bool = True
    allowed_file_patterns: List[str] = None
    excluded_file_patterns: List[str] = None

class ConfigManager:
    def __init__(self, config_path: str = "quality_gates.yml"):
        self.config_path = config_path
        
    def load_config(self) -> QualityConfig:
        """Load configuration from file with fallback to defaults."""
        try:
            with open(self.config_path, 'r') as f:
                data = yaml.safe_load(f)
            return self._parse_config(data)
        except FileNotFoundError:
            return self._default_config()
        except Exception as e:
            raise ValueError(f"Invalid config file: {e}")
    
    def _parse_config(self, data: dict) -> QualityConfig:
        diff_data = data.get('diff_limits', {})
        diff_limits = DiffLimits(
            max_files_changed=diff_data.get('max_files_changed', 10),
            max_lines_added=diff_data.get('max_lines_added', 500),
            max_lines_deleted=diff_data.get('max_lines_deleted', 300),
            max_lines_modified=diff_data.get('max_lines_modified', 800),
            max_complexity_increase=diff_data.get('max_complexity_increase', 10)
        )
        
        return QualityConfig(
            diff_limits=diff_limits,
            required_approvals=data.get('required_approvals', 1),
            block_on_failure=data.get('block_on_failure', True),
            allowed_file_patterns=data.get('allowed_file_patterns'),
            excluded_file_patterns=data.get('excluded_file_patterns', [])
        )
    
    def _default_config(self) -> QualityConfig:
        return QualityConfig(diff_limits=DiffLimits())