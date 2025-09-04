"""Main application demonstrating CrewAI provider coordination"""
import os
from dotenv import load_dotenv
from ai_crew import AIProviderCrew

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize the AI provider crew
    crew = AIProviderCrew()
    
    print("=== AI Provider Coordination with CrewAI ===\n")
    
    # Example 1: Process a simple request
    print("1. Processing a simple request:")
    result = crew.process_request(
        "Explain quantum computing in simple terms",
        requirements={"max_tokens": 150, "temperature": 0.7}
    )
    print(f"Result: {result}\n")
    
    # Example 2: Get provider status
    print("2. Getting provider status:")
    status = crew.get_provider_status()
    print(f"Status: {status}\n")
    
    # Example 3: Optimize routing
    print("3. Optimizing routing:")
    optimization = crew.optimize_routing()
    print(f"Optimization: {optimization}\n")
    
    # Example 4: Process multiple requests to see load balancing
    print("4. Processing multiple requests:")
    requests = [
        "What is machine learning?",
        "Explain neural networks",
        "How does AI work?"
    ]
    
    for i, request in enumerate(requests, 1):
        print(f"Request {i}: {request}")
        result = crew.process_request(request)
        print(f"Response: {result[:100]}...\n")

if __name__ == "__main__":
    main()