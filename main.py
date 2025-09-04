import os
import logging
from config.settings import config
from crews.base_crew import ContentCreationCrew


def setup_logging():
    """Configure logging based on environment settings."""
    logging.basicConfig(
        level=getattr(logging, config.log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def main():
    """Main application entry point."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info(f"Starting CrewAI application in {config.environment} environment")
    
    # Validate required configuration
    if not config.openai_api_key or config.openai_api_key.startswith("your_"):
        logger.error("OpenAI API key not configured properly")
        return
    
    # Set OpenAI API key for CrewAI
    os.environ["OPENAI_API_KEY"] = config.openai_api_key
    
    try:
        # Example: Create and run a content creation crew
        topic = "The Future of Artificial Intelligence"
        crew = ContentCreationCrew(topic)
        
        logger.info(f"Executing crew for topic: {topic}")
        result = crew.kickoff()
        
        logger.info("Crew execution completed successfully")
        print("\n" + "="*50)
        print("CREW EXECUTION RESULT:")
        print("="*50)
        print(result)
        
    except Exception as e:
        logger.error(f"Error during crew execution: {e}")
        raise


if __name__ == "__main__":
    main()