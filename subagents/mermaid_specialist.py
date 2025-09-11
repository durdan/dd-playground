from typing import Dict, List
from models.specification_template import SpecificationTemplate, TemplateType

class MermaidSpecialist:
    """Subagent specialized in creating Mermaid diagrams for templates"""
    
    def __init__(self):
        self.diagram_templates = {
            TemplateType.API_SPECIFICATION: self._api_diagram_template,
            TemplateType.DATABASE_SCHEMA: self._database_diagram_template,
            TemplateType.SYSTEM_ARCHITECTURE: self._system_diagram_template,
            TemplateType.USER_INTERFACE: self._ui_diagram_template,
            TemplateType.BUSINESS_PROCESS: self._process_diagram_template,
            TemplateType.SECURITY_REQUIREMENTS: self._security_diagram_template,
        }
    
    def generate_structure_diagram(self, template: SpecificationTemplate) -> str:
        """Generate a Mermaid diagram showing template structure"""
        if template.template_type not in self.diagram_templates:
            raise ValueError(f"Unsupported template type: {template.template_type}")
        
        return self.diagram_templates[template.template_type](template)
    
    def _api_diagram_template(self, template: SpecificationTemplate) -> str:
        return """
graph TD
    A[API Specification] --> B[Endpoints]
    A --> C[Authentication]
    A --> D[Data Models]
    A --> E[Error Handling]
    
    B --> B1[GET /users]
    B --> B2[POST /users]
    B --> B3[PUT /users/:id]
    B --> B4[DELETE /users/:id]
    
    C --> C1[JWT Token]
    C --> C2[API Keys]
    
    D --> D1[User Model]
    D --> D2[Response Model]
    
    E --> E1[4xx Client Errors]
    E --> E2[5xx Server Errors]
"""
    
    def _database_diagram_template(self, template: SpecificationTemplate) -> str:
        return """
erDiagram
    USER {
        int id PK
        string email UK
        string name
        datetime created_at
    }
    
    PROFILE {
        int id PK
        int user_id FK
        string bio
        string avatar_url
    }
    
    POST {
        int id PK
        int user_id FK
        string title
        text content
        datetime created_at
    }
    
    USER ||--|| PROFILE : has
    USER ||--o{ POST : creates
"""
    
    def _system_diagram_template(self, template: SpecificationTemplate) -> str:
        return """
graph TB
    subgraph "Frontend"
        UI[User Interface]
        WEB[Web Application]
    end
    
    subgraph "Backend"
        API[API Gateway]
        AUTH[Auth Service]
        BIZ[Business Logic]
    end
    
    subgraph "Data Layer"
        DB[(Database)]
        CACHE[(Cache)]
    end
    
    UI --> WEB
    WEB --> API
    API --> AUTH
    API --> BIZ
    BIZ --> DB
    BIZ --> CACHE
"""
    
    def _ui_diagram_template(self, template: SpecificationTemplate) -> str:
        return """
graph TD
    A[User Interface] --> B[Navigation]
    A --> C[Content Area]
    A --> D[Sidebar]
    A --> E[Footer]
    
    B --> B1[Header Menu]
    B --> B2[Breadcrumbs]
    
    C --> C1[Main Content]
    C --> C2[Forms]
    C --> C3[Data Tables]
    
    D --> D1[Filters]
    D --> D2[Quick Actions]
"""
    
    def _process_diagram_template(self, template: SpecificationTemplate) -> str:
        return """
flowchart TD
    START([Start]) --> INPUT[Gather Input]
    INPUT --> VALIDATE{Validate Data}
    VALIDATE -->|Valid| PROCESS[Process Request]
    VALIDATE -->|Invalid| ERROR[Return Error]
    PROCESS --> SAVE[Save to Database]
    SAVE --> NOTIFY[Send Notification]
    NOTIFY --> END([End])
    ERROR --> END
"""
    
    def _security_diagram_template(self, template: SpecificationTemplate) -> str:
        return """
graph TD
    A[Security Requirements] --> B[Authentication]
    A --> C[Authorization]
    A --> D[Data Protection]
    A --> E[Network Security]
    
    B --> B1[Multi-Factor Auth]
    B --> B2[Password Policy]
    
    C --> C1[Role-Based Access]
    C --> C2[Permission Matrix]
    
    D --> D1[Encryption at Rest]
    D --> D2[Encryption in Transit]
    
    E --> E1[HTTPS/TLS]
    E --> E2[Firewall Rules]
"""