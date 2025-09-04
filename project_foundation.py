from pathlib import Path
from typing import Dict, Any, Optional
import json

from config.model_config import ModelConfig
from repositories.repo_manager import RepositoryManager
from metrics.success_metrics import SuccessMetrics, Metric, MetricType

class ProjectFoundation:
    """Main orchestrator for ML project foundation setup."""
    
    def __init__(self, project_name: str, base_dir: str = "."):
        if not project_name:
            raise ValueError("Project name cannot be empty")
        
        self.project_name = project_name
        self.base_dir = Path(base_dir)
        self.config_dir = self.base_dir / "config"
        
        # Initialize components
        self.repo_manager = RepositoryManager(
            str(self.config_dir / "repositories.json")
        )
        self.model_config: Optional[ModelConfig] = None
        self.success_metrics = SuccessMetrics()
        
        # Create directory structure
        self._setup_directories()
    
    def _setup_directories(self):
        """Create necessary project directories."""
        directories = [
            self.config_dir,
            self.base_dir / "data",
            self.base_dir / "models",
            self.base_dir / "logs",
            self.base_dir / "results"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def setup_model_config(self, model_type: str, **kwargs) -> ModelConfig:
        """Setup model configuration."""
        self.model_config = ModelConfig(model_type=model_type, **kwargs)
        config_path = self.config_dir / "model_config.json"
        self.model_config.save(str(config_path))
        return self.model_config
    
    def add_success_metric(self, name: str, metric_type: str, target_value: float, 
                          higher_is_better: bool = True) -> bool:
        """Add a success metric."""
        try:
            metric_type_enum = MetricType(metric_type)
            metric = Metric(
                name=name,
                metric_type=metric_type_enum,
                target_value=target_value,
                higher_is_better=higher_is_better
            )
            self.success_metrics.add_metric(metric)
            self._save_metrics()
            return True
        except ValueError as e:
            raise ValueError(f"Invalid metric type '{metric_type}': {e}")
    
    def add_repository(self, repo_path: str) -> bool:
        """Add a target repository."""
        return self.repo_manager.add_repository(repo_path)
    
    def get_project_status(self) -> Dict[str, Any]:
        """Get comprehensive project status."""
        return {
            'project_name': self.project_name,
            'repositories': {
                'count': len(self.repo_manager.list_repositories()),
                'list': self.repo_manager.list_repositories(),
                'invalid': self.repo_manager.validate_repositories()
            },
            'model_config': self.model_config.to_dict() if self.model_config else None,
            'metrics': {
                'count': len(self.success_metrics.list_metrics()),
                'summary': self.success_metrics.get_summary(),
                'all_targets_met': self.success_metrics.all_targets_met()
            }
        }
    
    def save_project_state(self):
        """Save all project configurations."""
        if self.model_config:
            self.model_config.save(str(self.config_dir / "model_config.json"))
        self._save_metrics()
    
    def load_project_state(self):
        """Load existing project configurations."""
        # Load model config
        model_config_path = self.config_dir / "model_config.json"
        if model_config_path.exists():
            self.model_config = ModelConfig.load(str(model_config_path))
        
        # Load metrics
        metrics_path = self.config_dir / "success_metrics.json"
        if metrics_path.exists():
            self.success_metrics = SuccessMetrics.load(str(metrics_path))
    
    def _save_metrics(self):
        """Save success metrics to file."""
        metrics_path = self.config_dir / "success_metrics.json"
        self.success_metrics.save(str(metrics_path))