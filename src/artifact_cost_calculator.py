from typing import Dict, Any
from .artifact import Artifact, ArtifactType

class ArtifactCostCalculator:
    # Cost per GB per month for different artifact types
    STORAGE_COSTS = {
        ArtifactType.DOCUMENT: 0.023,  # Standard storage
        ArtifactType.IMAGE: 0.023,     # Standard storage
        ArtifactType.MODEL: 0.045,     # Premium storage for models
        ArtifactType.DATASET: 0.018,   # Cold storage for datasets
        ArtifactType.CODE: 0.023       # Standard storage
    }
    
    # Processing costs per operation
    PROCESSING_COSTS = {
        "create": 0.001,
        "read": 0.0001,
        "update": 0.0005,
        "delete": 0.0001
    }
    
    def calculate_storage_cost(self, artifact: Artifact, days: int = 30) -> float:
        """Calculate monthly storage cost for an artifact."""
        if artifact.size_bytes <= 0:
            return 0.0
        
        gb_size = artifact.size_bytes / (1024 ** 3)  # Convert to GB
        monthly_rate = self.STORAGE_COSTS.get(artifact.type, 0.023)
        daily_rate = monthly_rate / 30
        
        return gb_size * daily_rate * days
    
    def calculate_processing_cost(self, operation: str, artifact: Artifact) -> float:
        """Calculate cost for a processing operation."""
        base_cost = self.PROCESSING_COSTS.get(operation, 0.001)
        
        # Scale cost based on artifact size (larger artifacts cost more to process)
        size_multiplier = min(artifact.size_bytes / (1024 ** 2), 10)  # Cap at 10x for very large files
        
        return base_cost * (1 + size_multiplier * 0.1)
    
    def get_cost_breakdown(self, artifact: Artifact, days: int = 30) -> Dict[str, float]:
        """Get detailed cost breakdown for an artifact."""
        storage_cost = self.calculate_storage_cost(artifact, days)
        
        return {
            "storage_cost": storage_cost,
            "artifact_id": artifact.id,
            "artifact_type": artifact.type.value,
            "size_gb": artifact.size_bytes / (1024 ** 3),
            "days": days
        }