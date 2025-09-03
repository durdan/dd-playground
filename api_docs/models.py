from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum

class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"

@dataclass
class Parameter:
    name: str
    type: str
    description: str
    required: bool = True
    example: Any = None

@dataclass
class Response:
    status_code: int
    description: str
    example: Dict[str, Any] = field(default_factory=dict)
    headers: Dict[str, str] = field(default_factory=dict)

@dataclass
class Endpoint:
    path: str
    method: HTTPMethod
    summary: str
    description: str
    tags: List[str] = field(default_factory=list)
    path_params: List[Parameter] = field(default_factory=list)
    query_params: List[Parameter] = field(default_factory=list)
    request_body: Optional[Dict[str, Any]] = None
    responses: List[Response] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.responses:
            self.responses = [Response(200, "Success")]