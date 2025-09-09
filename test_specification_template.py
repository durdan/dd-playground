from typing import List
from base_template import SpecificationTemplate
from template_types import TemplateSection

class TestSpecificationTemplate(SpecificationTemplate):
    def _create_sections(self) -> List[TemplateSection]:
        return [
            TemplateSection(
                title="Test Overview",
                subsections=[
                    TemplateSection("Test Objectives", "Primary goals and objectives of testing."),
                    TemplateSection("Scope", "What will and will not be tested."),
                    TemplateSection("Test Approach", "Overall testing strategy and methodology.")
                ]
            ),
            TemplateSection(
                title="Test Environment",
                subsections=[
                    TemplateSection("Hardware Requirements", "Required hardware specifications."),
                    TemplateSection("Software Requirements", "Required software and tools."),
                    TemplateSection("Test Data", "Description of test data requirements.")
                ]
            ),
            TemplateSection(
                title="Test Cases",
                subsections=[
                    TemplateSection("Functional Test Cases", "Test cases for functional requirements."),
                    TemplateSection("Non-Functional Test Cases", "Performance, security, usability tests."),
                    TemplateSection("Integration Test Cases", "System integration test scenarios."),
                    TemplateSection("Regression Test Cases", "Tests to ensure existing functionality.")
                ]
            ),
            TemplateSection(
                title="Test Execution",
                subsections=[
                    TemplateSection("Test Schedule", "Timeline for test execution phases."),
                    TemplateSection("Entry Criteria", "Conditions that must be met before testing."),
                    TemplateSection("Exit Criteria", "Conditions for completing testing."),
                    TemplateSection("Defect Management", "Process for reporting and tracking defects.")
                ]
            ),
            TemplateSection(
                title="Test Deliverables",
                content="List of all test artifacts and documentation to be delivered."
            ),
            TemplateSection(
                title="Risks and Mitigation",
                content="Identified testing risks and mitigation strategies."
            )
        ]