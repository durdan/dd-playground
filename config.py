from dataclasses import dataclass
from typing import Dict, List
import os

@dataclass
class ModelConfig:
    name: str
    version: str
    deployment_date: str
    performance_threshold: float
    max_versions: int = 5

@dataclass
class KeyConfig:
    key_name: str
    rotation_days: int
    service: str

@dataclass
class ArchivalConfig:
    retention_days: int
    storage_path: str
    compression: bool = True

class ConfigManager:
    def __init__(self):
        self.models = self._load_model_configs()
        self.keys = self._load_key_configs()
        self.archival = self._load_archival_config()
    
    def _load_model_configs(self) -> List[ModelConfig]:
        # In production, load from config file or environment
        return [
            ModelConfig("sentiment-analyzer", "v1.2.0", "2024-01-15", 0.85),
            ModelConfig("text-classifier", "v2.1.0", "2024-01-10", 0.90)
        ]
    
    def _load_key_configs(self) -> List[KeyConfig]:
        return [
            KeyConfig("api_key_primary", 30, "main_service"),
            KeyConfig("db_password", 90, "database"),
            KeyConfig("jwt_secret", 60, "auth_service")
        ]
    
    def _load_archival_config(self) -> ArchivalConfig:
        return ArchivalConfig(
            retention_days=365,
            storage_path=os.getenv("ARCHIVE_PATH", "/data/archive"),
            compression=True
        )