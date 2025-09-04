from models import Feature, FeatureStatus
from storage import InMemoryStorage

class DevelopmentService:
    def __init__(self, storage: InMemoryStorage):
        self.storage = storage
    
    def start_development(self, feature_id: str) -> Feature:
        feature = self._get_feature_or_raise(feature_id)
        
        if feature.status != FeatureStatus.INTAKE:
            raise ValueError(f"Feature {feature_id} must be in intake status to start development")
        
        feature.update_status(FeatureStatus.IN_DEVELOPMENT)
        self.storage.save_feature(feature)
        return feature
    
    def complete_development(self, feature_id: str) -> Feature:
        feature = self._get_feature_or_raise(feature_id)
        
        if feature.status != FeatureStatus.IN_DEVELOPMENT:
            raise ValueError(f"Feature {feature_id} must be in development to complete")
        
        feature.update_status(FeatureStatus.IN_TESTING)
        self.storage.save_feature(feature)
        return feature
    
    def complete_testing(self, feature_id: str) -> Feature:
        feature = self._get_feature_or_raise(feature_id)
        
        if feature.status != FeatureStatus.IN_TESTING:
            raise ValueError(f"Feature {feature_id} must be in testing to complete testing")
        
        feature.update_status(FeatureStatus.READY_FOR_RELEASE)
        self.storage.save_feature(feature)
        return feature
    
    def _get_feature_or_raise(self, feature_id: str) -> Feature:
        feature = self.storage.get_feature(feature_id)
        if not feature:
            raise ValueError(f"Feature {feature_id} not found")
        return feature