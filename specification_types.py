from enum import Enum

class SpecificationType(Enum):
    BUSINESS_ANALYSIS = "business_analysis"
    TEST_SPECS = "test_specs"
    ARCHITECTURE_SPECS = "architecture_specs"
    USER_STORIES = "user_stories"
    API_DOCS = "api_docs"

class ExportFormat(Enum):
    MARKDOWN = "markdown"
    JSON = "json"
    HTML = "html"
    PDF = "pdf"