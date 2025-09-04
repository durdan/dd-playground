import json
import os
import shutil
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import asdict

class ModelVersionManager:
    def __init__(self, models_path: str = "/models"):
        self.models_path = models_path
        self.metadata_file = os.path.join(models_path, "versions.json")
        self._ensure_directory()
    
    def _ensure_directory(self):
        os.makedirs(self.models_path, exist_ok=True)
    
    def _load_metadata(self) -> Dict:
        if not os.path.exists(self.metadata_file):
            return {"models": {}}
        
        with open(self.metadata_file, 'r') as f:
            return json.load(f)
    
    def _save_metadata(self, metadata: Dict):
        with open(self.metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def register_version(self, model_name: str, version: str, model_path: str, 
                        metrics: Dict[str, float]) -> bool:
        """Register a new model version"""
        if not os.path.exists(model_path):
            raise ValueError(f"Model path does not exist: {model_path}")
        
        metadata = self._load_metadata()
        
        if model_name not in metadata["models"]:
            metadata["models"][model_name] = {"versions": {}, "active": None}
        
        # Copy model to versioned directory
        version_dir = os.path.join(self.models_path, model_name, version)
        os.makedirs(version_dir, exist_ok=True)
        
        if os.path.isdir(model_path):
            shutil.copytree(model_path, os.path.join(version_dir, "model"), 
                          dirs_exist_ok=True)
        else:
            shutil.copy2(model_path, os.path.join(version_dir, "model"))
        
        # Update metadata
        metadata["models"][model_name]["versions"][version] = {
            "registered_at": datetime.now().isoformat(),
            "metrics": metrics,
            "path": version_dir
        }
        
        self._save_metadata(metadata)
        return True
    
    def deploy_version(self, model_name: str, version: str) -> bool:
        """Deploy a specific version as active"""
        metadata = self._load_metadata()
        
        if (model_name not in metadata["models"] or 
            version not in metadata["models"][model_name]["versions"]):
            raise ValueError(f"Version {version} not found for model {model_name}")
        
        metadata["models"][model_name]["active"] = version
        metadata["models"][model_name]["versions"][version]["deployed_at"] = \
            datetime.now().isoformat()
        
        self._save_metadata(metadata)
        return True
    
    def rollback_version(self, model_name: str, target_version: str) -> bool:
        """Rollback to a previous version"""
        return self.deploy_version(model_name, target_version)
    
    def cleanup_old_versions(self, model_name: str, keep_count: int = 5):
        """Remove old versions, keeping only the most recent ones"""
        metadata = self._load_metadata()
        
        if model_name not in metadata["models"]:
            return
        
        versions = metadata["models"][model_name]["versions"]
        sorted_versions = sorted(
            versions.items(),
            key=lambda x: x[1]["registered_at"],
            reverse=True
        )
        
        if len(sorted_versions) <= keep_count:
            return
        
        versions_to_remove = sorted_versions[keep_count:]
        
        for version, version_data in versions_to_remove:
            # Remove directory
            version_path = version_data["path"]
            if os.path.exists(version_path):
                shutil.rmtree(version_path)
            
            # Remove from metadata
            del metadata["models"][model_name]["versions"][version]
        
        self._save_metadata(metadata)
    
    def get_active_version(self, model_name: str) -> Optional[str]:
        """Get the currently active version"""
        metadata = self._load_metadata()
        return metadata["models"].get(model_name, {}).get("active")
    
    def list_versions(self, model_name: str) -> List[Dict]:
        """List all versions for a model"""
        metadata = self._load_metadata()
        if model_name not in metadata["models"]:
            return []
        
        return [
            {"version": v, **data}
            for v, data in metadata["models"][model_name]["versions"].items()
        ]