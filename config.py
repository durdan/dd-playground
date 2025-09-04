from dataclasses import dataclass
from typing import Dict, Any
import os

@dataclass
class ReleaseDocConfig:
    template_dir: str = "templates"
    output_dir: str = "releases"
    default_template: str = "release_notes.md"
    include_audit_trail: bool = True
    include_approval_chain: bool = True
    
    def __post_init__(self):
        os.makedirs(self.output_dir, exist_ok=True)

DEFAULT_CONFIG = ReleaseDocConfig()

# Template variables mapping
TEMPLATE_VARS = {
    'release_version': 'version',
    'release_date': 'date',
    'changes': 'changes',
    'audit_records': 'audit_records',
    'approvals': 'approvals',
    'deployment_info': 'deployment'
}