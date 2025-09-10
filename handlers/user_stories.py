from typing import Dict, Any
from .base import SpecificationHandler
from ..exceptions import ValidationError

class UserStoryHandler(SpecificationHandler):
    """Handler for user story specifications"""
    
    def validate_input(self, input_data: Dict[str, Any]) -> None:
        required_fields = ["epic_name", "stories"]
        for field in required_fields:
            if field not in input_data:
                raise ValidationError(f"Missing required field: {field}")
    
    def generate(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(input_data)
        
        content = {
            "title": f"User Stories: {input_data['epic_name']}",
            "sections": {
                "epic_overview": self._generate_epic_overview(input_data),
                "user_stories": self._process_user_stories(input_data["stories"]),
                "acceptance_criteria": self._generate_acceptance_criteria(input_data),
                "definition_of_done": input_data.get("definition_of_done", [])
            }
        }
        
        return self._add_metadata(content)
    
    def _generate_epic_overview(self, input_data: Dict[str, Any]) -> str:
        return f"Epic: {input_data['epic_name']} - {input_data.get('epic_description', '')}"
    
    def _process_user_stories(self, stories: list) -> list:
        processed = []
        for story in stories:
            processed_story = {
                "id": story.get("id", ""),
                "title": story.get("title", ""),
                "as_a": story.get("as_a", "user"),
                "i_want": story.get("i_want", ""),
                "so_that": story.get("so_that", ""),
                "priority": story.get("priority", "medium"),
                "story_points": story.get("story_points", 0)
            }
            
            if self.config.include_examples:
                processed_story["examples"] = story.get("examples", [])
            
            if self.config.detail_level == "high":
                processed_story["detailed_acceptance_criteria"] = story.get("acceptance_criteria", [])
            
            processed.append(processed_story)
        return processed
    
    def _generate_acceptance_criteria(self, input_data: Dict[str, Any]) -> list:
        criteria = []
        for story in input_data["stories"]:
            if "acceptance_criteria" in story:
                criteria.extend(story["acceptance_criteria"])
        return criteria