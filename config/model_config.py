from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
import json
from pathlib import Path

@dataclass
class ModelConfig:
    """Configuration for ML model parameters and hyperparameters."""
    model_type: str
    learning_rate: float = 0.001
    batch_size: int = 32
    epochs: int = 100
    random_seed: int = 42
    hyperparameters: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.hyperparameters is None:
            self.hyperparameters = {}
        self._validate()
    
    def _validate(self):
        if not self.model_type:
            raise ValueError("model_type cannot be empty")
        if self.learning_rate <= 0:
            raise ValueError("learning_rate must be positive")
        if self.batch_size <= 0:
            raise ValueError("batch_size must be positive")
        if self.epochs <= 0:
            raise ValueError("epochs must be positive")
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ModelConfig':
        return cls(**data)
    
    def save(self, filepath: str):
        """Save configuration to JSON file."""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load(cls, filepath: str) -> 'ModelConfig':
        """Load configuration from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)