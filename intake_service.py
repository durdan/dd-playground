from datetime import datetime
from models import Feature, FeatureStatus, Priority
from storage import InMemoryStorage

class IntakeService:
    def __init__(self, storage: InMemoryStorage):
        self.storage = storage
    
    def submit_feature_request(self, title: str, description: str, 
                             priority: str, assignee: str = None, 
                             estimated_hours: int = None) -> Feature:
        if not title or not title.strip():
            raise ValueError("Feature title is required")
        
        if not description or not description.strip():
            raise ValueError("Feature description is required")
        
        try:
            priority_enum = Priority(priority.lower())
        except ValueError:
            raise ValueError(f"Invalid priority. Must be one of: {[p.value for p in Priority]}")
        
        if estimated_hours is not None and estimated_hours <= 0:
            raise ValueError("Estimated hours must be positive")
        
        feature_id = f"FEAT-{len(self.storage.features) + 1:04d}"
        now = datetime.now()
        
        feature = Feature(
            id=feature_id,
            title=title.strip(),
            description=description.strip(),
            priority=priority_enum,
            status=FeatureStatus.INTAKE,
            created_at=now,
            updated_at=now,
            assignee=assignee,
            estimated_hours=estimated_hours
        )
        
        self.storage.save_feature(feature)
        return feature