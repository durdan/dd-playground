from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum

class ArtifactType(Enum):
    DOCUMENT = "document"
    IMAGE = "image"
    MODEL = "model"
    DATASET = "dataset"
    CODE = "code"

class ArtifactStatus(Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"

@dataclass
class Artifact:
    id: str
    name: str
    type: ArtifactType
    size_bytes: int
    content_hash: str
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    status: ArtifactStatus = ArtifactStatus.ACTIVE
    storage_path: Optional[str] = None
    version: int = 1
    parent_id: Optional[str] = None
    
    def __post_init__(self):
        if not self.id:
            raise ValueError("Artifact ID cannot be empty")
        if not self.name:
            raise ValueError("Artifact name cannot be empty")
        if self.size_bytes < 0:
            raise ValueError("Artifact size cannot be negative")