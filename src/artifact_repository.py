from typing import List, Optional, Dict, Any
from datetime import datetime
import json
import os
from .artifact import Artifact, ArtifactStatus, ArtifactType

class ArtifactRepository:
    def __init__(self, storage_path: str = "data/artifacts"):
        self.storage_path = storage_path
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        os.makedirs(self.storage_path, exist_ok=True)
        os.makedirs(f"{self.storage_path}/metadata", exist_ok=True)
    
    def _get_metadata_path(self, artifact_id: str) -> str:
        return f"{self.storage_path}/metadata/{artifact_id}.json"
    
    def save(self, artifact: Artifact) -> None:
        metadata_path = self._get_metadata_path(artifact.id)
        artifact_data = {
            "id": artifact.id,
            "name": artifact.name,
            "type": artifact.type.value,
            "size_bytes": artifact.size_bytes,
            "content_hash": artifact.content_hash,
            "metadata": artifact.metadata,
            "created_at": artifact.created_at.isoformat(),
            "updated_at": artifact.updated_at.isoformat(),
            "status": artifact.status.value,
            "storage_path": artifact.storage_path,
            "version": artifact.version,
            "parent_id": artifact.parent_id
        }
        
        with open(metadata_path, 'w') as f:
            json.dump(artifact_data, f, indent=2)
    
    def find_by_id(self, artifact_id: str) -> Optional[Artifact]:
        metadata_path = self._get_metadata_path(artifact_id)
        if not os.path.exists(metadata_path):
            return None
        
        try:
            with open(metadata_path, 'r') as f:
                data = json.load(f)
            
            return Artifact(
                id=data["id"],
                name=data["name"],
                type=ArtifactType(data["type"]),
                size_bytes=data["size_bytes"],
                content_hash=data["content_hash"],
                metadata=data["metadata"],
                created_at=datetime.fromisoformat(data["created_at"]),
                updated_at=datetime.fromisoformat(data["updated_at"]),
                status=ArtifactStatus(data["status"]),
                storage_path=data.get("storage_path"),
                version=data.get("version", 1),
                parent_id=data.get("parent_id")
            )
        except (json.JSONDecodeError, KeyError, ValueError):
            return None
    
    def find_all(self, status: Optional[ArtifactStatus] = None) -> List[Artifact]:
        artifacts = []
        metadata_dir = f"{self.storage_path}/metadata"
        
        if not os.path.exists(metadata_dir):
            return artifacts
        
        for filename in os.listdir(metadata_dir):
            if filename.endswith('.json'):
                artifact_id = filename[:-5]  # Remove .json extension
                artifact = self.find_by_id(artifact_id)
                if artifact and (status is None or artifact.status == status):
                    artifacts.append(artifact)
        
        return artifacts
    
    def delete(self, artifact_id: str) -> bool:
        metadata_path = self._get_metadata_path(artifact_id)
        if os.path.exists(metadata_path):
            os.remove(metadata_path)
            return True
        return False