from typing import List
from datetime import datetime
from models import Feature, Release
from storage import InMemoryStorage
from intake_service import IntakeService
from development_service import DevelopmentService
from release_service import ReleaseService

class WorkflowEngine:
    def __init__(self):
        self.storage = InMemoryStorage()
        self.intake_service = IntakeService(self.storage)
        self.development_service = DevelopmentService(self.storage)
        self.release_service = ReleaseService(self.storage)
    
    def end_to_end_flow(self, title: str, description: str, priority: str,
                       version: str, assignee: str = None, 
                       estimated_hours: int = None) -> dict:
        """Complete flow from intake to release prep"""
        
        # 1. Intake
        feature = self.intake_service.submit_feature_request(
            title, description, priority, assignee, estimated_hours
        )
        
        # 2. Development workflow
        feature = self.development_service.start_development(feature.id)
        feature = self.development_service.complete_development(feature.id)
        feature = self.development_service.complete_testing(feature.id)
        
        # 3. Release preparation
        release = self.release_service.create_release(version, [feature.id])
        
        return {
            "feature": feature,
            "release": release,
            "status": "Ready for release"
        }
    
    def batch_release_prep(self, version: str, feature_ids: List[str]) -> Release:
        """Prepare release with multiple existing features"""
        return self.release_service.create_release(version, feature_ids)
    
    def get_pipeline_status(self) -> dict:
        """Get overview of current pipeline status"""
        features = self.storage.get_all_features()
        releases = self.storage.get_all_releases()
        
        status_counts = {}
        for feature in features:
            status = feature.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            "features_by_status": status_counts,
            "total_features": len(features),
            "total_releases": len(releases),
            "ready_for_release": len(self.release_service.get_ready_features())
        }