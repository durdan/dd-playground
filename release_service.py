from datetime import datetime
from typing import List
from models import Feature, Release, FeatureStatus
from storage import InMemoryStorage

class ReleaseService:
    def __init__(self, storage: InMemoryStorage):
        self.storage = storage
    
    def create_release(self, version: str, feature_ids: List[str], 
                      target_date: datetime = None) -> Release:
        if not version or not version.strip():
            raise ValueError("Release version is required")
        
        if not feature_ids:
            raise ValueError("At least one feature is required for a release")
        
        # Validate all features exist and are ready
        features = []
        for feature_id in feature_ids:
            feature = self.storage.get_feature(feature_id)
            if not feature:
                raise ValueError(f"Feature {feature_id} not found")
            if feature.status != FeatureStatus.READY_FOR_RELEASE:
                raise ValueError(f"Feature {feature_id} is not ready for release (status: {feature.status.value})")
            features.append(feature)
        
        release_id = f"REL-{len(self.storage.releases) + 1:04d}"
        
        release = Release(
            id=release_id,
            version=version.strip(),
            features=feature_ids,
            created_at=datetime.now(),
            target_date=target_date,
            is_ready=True
        )
        
        self.storage.save_release(release)
        return release
    
    def get_ready_features(self) -> List[Feature]:
        return [f for f in self.storage.get_all_features() 
                if f.status == FeatureStatus.READY_FOR_RELEASE]