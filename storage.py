from typing import Dict, List, Optional
from models import Feature, Release

class InMemoryStorage:
    def __init__(self):
        self.features: Dict[str, Feature] = {}
        self.releases: Dict[str, Release] = {}
    
    def save_feature(self, feature: Feature) -> None:
        self.features[feature.id] = feature
    
    def get_feature(self, feature_id: str) -> Optional[Feature]:
        return self.features.get(feature_id)
    
    def get_all_features(self) -> List[Feature]:
        return list(self.features.values())
    
    def save_release(self, release: Release) -> None:
        self.releases[release.id] = release
    
    def get_release(self, release_id: str) -> Optional[Release]:
        return self.releases.get(release_id)
    
    def get_all_releases(self) -> List[Release]:
        return list(self.releases.values())